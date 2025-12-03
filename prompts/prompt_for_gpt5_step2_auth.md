# Prompt for AI Developer (GPT-5) - Step 2: Authentication

**Context:**
We have successfully implemented the **Database Connection** and **SQLAlchemy Models** (User, Post, etc.).
Now we need to secure the API.

**Your Task:**
Implement the **Authentication System** using JWT (JSON Web Tokens).

**Requirements:**
1.  **Security Utils** (`backend/app/core/security.py`):
    -   Function to hash passwords (using `passlib`).
    -   Function to verify passwords.
    -   Function to create access tokens (JWT).
2.  **Auth Router** (`backend/app/routers/auth.py`):
    -   `POST /auth/register`: Create a new user. Input: `username`, `password`, `nickname`.
    -   `POST /auth/token`: Login endpoint (OAuth2 compatible). Input: `username`, `password`. Returns JWT token.
    -   `GET /auth/me`: Return current user info. Dependency: `get_current_user`.
3.  **Main Application**:
    -   Register the `auth` router in `backend/main.py`.

**Technical Details:**
-   Use `python-jose` for JWT.
-   Use `passlib[bcrypt]` for hashing.
-   Use `fastapi.security.OAuth2PasswordBearer` for the token dependency.
-   Token expiration should be 30 minutes (configurable via env).

Please generate the code for `security.py`, `auth.py`, and the updated `main.py`.
