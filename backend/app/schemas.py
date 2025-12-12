from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from app.models.post import MediaType


class UserOut(BaseModel):
    id: int
    username: str
    nickname: Optional[str] = None
    avatar_url: Optional[str] = None
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True


class TagOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class CommentCreate(BaseModel):
    content: str


class CommentOut(BaseModel):
    id: int
    post_id: int
    user_id: int
    content: str
    created_at: datetime
    user: UserOut

    class Config:
        from_attributes = True


class RatingCreate(BaseModel):
    score: int = Field(..., ge=1, le=5)


class RatingOut(BaseModel):
    id: int
    post_id: int
    user_id: int
    score: int
    created_at: datetime
    user: UserOut

    class Config:
        from_attributes = True


class PostCreate(BaseModel):
    content: str
    media_type: MediaType
    media_urls: List[str]
    tags: List[str] = []


class PostOut(BaseModel):
    id: int
    user_id: int
    content: str
    media_type: MediaType
    media_urls: List[str]
    created_at: datetime
    updated_at: datetime
    user: UserOut
    tags: List[TagOut] = []
    comment_count: int = 0
    average_rating: Optional[float] = None
    is_following: bool = False
    is_liked: bool = False
    comments: List[CommentOut] = []

    class Config:
        from_attributes = True


class PostDetail(PostOut):
    comments: List[CommentOut] = []
    ratings: List[RatingOut] = []


class UploadResponse(BaseModel):
    url: str


class AssistantRequest(BaseModel):
    content: str
    mode: Literal[
        "summary",
        "reply",
        "tags",
        "polish",
        "emojify",
        "title",
        "translate",
        "vibe",
    ] = "summary"
    tone: Literal["friendly", "professional", "humorous"] = "friendly"
    include_tags: bool = True
    target_lang: str = "zh"


class AssistantResponse(BaseModel):
    status: Literal["ok", "sensitive", "error"] = "ok"
    summary: Optional[str] = None
    suggestions: List[str] = []
    tags: List[str] = []
    translated_content: Optional[str] = None
    vibe: Optional[dict] = None
