import asyncio
import sys
import os
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

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
    "Learning Vue 3 and FastAPI. It's a great combo! #tech #learning",
    "今天天气真好，去公园散步心情很棒！🎉 #生活 #快乐",
    "这个新餐厅太难吃了，服务也很差，避雷！👿 #吐槽 #美食",
    "工作压力好大，感觉快要崩溃了... 🌧️ #emo #加班",
    "学习 Rust 真的好难，但是很有趣！ #tech #rust",
    "Je suis très heureux aujourd'hui! (I am very happy today)",
    "Esta comida es deliciosa. (This food is delicious)",
    # Long Post 1: Tech Article
    """
    最近在研究微服务架构，发现它虽然能解决单体应用的扩展性问题，但也带来了复杂的运维成本。
    特别是服务发现、熔断降级、分布式链路追踪这些组件的引入，让整个系统变得极其庞大。
    对于初创团队来说，过早引入微服务可能是一个陷阱。
    更好的做法可能是模块化单体（Modular Monolith），在保持代码边界清晰的同时，避免网络调用的开销和分布式的复杂性。
    大家怎么看？欢迎评论区讨论！👇
    #tech #architecture #microservices
    """,
    # Long Post 2: Story
    """
    It was a rainy Tuesday when I first met him. He was standing under the awning of the old bookstore, holding a soaking wet umbrella.
    "Do you think it will ever stop?" he asked, looking at the grey sky.
    I smiled, "Eventually, everything stops."
    We ended up talking for hours about books, life, and the strange comfort of rainy days.
    Sometimes the best connections happen in the most unexpected moments.
    Life is funny that way. You never know who you might meet just by waiting for the rain to clear.
    #story #life #rain
    """,
    # Long Post 3: Movie Review
    """
    刚刚看完《星际穿越》重映，依然被震撼得说不出话。
    诺兰对五维空间的想象，以及汉斯季默的配乐，简直是天作之合。
    最打动我的还是库珀和墨菲之间的父女情，“爱是唯一可以穿越时间与空间的事物”。
    即使在浩瀚宇宙中，人类的情感依然是最强大的力量。
    强推大家去 IMAX 再刷一遍！
    评分：10/10 🌟🌟🌟🌟🌟
    #movie #interstellar #nolan
    """
]
TAGS = ['travel', 'food', 'tech', 'sport', 'movie', 'music', 'cat', 'pet', 'learning', 'paris', 'sushi', 'coding', 'running', 'chill', '生活', '快乐', '吐槽', '美食', 'emo', '加班', 'rust', 'architecture', 'microservices', 'story', 'life', 'rain', 'interstellar', 'nolan']

POST_TYPE_IMAGE = "image"
IMAGE_CAPTIONS = [
    "Look at this amazing view! #scenery #travel",
    "Delicious homemade dinner 🍳 #food #cooking",
    "My workspace setup for today 💻 #tech #setup",
    "Cute cat alert! 🐱 #cat #pet",
    "Sunset vibes 🌅 #sky #nature",
    "Art museum visit 🎨 #art #culture",
    "Coffee time ☕ #coffee #relax",
    "New kicks! 👟 #fashion #style"
]

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
        for _ in range(50): # Increased to 50
            user = random.choice(user_models)
            
            # Randomly decide type: 40% Image, 60% Text
            if random.random() < 0.4:
                content = random.choice(IMAGE_CAPTIONS)
                media_type = "image"
                # Use distinct seeds for variety
                img_seed = random.randint(100, 1000)
                media_urls = [f"https://picsum.photos/seed/{img_seed}/800/600"]
            else:
                content = random.choice(POST_CONTENTS)
                media_type = "text"
                media_urls = []

            # Extract tags
            post_tags = []
            for t_name in TAGS:
                if f"#{t_name}" in content.lower() or t_name in content.lower():
                    if t_name in tag_models:
                        post_tags.append(tag_models[t_name])
            
            # Distribute dates heavily in last 7 days for Real Stats visibility
            days_ago = random.choices(
                [0, 1, 2, 3, 4, 5, 6, 7, 10, 20, 30], 
                weights=[10, 8, 5, 5, 5, 5, 5, 2, 2, 1, 1],
                k=1
            )[0]
            created_at = datetime.utcnow() - timedelta(days=days_ago)

            post = Post(
                user_id=user.id,
                content=content,
                media_type=media_type, 
                media_urls=media_urls,
                tags=post_tags,
                created_at=created_at
            )
            db.add(post)
        await db.commit()

        # 4. Create Interactions (Comments, Ratings, Follows)
        print("Seeding Interactions...")
        # Fetch all posts again to include new ones
        res = await db.execute(select(Post))
        all_posts = res.scalars().all()

        for post in all_posts:
            # Random ratings
            for _ in range(random.randint(0, 8)): # More ratings
                u = random.choice(user_models)
                if u.id == post.user_id: continue
                
                # Check exist
                res = await db.execute(select(Rating).where(Rating.user_id==u.id, Rating.post_id==post.id))
                if not res.scalar_one_or_none():
                    # Fake the interaction time to match post time broadly (or today)
                    # Ideally, Real Stats uses created_at. We mock it to 'now' mostly, 
                    # but for 'Daily Active' it counts user activity. 
                    # If we want past activity, we need to manulaly set created_at if model allows.
                    # Model defines server_default=func.now(). We can override if passed explicitly?
                    # Let's try forcing it or just let it be now (Active Today).
                    # For demo, 'Active Today' is fine.
                    db.add(Rating(user_id=u.id, post_id=post.id, score=random.randint(3, 5)))
            
            # Random comments
            for _ in range(random.randint(0, 5)):
                u = random.choice(user_models)
                cmt = Comment(user_id=u.id, post_id=post.id, content="Great post! 👍")
                db.add(cmt)

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
