# Prompt for AI Developer (GPT-5) - Step 3: CRUD API Endpoints

**Context:**
We have the **Database Models** and **Authentication System** (JWT) ready.
Now we need to implement the core business logic and API endpoints.

**Your Task:**
Implement the **CRUD API Endpoints** for Posts, Comments, Ratings, and File Uploads.

**Requirements:**

1.  **File Upload (`backend/app/routers/upload.py`)**:
    -   `POST /upload`: Accept a file (image/video).
    -   Save it to `backend/static/uploads/`.
    -   Return the accessible URL (e.g., `/static/uploads/filename.jpg`).
    -   Ensure unique filenames (use UUID).

2.  **Posts (`backend/app/routers/posts.py`)**:
    -   `POST /posts`: Create a post. Input: `content`, `media_type`, `media_urls` (list of strings), `tags` (list of strings).
        -   *Logic*: Create `Post`, handle `Tags` (create if not exists), link `PostTag`.
    -   `GET /posts`: List posts.
        -   *Filters*: `tag` (optional), `user_id` (optional).
        -   *Pagination*: `skip`, `limit`.
        -   *Response*: Include user info, tags, comment count, average rating.
    -   `GET /posts/{id}`: Get single post detail (with comments and ratings).
    -   `DELETE /posts/{id}`: Delete post. *Auth*: Only owner or Admin.

3.  **Interactions (`backend/app/routers/interactions.py`)**:
    -   `POST /posts/{id}/comments`: Add comment.
    -   `DELETE /comments/{id}`: Delete comment. *Auth*: Owner, Post Owner, or Admin.
    -   `POST /posts/{id}/rate`: Rate a post (1-5). If already rated, update score.

4.  **Main Application**:
    -   Register new routers in `backend/main.py`.
    -   Mount `StaticFiles` to serve `/static` directory.

**Technical Details:**
-   Use `SQLAlchemy` async session.
-   Use `Pydantic` schemas for validation (`backend/app/schemas.py` - create this if needed).
-   Ensure `current_user` dependency is used for protected routes.

Please generate the code for `upload.py`, `posts.py`, `interactions.py`, `schemas.py` and the updated `main.py`.
