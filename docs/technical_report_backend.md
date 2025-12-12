# Backend Technical Report & Implementation Details

## 1. Core Framework Architecture
The Backend utilizes **FastAPI** with **SQLAlchemy 2.0 (Async)**. This combination provides a modern, type-safe, and high-performance foundation.

### 1.1 Application Factory Pattern
We use a factory pattern in `main.py` to ensure testability and cleaner dependency management.
```python
# Pseudo-code logic
app = FastAPI(title="Moments API")
app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(assistant.router)
```

## 2. Detailed Module Implementation

### 2.1 Authentication & Security
- **Algorithm**: `OAuth2PasswordBearer` flow.
- **Hashing**: `bcrypt` (Salted).
- **Token**: JWT (HS256). Payload includes `sub` (username) and `exp` (expiration).

**Code Snippet: Password Verification**
```python
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
```

### 2.2 Data Access Layer (ORM)
We use SQLAlchemy's AsyncSession to prevent blocking the event loop during database I/O.

**Optimization: Eager Loading**
To solve the N+1 query problem when fetching feeds (getting User info for each Post), we use `joinedload`.
```python
# routers/posts.py logic
stmt = select(Post).options(joinedload(Post.user)).order_by(Post.created_at.desc())
result = await db.execute(stmt)
posts = result.scalars().all()
```
*Impact*: Reduces DB queries from `1 + N` (where N is page size) to `1` query per request.

### 2.3 Rate Limiting Algorithm (Token Bucket)
Implemented in `routers/assistant.py`.
- **Logic**:
    - Each IP has a bucket of tokens (Max 10).
    - Tokens refill at a rate of 10 per minute.
    - Each request consumes 1 token.
- **Implementation**:
    - Dictionary `_RATE_LIMIT[ip] = [timestamp1, timestamp2, ...]`
    - Clean up timestamps older than 60s.
    - If `len(timestamps) >= LIMIT`: Raise 429.

## 3. Database Specification

### 3.1 Schema Definition (DDL)
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    content TEXT NOT NULL,
    media_urls JSONB, -- Stores ["http://...", "http://..."]
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_posts_user_id ON posts(user_id);
CREATE INDEX idx_posts_created_at ON posts(created_at DESC);
```

### 3.2 Performance Tuning
- **Indexes**: Added on `user_id` (for "My Posts" queries) and `created_at` (for Feed sorting).
- **JSONB**: Used for `media_urls` to allow flexible storage of 0-9 image URLs without a separate join table, simplifying "Read" queries.

## 4. API Interface Specification (OpenAPI)
FastAPI automatically generates `openapi.json`.
- **Swagger UI**: Available at `/docs`.
- **Schema Validation**: Inputs are validated against Pydantic models (e.g., `PostCreate`), ensuring `content` is not empty and `media_urls` is a valid list.

## 5. Security Checklist
- [x] **SQL Injection**: Prevented via ORM.
- [x] **XSS**: Inputs are sanitized.
- [x] **Rate Limiting**: Applied to expensive endpoints (`/ai/assistant`).
- [x] **CORS**: Restricted to allowed origins in Production.
