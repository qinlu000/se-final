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

    # Real Daily Active Users (DAU) Calculation
    # Definition: Anyone who posted, commented, or rated on that day.
    from app.models import Comment, Rating
    from sqlalchemy import union

    today = datetime.utcnow().date()
    
    # Total Interactions (Comments + Ratings)
    total_comments = (await db.execute(select(func.count(Comment.id)))).scalar_one() or 0
    total_ratings = (await db.execute(select(func.count(Rating.id)))).scalar_one() or 0
    total_interactions = total_comments + total_ratings

    daily_active = []
    
    for i in range(7):
        target_date = today - timedelta(days=6 - i)
        start_dt = datetime.combine(target_date, datetime.min.time())
        end_dt = datetime.combine(target_date, datetime.max.time())
        
        # Select user_ids from all 3 tables for this time range
        q_posts = select(Post.user_id).where(Post.created_at >= start_dt, Post.created_at <= end_dt)
        q_comments = select(Comment.user_id).where(Comment.created_at >= start_dt, Comment.created_at <= end_dt)
        q_ratings = select(Rating.user_id).where(Rating.created_at >= start_dt, Rating.created_at <= end_dt)
        
        # Union them to get unique active users
        u_query = union(q_posts, q_comments, q_ratings)
        
        # Count the result of the union
        result = await db.execute(
             select(func.count()).select_from(u_query.subquery())
        )
        active_count = result.scalar_one() or 0
        
        daily_active.append({"date": target_date.isoformat(), "active": active_count})

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
        "total_interactions": total_interactions,
        "daily_active": daily_active,
        "content_type_distribution": content_type_distribution,
    }
