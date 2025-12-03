from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models import User
from app.routers.auth import get_current_user
from app.schemas import UserOut

router = APIRouter(prefix="/users", tags=["users"])


async def _ensure_admin(current_user: User) -> None:
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")


from typing import Optional
from sqlalchemy import or_

@router.get("", response_model=list[UserOut])
async def list_users(
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
) -> list[UserOut]:
    await _ensure_admin(current_user)
    query = select(User).order_by(User.created_at.desc())
    
    if search:
        search_term = f"%{search}%"
        query = query.where(
            or_(
                User.username.ilike(search_term),
                User.nickname.ilike(search_term)
            )
        )
        
    result = await db.execute(query)
    users = result.scalars().all()
    return users


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)
) -> Response:
    await _ensure_admin(current_user)
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    await db.delete(user)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
