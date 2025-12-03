from fastapi import HTTPException, status

SENSITIVE_WORDS = {"bad", "evil"}


def check_sensitive_words(text: str) -> None:
    """Raise HTTP 400 if any sensitive word is contained in text."""
    if not text:
        return
    lowered = text.lower()
    for word in SENSITIVE_WORDS:
        if word in lowered:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Content contains sensitive words",
            )
