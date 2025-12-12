import hashlib
import time
from typing import Dict, Tuple

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.llm import ask_ai_assistant
from app.core.sensitive import check_sensitive_words
from app.schemas import AssistantRequest, AssistantResponse

router = APIRouter(prefix="/ai", tags=["ai"])

# --- Simple in-memory cache and rate limit (MVP) ---
_CACHE: Dict[str, Tuple[float, dict]] = {}
_CACHE_TTL_SECONDS = 60 * 60 * 24  # 24h
_RATE_LIMIT: Dict[str, list[float]] = {}
_RATE_LIMIT_PER_MIN = 10


def _get_ip(request: Request) -> str:
    return request.client.host or "unknown"


def _check_rate_limit(ip: str) -> None:
    now = time.time()
    history = [t for t in _RATE_LIMIT.get(ip, []) if now - t < 60]
    if len(history) >= _RATE_LIMIT_PER_MIN:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="AI request limit exceeded. Please try again later.",
        )
    history.append(now)
    _RATE_LIMIT[ip] = history


def _make_cache_key(body: AssistantRequest) -> str:
    raw = f"{body.content}|{body.mode}|{body.tone}|{body.include_tags}"
    return hashlib.sha256(raw.encode()).hexdigest()


@router.post("/assistant", response_model=AssistantResponse)
async def run_assistant(
    body: AssistantRequest, request: Request, db: AsyncSession = Depends(get_db)
) -> AssistantResponse:
    content = (body.content or "").strip()
    if not content:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Content is required")

    # 1) Sensitive input -> status=sensitive
    try:
        check_sensitive_words(content)
    except HTTPException:
        return AssistantResponse(status="sensitive")

    # 2) Rate limit
    _check_rate_limit(_get_ip(request))

    # 3) Cache
    cache_key = _make_cache_key(body)
    cached = _CACHE.get(cache_key)
    now = time.time()
    if cached and now - cached[0] < _CACHE_TTL_SECONDS:
        return AssistantResponse(status="ok", **cached[1])

    # 4) Call LLM (with fallback inside helper)
    result = await ask_ai_assistant(
        content=content,
        mode=body.mode,
        tone=body.tone,
        include_tags=body.include_tags,
    )

    # 5) Sensitive output check
    combined = " ".join(
        [
          result.get("summary") or "",
          " ".join(result.get("suggestions") or []),
          " ".join(result.get("tags") or []),
        ]
    )
    try:
        check_sensitive_words(combined)
    except HTTPException:
        return AssistantResponse(status="sensitive")

    # 6) Success + cache
    _CACHE[cache_key] = (now, result)
    return AssistantResponse(status="ok", **result)
