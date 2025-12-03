from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Integer, UniqueConstraint, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Rating(Base):
    __tablename__ = "ratings"
    __table_args__ = (
        UniqueConstraint("post_id", "user_id", name="uq_rating_post_user"),
        CheckConstraint("score BETWEEN 1 AND 5", name="ck_rating_score_range"),
    )

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    score = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    post = relationship("Post", back_populates="ratings")
    user = relationship("User", back_populates="ratings")
