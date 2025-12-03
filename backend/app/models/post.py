from enum import Enum

from sqlalchemy import Column, DateTime, Enum as SQLEnum, ForeignKey, Integer, JSON, Text, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class MediaType(str, Enum):
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    content = Column(Text, nullable=False)
    media_type = Column(SQLEnum(MediaType, name="media_type"), nullable=False)
    media_urls = Column(JSON, nullable=False, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    ratings = relationship("Rating", back_populates="post", cascade="all, delete-orphan")
    tags = relationship("Tag", secondary="post_tags", back_populates="posts")
