# Prompt for AI Developer (GPT-5) - Step 4: Admin Web (Vue 3)

**Context:**
The Backend API is fully implemented (Auth + CRUD).
Now we need to build the **Admin Dashboard** for administrators to manage users and content.

**Your Task:**
Implement the **Admin Web** using Vue 3, Vite, and Element Plus.

**Requirements:**

1.  **API Client (`admin-web/src/api.ts`)**:
    -   Setup `axios` instance with `baseURL` (e.g., `http://localhost:8000`).
    -   Add interceptor to inject `Authorization: Bearer <token>` header from localStorage.

2.  **Views**:
    -   **Login** (`src/views/Login.vue`):
        -   Form: Username, Password.
        -   Action: Call `/auth/token`, save token to localStorage, redirect to Dashboard.
    -   **Dashboard Layout** (`src/layout/Layout.vue`):
        -   Sidebar: "User Management", "Content Management".
        -   Header: "Logout" button.
    -   **User Management** (`src/views/Users.vue`):
        -   Table: ID, Username, Nickname, Admin Status, Created At.
        -   Action: "Delete" button (Call `DELETE /users/{id}` - *Note: You might need to add this endpoint to backend if not exists, or just mock it for now*).
    -   **Content Management** (`src/views/Posts.vue`):
        -   Table: ID, User, Content (truncate), Media Type, Created At.
        -   Action: "Delete" button (Call `DELETE /posts/{id}`).

3.  **Router (`src/router/index.ts`)**:
    -   Define routes: `/login`, `/` (Dashboard) -> children: `/users`, `/posts`.
    -   Add Navigation Guard: Redirect to `/login` if no token.

**Technical Details:**
-   Use `<script setup lang="ts">`.
-   Use `Element Plus` components (`el-table`, `el-form`, `el-menu`, etc.).

Please generate the code for `api.ts`, `router/index.ts`, `views/Login.vue`, `layout/Layout.vue`, `views/Users.vue`, and `views/Posts.vue`.
