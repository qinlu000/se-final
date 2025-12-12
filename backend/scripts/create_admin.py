import asyncio
import sys
import os
from dotenv import load_dotenv

load_dotenv()

# Add the parent directory to sys.path to allow importing app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import AsyncSessionLocal
from app.models import User
from app.core.security import hash_password
from sqlalchemy import select

async def create_admin(username, password):
    # Ensure tables exist
    from app.core.database import engine, Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        # Check if user exists
        result = await db.execute(select(User).where(User.username == username))
        user = result.scalar_one_or_none()
        
        if user:
            print(f"User {username} already exists. Updating to admin...")
            user.is_admin = True
            user.password_hash = hash_password(password)
        else:
            print(f"Creating new admin user {username}...")
            user = User(
                username=username,
                password_hash=hash_password(password),
                nickname="Super Admin",
                is_admin=True
            )
            db.add(user)
        
        await db.commit()
        print(f"Successfully configured {username} as admin.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python create_admin.py <username> <password>")
        sys.exit(1)
    
    username = sys.argv[1]
    password = sys.argv[2]
    
    asyncio.run(create_admin(username, password))
