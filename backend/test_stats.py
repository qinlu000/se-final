import asyncio
from datetime import datetime, timedelta
from app.core.database import async_session_factory
from app.models import Post, Comment, Rating
from sqlalchemy import select, func, union

async def test_stats():
    async with async_session_factory() as db:
        today = datetime.utcnow().date()
        target_date = today # - timedelta(days=0)
        start_dt = datetime.combine(target_date, datetime.min.time())
        end_dt = datetime.combine(target_date, datetime.max.time())
        
        q_posts = select(Post.user_id).where(Post.created_at >= start_dt, Post.created_at <= end_dt)
        q_comments = select(Comment.user_id).where(Comment.created_at >= start_dt, Comment.created_at <= end_dt)
        q_ratings = select(Rating.user_id).where(Rating.created_at >= start_dt, Rating.created_at <= end_dt)
        
        # Test the problematic syntax
        try:
            print("Testing union query...")
            # Original code had .selected_columns(Post.user_id)
            u_query = union(q_posts, q_comments, q_ratings).selected_columns(Post.user_id) 
            print("Syntax seems valid object wise (unlikely)")
        except AttributeError as e:
            print(f"Caught expected error: {e}")
            
        # Test corrected syntax
        print("Testing corrected query...")
        u_query = union(q_posts, q_comments, q_ratings)
        result = await db.execute(
             select(func.count()).select_from(u_query.subquery())
        )
        print(f"Count: {result.scalar_one()}")

if __name__ == "__main__":
    asyncio.run(test_stats())
