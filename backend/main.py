from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.database import Base, engine
from app.routers import (
    auth_router,
    friends_router,
    interactions_router,
    posts_router,
    stats_router,
    upload_router,
    users_router,
)

app = FastAPI(title="Multimedia Social Platform API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
async def on_startup() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def read_root():
    return {"message": "Welcome to the Multimedia Social Platform API"}


app.include_router(auth_router)
app.include_router(posts_router)
app.include_router(interactions_router)
app.include_router(upload_router)
app.include_router(users_router)
app.include_router(friends_router)
app.include_router(stats_router)
