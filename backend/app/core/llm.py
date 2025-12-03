from typing import List


async def analyze_content(text: str) -> List[str]:
    """
    Mock LLM analysis that generates simple tags from keywords.
    Replace with real LLM API integration in production.
    """
    if not text:
        return []
    keywords = []
    lowered = text.lower()
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
            keywords.append(tag)
    return keywords
