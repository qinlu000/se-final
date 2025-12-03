from typing import List, Optional

from fastapi import APIRouter, Depends, Header, HTTPException, Query, Response, status
from jose import JWTError, jwt
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.core.llm import analyze_content
from app.core.sensitive import check_sensitive_words
from app.core.security import ALGORITHM, SECRET_KEY
from app.models import Comment, Follow, Post, Rating, Tag, User
from app.routers.auth import get_current_user
from app.schemas import PostCreate, PostDetail, PostOut

router = APIRouter(prefix="/posts", tags=["posts"])


async def _get_following_ids(db: AsyncSession, user_id: int) -> set[int]:
    result = await db.execute(select(Follow.followed_id).where(Follow.follower_id == user_id))
    return {row[0] for row in result.all()}


async def get_current_user_optional(
    db: AsyncSession = Depends(get_db), authorization: Optional[str] = Header(default=None)
) -> Optional[User]:
    if not authorization:
        return None
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None
    token = parts[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub = payload.get("sub")
        if sub is None:
            return None
        user_id = int(sub)
    except (JWTError, ValueError):
        return None
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def _get_post_with_relations(db: AsyncSession, post_id: int) -> Optional[Post]:
    result = await db.execute(
        select(Post)
        .options(
            selectinload(Post.user),
            selectinload(Post.tags),
            selectinload(Post.comments).selectinload(Comment.user),
            selectinload(Post.ratings).selectinload(Rating.user),
        )
        .where(Post.id == post_id)
    )
    return result.scalar_one_or_none()


@router.post("", response_model=PostDetail, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_in: PostCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)
) -> PostDetail:
    check_sensitive_words(post_in.content)
    inferred_tags = await analyze_content(post_in.content)

    tag_names = [tag.strip() for tag in (post_in.tags or []) if tag.strip()]
    if inferred_tags:
        tag_names.extend(inferred_tags)
    existing_tags = []
    if tag_names:
        result = await db.execute(select(Tag).where(Tag.name.in_(tag_names)))
        existing_tags = result.scalars().all()
        existing_names = {t.name for t in existing_tags}
        for name in set(tag_names) - existing_names:
            new_tag = Tag(name=name)
            db.add(new_tag)
            existing_tags.append(new_tag)
        await db.flush()

    post = Post(
        user_id=current_user.id,
        content=post_in.content,
        media_type=post_in.media_type,
        media_urls=post_in.media_urls,
        tags=existing_tags,
    )
    db.add(post)
    await db.commit()

    post_with_relations = await _get_post_with_relations(db, post.id)
    if not post_with_relations:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to load post")

    average_rating = None
    if post_with_relations.ratings:
        average_rating = sum(r.score for r in post_with_relations.ratings) / len(post_with_relations.ratings)

    return PostDetail.from_orm(post_with_relations).copy(
        update={
            "comment_count": len(post_with_relations.comments),
            "average_rating": average_rating,
        }
    )


@router.get("", response_model=List[PostOut])
async def list_posts(
    tag: Optional[str] = None,
    user_id: Optional[int] = None,
    media_type: Optional[str] = None,
    filter: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
) -> List[PostOut]:
    query = (
        select(Post)
        .options(
            selectinload(Post.user),
            selectinload(Post.tags),
            selectinload(Post.comments).selectinload(Comment.user)
        )
        .order_by(Post.created_at.desc())
        .offset(skip)
        .limit(limit)
    )

    if tag:
        query = query.join(Post.tags).where(Tag.name == tag)
    if filter == "following":
        if not current_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Login required for following feed")
        query = query.join(Follow, Post.user_id == Follow.followed_id).where(
            Follow.follower_id == current_user.id
        )
    if user_id:
        query = query.where(Post.user_id == user_id)
    if media_type:
        query = query.where(Post.media_type == media_type)

    result = await db.execute(query)
    posts = result.scalars().unique().all()
    if not posts:
        return []

    post_ids = [p.id for p in posts]

    following_ids: set[int] = set()
    if current_user:
        following_ids = await _get_following_ids(db, current_user.id)

    comment_counts_result = await db.execute(
        select(Comment.post_id, func.count(Comment.id)).where(Comment.post_id.in_(post_ids)).group_by(Comment.post_id)
    )
    comment_counts = {post_id: count for post_id, count in comment_counts_result.all()}

    rating_result = await db.execute(
        select(Rating.post_id, func.avg(Rating.score)).where(Rating.post_id.in_(post_ids)).group_by(Rating.post_id)
    )
    avg_ratings = {post_id: float(avg) for post_id, avg in rating_result.all()}

    # Get user's liked posts (ratings > 0)
    liked_post_ids: set[int] = set()
    if current_user:
        liked_result = await db.execute(
            select(Rating.post_id).where(
                Rating.user_id == current_user.id,
                Rating.post_id.in_(post_ids),
                Rating.score > 0
            )
        )
        liked_post_ids = {row[0] for row in liked_result.all()}

    post_out_list: List[PostOut] = []
    for post in posts:
        post_out = PostOut.from_orm(post).copy(
            update={
                "comment_count": comment_counts.get(post.id, 0),
                "average_rating": avg_ratings.get(post.id),
                "is_following": post.user_id in following_ids if current_user else False,
                "is_liked": post.id in liked_post_ids,
            }
        )
        post_out_list.append(post_out)

    return post_out_list


@router.get("/{post_id}", response_model=PostDetail)
async def get_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
) -> PostDetail:
    post = await _get_post_with_relations(db, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    following_ids: set[int] = set()
    if current_user:
        following_ids = await _get_following_ids(db, current_user.id)

    average_rating = None
    if post.ratings:
        average_rating = sum(r.score for r in post.ratings) / len(post.ratings)

    return PostDetail.from_orm(post).copy(
        update={
            "comment_count": len(post.comments),
            "average_rating": average_rating,
            "is_following": bool(current_user and post.user_id in following_ids),
        }
    )


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)
) -> Response:
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    if not (current_user.is_admin or post.user_id == current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this post")

    await db.delete(post)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
