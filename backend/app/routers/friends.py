from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models import Follow, User
from app.routers.auth import get_current_user
from app.schemas import UserOut

router = APIRouter(tags=["friends"])


@router.post("/users/{user_id}/follow", status_code=status.HTTP_204_NO_CONTENT)
async def follow_user(
    user_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)
):
    if user_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot follow yourself")

    target = await db.get(User, user_id)
    if not target:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    result = await db.execute(
        select(Follow).where(Follow.follower_id == current_user.id, Follow.followed_id == user_id)
    )
    existing = result.scalar_one_or_none()
    if existing:
        return

    db.add(Follow(follower_id=current_user.id, followed_id=user_id))
    await db.commit()
    return


@router.delete("/users/{user_id}/follow", status_code=status.HTTP_204_NO_CONTENT)
async def unfollow_user(
    user_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Follow).where(Follow.follower_id == current_user.id, Follow.followed_id == user_id)
    )
    follow = result.scalar_one_or_none()
    if follow:
        await db.delete(follow)
        await db.commit()
    return


@router.get("/users/{user_id}/followers", response_model=list[UserOut])
async def list_followers(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Follow)
        .options(selectinload(Follow.follower))
        .where(Follow.followed_id == user_id)
    )
    follows = result.scalars().all()
    return [f.follower for f in follows if f.follower]


@router.get("/users/{user_id}/following", response_model=list[UserOut])
async def list_following(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Follow)
        .options(selectinload(Follow.followed))
        .where(Follow.follower_id == user_id)
    )
    follows = result.scalars().all()
    return [f.followed for f in follows if f.followed]
