# Prompt for AI Developer (GPT-5) - Step 7: Bonus Features

**Context:**
The core project (Backend, Admin Web, Mini Program) is fully functional.
Now we want to add some **Bonus Features** to impress the users.

**Your Task:**
Implement the following bonus features in the **Backend**.

**Requirements:**

1.  **Friend System (Follow/Unfollow)**:
    -   **Models**: Add `Follow` model (`follower_id`, `followed_id`).
    -   **API** (`backend/app/routers/friends.py`):
        -   `POST /users/{id}/follow`: Follow a user.
        -   `DELETE /users/{id}/follow`: Unfollow.
        -   `GET /users/{id}/followers`: List followers.
        -   `GET /users/{id}/following`: List following.
    -   **Feed Update**: Update `GET /posts` to support `filter=following` (only show posts from followed users).

2.  **Sensitive Word Filtering**:
    -   **Middleware**: Create a dependency or utility function `check_sensitive_words(text: str)`.
    -   **Integration**: Apply this check in `POST /posts` and `POST /comments`. If sensitive word found, reject with 400.
    -   **Word List**: Just use a simple hardcoded list for now (e.g., `["bad", "evil"]`).

3.  **LLM Integration (Content Analysis)**:
    -   **Goal**: Automatically tag posts based on content.
    -   **Implementation**:
        -   Create `backend/app/core/llm.py`.
        -   Mock function `analyze_content(text: str) -> List[str]`. (In real world this would call OpenAI/Gemini).
        -   Call this asynchronously in `POST /posts` to append tags.

**Technical Details:**
-   Update `main.py` to include new routers.
-   Ensure database migrations (or `create_all`) handle the new `Follow` model.

Please generate the code for `models/follow.py`, `routers/friends.py`, `core/sensitive.py`, `core/llm.py`, and updated `routers/posts.py` & `main.py`.
