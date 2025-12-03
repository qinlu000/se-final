# System Architecture Design

## 1. System Overview

The **Multimedia Social Platform** is a full-stack application designed to mimic core social media functionalities (like WeChat Moments). It adopts a **Client-Server** architecture with a clear separation of concerns:

*   **Backend**: A RESTful API service built with **FastAPI**, handling business logic, data persistence, and authentication.
*   **Admin Web**: A Single Page Application (SPA) built with **Vue 3**, serving as the management dashboard.
*   **Mini Program**: A mobile client built with **Uni-app**, providing the end-user experience.

---

## 2. Technology Stack & Rationale

### 2.1 Backend: Python + FastAPI
*   **Selection**: FastAPI is chosen over Django/Flask for its high performance (ASGI), automatic OpenAPI (Swagger) documentation generation, and native Python type hinting support.
*   **Key Libraries**:
    *   `SQLAlchemy`: ORM for database interactions, ensuring database agnosticism.
    *   `Pydantic`: Data validation and settings management.
    *   `Passlib` + `PyJWT`: Secure password hashing (bcrypt) and stateless authentication.

### 2.2 Admin Frontend: Vue 3 + Vite + Element Plus
*   **Selection**: Vue 3 offers a reactive and composable component model. Vite provides lightning-fast build times. Element Plus is the industry standard UI library for Vue-based admin panels.
*   **Key Features**:
    *   `Vue Router`: Client-side routing.
    *   `Axios`: HTTP client with interceptors for token management.
    *   `ECharts`: For data visualization in the dashboard.

### 2.3 Mobile Client: Uni-app
*   **Selection**: Uni-app allows writing Vue.js code that compiles to multiple platforms (WeChat Mini Program, H5, iOS, Android). This significantly reduces development cost compared to native development.
*   **Key Features**:
    *   Cross-platform compatibility.
    *   Native-like performance for list rendering.

---

## 3. System Architecture Diagram

```mermaid
graph TD
    subgraph "Client Layer"
        MP[Mini Program (Uni-app)]
        Web[Admin Dashboard (Vue 3)]
    end

    subgraph "Gateway / Network"
        HTTP[HTTP/HTTPS]
    end

    subgraph "Service Layer (FastAPI)"
        Auth[Auth Service]
        User[User Service]
        Post[Post/Content Service]
        Inter[Interaction Service]
        Stat[Statistics Service]
    end

    subgraph "Data Layer"
        DB[(PostgreSQL/SQLite)]
        FS[File System (Media Storage)]
    end

    MP -->|REST API| HTTP
    Web -->|REST API| HTTP
    HTTP --> Auth
    HTTP --> User
    HTTP --> Post
    HTTP --> Inter
    HTTP --> Stat

    Auth --> DB
    User --> DB
    Post --> DB
    Post --> FS
    Inter --> DB
    Stat --> DB
```

---

## 4. Core Module Design

### 4.1 Authentication & Security
*   **Mechanism**: OAuth2 with Password Flow (Bearer Token).
*   **Flow**:
    1.  Client sends `username` + `password`.
    2.  Server verifies hash, issues `access_token` (JWT).
    3.  Client stores token (Storage/LocalStorage) and attaches it to `Authorization` header for subsequent requests.
*   **Security**:
    *   Passwords are hashed using `bcrypt` before storage.
    *   CORS middleware configured to allow trusted origins.

### 4.2 Content Management (Feed)
*   **Data Model**: `Post` entity contains `content` (text) and `media_urls` (JSON array).
*   **Optimization**:
    *   **Pagination**: API uses `skip` and `limit` to support infinite scrolling on the client.
    *   **Eager Loading**: `SQLAlchemy`'s `selectinload` is used to fetch related `User` and `Comments` data in a single query to avoid N+1 problems.

### 4.3 Interaction System
*   **Optimistic UI**: The frontend (Mini Program) updates the UI *immediately* upon user action (Like/Follow) without waiting for the server response. If the API call fails, the UI reverts. This ensures a snappy user experience.
*   **Persistence**: All interactions (Likes, Comments, Follows) are stored in relational tables (`ratings`, `comments`, `follows`) with foreign keys ensuring referential integrity.

---

## 5. Directory Structure & Responsibilities

### Backend (`/backend`)
*   `app/core`: Global configurations, security utilities, database connection factory.
*   `app/models`: SQLAlchemy ORM models (Database schema definition).
*   `app/schemas`: Pydantic models (Request/Response validation).
*   `app/routers`: API route handlers (Controllers).
*   `static/uploads`: Local storage for user-uploaded media.

### Admin Web (`/admin-web`)
*   `src/api.ts`: Centralized API configuration and interceptors.
*   `src/views`: Page components (Login, Dashboard, Users, Posts).
*   `src/layout`: Common layout wrapper (Sidebar, Header).

### Mini Program (`/mini-program`)
*   `pages/`: Screen components (Index, Profile, Upload).
*   `components/`: Reusable UI widgets (`PostCard`, `MediaGrid`).
*   `utils/request.js`: Encapsulated `uni.request` with token handling.

---

## 6. Future Scalability Considerations

1.  **Database**: Currently using SQLite for dev simplicity. Can be switched to PostgreSQL by changing the `DATABASE_URL` env var.
2.  **Storage**: Currently using local filesystem. Can be refactored to use S3/MinIO by updating the `upload` router.
3.  **Caching**: Redis can be introduced to cache the Feed stream for high-concurrency scenarios.
4.  **AI**: The architecture supports adding a background worker (e.g., Celery) to handle heavy AI tasks (content moderation, sentiment analysis) without blocking the main API thread.
