import asyncio
import sys
import os
import random
from datetime import datetime, timedelta

# Add parent dir to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import AsyncSessionLocal, engine, Base
from app.models import User, Post, Comment, Rating, Tag, Follow
from app.core.security import hash_password
from sqlalchemy import select

# Mock data
USERNAMES = ['alice', 'bob', 'charlie', 'david', 'eve', 'frank', 'grace', 'heidi']
AVATARS = [
    'https://api.dicebear.com/7.x/avataaars/svg?seed=alice',
    'https://api.dicebear.com/7.x/avataaars/svg?seed=bob',
    'https://api.dicebear.com/7.x/avataaars/svg?seed=charlie',
    'https://api.dicebear.com/7.x/avataaars/svg?seed=david',
    'https://api.dicebear.com/7.x/avataaars/svg?seed=eve',
    'https://api.dicebear.com/7.x/avataaars/svg?seed=frank',
    'https://api.dicebear.com/7.x/avataaars/svg?seed=grace',
    'https://api.dicebear.com/7.x/avataaars/svg?seed=heidi',
]
POST_CONTENTS = [
    "Just arrived in Paris! The Eiffel Tower is breathtaking. #travel #paris",
    "Had the best sushi ever tonight. Highly recommend! #food #sushi",
    "Coding late into the night. Coffee is my best friend. #tech #coding",
    "Morning run complete. 5k in 25 mins! #sport #running",
    "Watching the new Marvel movie. No spoilers please! #movie",
    "Listening to some jazz to relax. #music #chill",
    "Can't believe it's already December. Time flies.",
    "Anyone know a good place to fix a flat tire?",
    "My cat is so cute when she sleeps. #cat #pet",
    "Learning Vue 3 and FastAPI. It's a great combo! #tech #learning"
]
TAGS = ['travel', 'food', 'tech', 'sport', 'movie', 'music', 'cat', 'pet', 'learning', 'paris', 'sushi', 'coding', 'running', 'chill']

async def seed_data():
    print("Creating tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        print("Cleaning up old data...")
        # In a real app we might truncate, but here we'll just add new data if empty-ish
        # or just append. Let's append to avoid deleting admin.
        
        # 1. Create Users
        print("Seeding Users...")
        users = []
        for i, name in enumerate(USERNAMES):
            # Check if exists
            res = await db.execute(select(User).where(User.username == name))
            if res.scalar_one_or_none():
                continue
            
            user = User(
                username=name,
                password_hash=hash_password("123456"),
                nickname=name.capitalize(),
                avatar_url=AVATARS[i],
                is_admin=False
            )
            db.add(user)
            users.append(user)
        await db.commit()
        
        # Refresh users to get IDs
        user_models = []
        for name in USERNAMES:
            res = await db.execute(select(User).where(User.username == name))
            u = res.scalar_one_or_none()
            if u: user_models.append(u)

        if not user_models:
            print("No users created. Exiting.")
            return

        # 2. Create Tags
        print("Seeding Tags...")
        tag_models = {}
        for t_name in TAGS:
            res = await db.execute(select(Tag).where(Tag.name == t_name))
            tag = res.scalar_one_or_none()
            if not tag:
                tag = Tag(name=t_name)
                db.add(tag)
            tag_models[t_name] = tag
        await db.commit()

        # 3. Create Posts
        print("Seeding Posts...")
        for _ in range(20): # Create 20 random posts
            user = random.choice(user_models)
            content = random.choice(POST_CONTENTS)
            
            # Extract tags from content (simple hash check)
            post_tags = []
            for t_name in TAGS:
                if f"#{t_name}" in content.lower() or t_name in content.lower():
                    if t_name in tag_models:
                        post_tags.append(tag_models[t_name])
            
            post = Post(
                user_id=user.id,
                content=content,
                media_type="text", # Simplified for seed
                media_urls=[],
                tags=post_tags,
                created_at=datetime.utcnow() - timedelta(days=random.randint(0, 30))
            )
            db.add(post)
        await db.commit()

        # 4. Create Interactions (Comments, Ratings, Follows)
        print("Seeding Interactions...")
        # Fetch all posts
        res = await db.execute(select(Post))
        all_posts = res.scalars().all()

        for post in all_posts:
            # Random ratings
            for _ in range(random.randint(0, 5)):
                u = random.choice(user_models)
                if u.id == post.user_id: continue
                # Check existing
                res = await db.execute(select(Rating).where(Rating.user_id==u.id, Rating.post_id==post.id))
                if not res.scalar_one_or_none():
                    db.add(Rating(user_id=u.id, post_id=post.id, score=random.randint(3, 5)))
            
            # Random comments
            for _ in range(random.randint(0, 3)):
                u = random.choice(user_models)
                db.add(Comment(user_id=u.id, post_id=post.id, content="Nice post!"))

        # Random follows
        for u in user_models:
            targets = random.sample(user_models, k=random.randint(1, 3))
            for t in targets:
                if u.id == t.id: continue
                res = await db.execute(select(Follow).where(Follow.follower_id==u.id, Follow.followed_id==t.id))
                if not res.scalar_one_or_none():
                    db.add(Follow(follower_id=u.id, followed_id=t.id))

        await db.commit()
        print("Seed data generation complete!")

if __name__ == "__main__":
    asyncio.run(seed_data())
