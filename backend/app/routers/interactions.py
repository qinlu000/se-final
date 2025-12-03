from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.core.sensitive import check_sensitive_words
from app.models import Comment, Post, Rating, User
from app.routers.auth import get_current_user
from app.schemas import CommentCreate, CommentOut, RatingCreate, RatingOut

router = APIRouter(tags=["interactions"])


@router.post("/posts/{post_id}/comments", response_model=CommentOut, status_code=status.HTTP_201_CREATED)
async def add_comment(
    post_id: int,
    comment_in: CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CommentOut:
    check_sensitive_words(comment_in.content)
    post = await db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    comment = Comment(post_id=post_id, user_id=current_user.id, content=comment_in.content)
    db.add(comment)
    await db.commit()
    await db.refresh(comment)

    # Ensure user relationship is available for response serialization.
    comment.user = current_user
    return CommentOut.from_orm(comment)


@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Comment).options(selectinload(Comment.post)).where(Comment.id == comment_id)
    )
    comment = result.scalar_one_or_none()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    if not (
        current_user.is_admin
        or comment.user_id == current_user.id
        or (comment.post and comment.post.user_id == current_user.id)
    ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this comment")

    await db.delete(comment)
    await db.commit()
    return None


@router.post("/posts/{post_id}/rate", response_model=RatingOut)
async def rate_post(
    post_id: int,
    rating_in: RatingCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> RatingOut:
    post = await db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    result = await db.execute(
        select(Rating).where(Rating.post_id == post_id, Rating.user_id == current_user.id)
    )
    rating = result.scalar_one_or_none()

    if rating:
        rating.score = rating_in.score
    else:
        rating = Rating(post_id=post_id, user_id=current_user.id, score=rating_in.score)
        db.add(rating)

    await db.commit()
    await db.refresh(rating)
    rating.user = current_user
    return RatingOut.from_orm(rating)


@router.delete("/posts/{post_id}/rate", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rating(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Rating).where(Rating.post_id == post_id, Rating.user_id == current_user.id)
    )
    rating = result.scalar_one_or_none()
    if not rating:
        return None  # Idempotent

    await db.delete(rating)
    await db.commit()
    return None
