import json
import os
from typing import Any, Dict, List, Optional

from openai import AsyncOpenAI

# OpenRouter client (DeepSeek via OpenRouter)
_api_key = os.getenv("OPENROUTER_API_KEY")
_base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
_model = os.getenv("OPENROUTER_MODEL", "deepseek/deepseek-v3")

# Configure client with explicit timeout and retries
client = AsyncOpenAI(
    api_key=_api_key, 
    base_url=_base_url,
    timeout=60.0,
    max_retries=3
) if _api_key else None


def _fallback_summary(content: str, mode: str = "summary") -> Dict[str, Any]:
    clean = (content or "").strip()
    snippet = clean[:120] + ("..." if len(clean) > 120 else "")
    res = {
        "summary": snippet or None,
        "tags": _keyword_tags(clean),
        "suggestions": [],
        "translated_content": None,
        "vibe": None,
    }

    if mode == "tags":
        res["summary"] = None
    if mode == "reply":
        base = res["summary"] or "已阅，期待更多分享！"
        res["suggestions"] = [
            f"{base}",
            f"{base} 再多讲讲吧！",
            f"想听听细节～",
        ]
    if mode == "polish":
        res["summary"] = f"{clean}"
    if mode == "emojify":
        res["summary"] = f"{clean} 😊"
    if mode == "title":
        res["suggestions"] = [
            f"灵感速递：{clean[:12]}",
            f"{clean[:10]} · 精选",
            f"{clean[:8]} · 热门",
        ]
    if mode == "translate":
        res["translated_content"] = clean
    if mode == "vibe":
        res["vibe"] = {"label": "neutral", "score": 0.5, "emoji": "😐", "color": "#FFE600"}
        res["summary"] = res["summary"] or clean
    
    return res


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
    content: str,
    mode: str = "summary",
    tone: str = "friendly",
    include_tags: bool = True,
    target_lang: str = "zh",
) -> Dict[str, Any]:
    """
    Call DeepSeek via OpenRouter to produce summary/tags/reply suggestions / magic compose.
    Falls back to deterministic heuristics if API key or call is unavailable.
    """
    clean = (content or "").strip()
    if not clean:
        return {"summary": None, "tags": [], "suggestions": [], "translated_content": None, "vibe": None}

    # Fallback path if no API key configured
    if client is None:
        return _fallback_summary(clean, mode)

    system_prompt = (
        "You are a concise social-media assistant. Return ONLY valid JSON.\n"
        "Supported modes:\n"
        "- summary: summarize content (<=120 chars) -> result in 'summary'\n"
        "- tags: generate hashtags -> result in 'tags'\n"
        "- reply: generate 3 reply suggestions -> result in 'suggestions'\n"
        "- polish: rewrite content fluently -> result in 'summary'\n"
        "- emojify: add emojis to content -> result in 'summary'\n"
        "- title: generate 3 catchy titles -> result in 'suggestions'\n"
        "- translate: translate to target_lang -> result in 'translated_content'\n"
        "- vibe: analyze sentiment -> result in 'vibe'\n"
        "JSON keys: summary, tags, suggestions, translated_content, vibe\n"
        "Tone options: friendly|professional|humorous."
    )

    user_prompt = f"""
Content: \"\"\"{clean}\"\"\"
Mode: {mode}
Tone: {tone}
Include tags: {include_tags}
Target language: {target_lang}
"""

    # ... (inside ask_ai_assistant)
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
        
        # 1. Clean Markdown wrappers (Robustness Fix)
        if "```" in raw:
            raw = raw.replace("```json", "").replace("```", "").strip()
        
        data = json.loads(raw)
        
        # 2. Extract fields
        res = {
            "summary": data.get("summary"),
            "tags": data.get("tags") if include_tags else [],
            "suggestions": data.get("suggestions") or [],
            "translated_content": data.get("translated_content"),
            "vibe": data.get("vibe"),
        }
        
        # 3. Validate Result (Prevent "No Result" error)
        # If specific mode return is empty, treat as failure to trigger smart fallback
        if mode == "title" and not res["suggestions"]:
            raise ValueError("Empty suggestions for title")
        if mode == "translate" and not res["translated_content"]:
            raise ValueError("Empty translation")
        if mode in ["summary", "polish", "emojify"] and not res["summary"]:
             raise ValueError("Empty summary")

        return res

    except Exception as e:
        print(f"[AI Error] {e}") # Optional logging
        return _fallback_summary(clean, mode)
