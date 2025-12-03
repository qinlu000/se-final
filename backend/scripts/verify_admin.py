import asyncio
import sys
import os

# Add parent dir to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import AsyncSessionLocal
from app.models import User
from sqlalchemy import select

async def verify_admin():
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(User).where(User.username == "admin"))
        user = result.scalar_one_or_none()
        
        if user:
            print(f"User found: {user.username}")
            print(f"Is Admin: {user.is_admin}")
            print(f"Password Hash: {user.password_hash}")
        else:
            print("User 'admin' NOT FOUND")

if __name__ == "__main__":
    asyncio.run(verify_admin())
