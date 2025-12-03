from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models import Post, User

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/dashboard")
async def get_dashboard_stats(db: AsyncSession = Depends(get_db)):
    total_users_result = await db.execute(select(func.count(User.id)))
    total_posts_result = await db.execute(select(func.count(Post.id)))

    total_users = total_users_result.scalar_one() or 0
    total_posts = total_posts_result.scalar_one() or 0

    # Mock daily active data for the past 7 days.
    today = datetime.utcnow().date()
    daily_active = []
    for i in range(7):
        day = today - timedelta(days=6 - i)
        daily_active.append({"date": day.isoformat(), "active": 50 + i * 5})

    # Content Type Distribution
    content_type_result = await db.execute(
        select(Post.media_type, func.count(Post.id)).group_by(Post.media_type)
    )
    content_type_distribution = [
        {"name": row[0], "value": row[1]} for row in content_type_result.all()
    ]

    return {
        "total_users": total_users,
        "total_posts": total_posts,
        "daily_active": daily_active,
        "content_type_distribution": content_type_distribution,
    }
