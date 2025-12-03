# Prompt for AI Developer (GPT-5) - Step 5: User Management API

**Context:**
The **Admin Web** has been implemented, but the **User Management** page (`Users.vue`) relies on API endpoints that are currently missing in the backend.

**Your Task:**
Implement the **User Management API** in the backend.

**Requirements:**

1.  **Users Router (`backend/app/routers/users.py`)**:
    -   `GET /users`: List all users.
        -   *Response*: List of users (id, username, nickname, is_admin, created_at).
        -   *Auth*: Admin only (`current_user.is_admin` must be True).
    -   `DELETE /users/{id}`: Delete a user.
        -   *Auth*: Admin only.
        -   *Logic*: Delete user from DB (Cascade will handle posts/comments).

2.  **Main Application**:
    -   Register the new `users_router` in `backend/main.py`.

**Technical Details:**
-   Use `SQLAlchemy` async session.
-   Ensure strict permission checks (Admin only).

Please generate the code for `users.py` and the updated `main.py`.
