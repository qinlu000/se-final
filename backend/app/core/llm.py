import json
import os
from typing import Any, Dict, List

from openai import AsyncOpenAI

# OpenRouter client (DeepSeek via OpenRouter)
_api_key = os.getenv("OPENROUTER_API_KEY")
_base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
_model = os.getenv("OPENROUTER_MODEL", "deepseek/deepseek-v3")

client = AsyncOpenAI(api_key=_api_key, base_url=_base_url) if _api_key else None


def _fallback_summary(content: str) -> Dict[str, Any]:
    clean = (content or "").strip()
    snippet = clean[:120] + ("..." if len(clean) > 120 else "")
    return {
        "summary": snippet or None,
        "tags": _keyword_tags(clean),
        "suggestions": [],
    }


def _keyword_tags(text: str) -> List[str]:
    if not text:
        return []
    lowered = text.lower()
    tags: List[str] = []
    for word, tag in [
        ("travel", "travel"),
        ("food", "food"),
        ("music", "music"),
        ("movie", "movie"),
        ("sport", "sport"),
        ("tech", "tech"),
        ("study", "study"),
    ]:
        if word in lowered:
            tags.append(tag)
    return tags


async def analyze_content(text: str) -> List[str]:
    """Lightweight tag inference used during post creation (kept LLM-free)."""
    return _keyword_tags(text)


async def ask_ai_assistant(
    content: str, mode: str = "summary", tone: str = "friendly", include_tags: bool = True
) -> Dict[str, Any]:
    """
    Call DeepSeek via OpenRouter to produce summary/tags/reply suggestions.
    Falls back to deterministic heuristics if API key or call is unavailable.
    """
    clean = (content or "").strip()
    if not clean:
        return {"summary": None, "tags": [], "suggestions": []}

    # Fallback path if no API key configured
    if client is None:
        resp = _fallback_summary(clean)
        if mode == "tags":
            resp["summary"] = None
        if mode == "reply":
            base = resp["summary"] or "已阅，期待更多分享！"
            resp["suggestions"] = [
                f"{base}",
                f"{base} 再多讲讲吧！",
                f"想听听细节～",
            ]
        return resp

    system_prompt = (
        "You are a concise social-media assistant. "
        "Return ONLY valid JSON with keys: summary (string|null, max 120 chars), "
        "tags (array of strings, lowercase, no #), suggestions (array of strings, max 3). "
        "Respect tone and mode. If a field is not applicable, use null or empty array."
    )

    user_prompt = f"""
Content to analyze:
\"\"\"{clean}\"\"\"
Mode: {mode} (options: summary, reply, tags)
Tone: {tone} (friendly | professional | humorous)
Include tags: {include_tags}
"""

    try:
        completion = await client.chat.completions.create(
            model=_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.4,
            max_tokens=400,
        )
        raw = completion.choices[0].message.content or "{}"
        data = json.loads(raw)
        return {
            "summary": data.get("summary"),
            "tags": data.get("tags") if include_tags else [],
            "suggestions": data.get("suggestions") or [],
        }
    except Exception:
        return _fallback_summary(clean)
