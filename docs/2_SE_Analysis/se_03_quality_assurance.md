# Software Engineering Analysis 03: Quality Assurance & Testing

## 1. Testing Strategy: The Testing Pyramid

We employ a pragmatic testing strategy suitable for a rapid-development prototype.

### 1.1 Unit Testing (Backend)
*   **Tools**: `pytest`, `httpx` (for AsyncClient).
*   **Scope**:
    *   **Pydantic Models**: Ensure validation rules work (e.g., email format, empty strings).
    *   **Utility Functions**: Test helper logic (e.g., `verify_password`, `check_rate_limit`).
*   **Coverage**: Focus on "Business Critical" logic (Auth, AI integration).

### 1.2 Integration Testing (Backend API)
*   **Tools**: `TestClient` (FastAPI).
*   **Scope**:
    *   Test full API endpoints (`POST /login`, `GET /posts`).
    *   Verify Database interactions (CREATE, READ).
    *   *Example*: Creating a post and immediately fetching the feed to ensure it appears.

### 1.3 End-to-End (E2E) / Manual Testing (Frontend)
*   **Tools**: HBuilderX Simulator, Chrome DevTools.
*   **Scope**:
    *   **UI Workflows**: User Login -> Post -> Check Feed.
    *   **Cross-Platform Verification**: Checking layout on specific "dimensions" (iPhone 14 vs Desktop).
    *   **Visual Regression**: Manually verifying "Neu-Brutalism" styles (borders, shadows) render correctly.

## 2. Static Code Analysis (Linting)

### 2.1 Backend
*   **Type Hinting**: Extensive use of Python Type Hints (`def foo(x: int) -> str`) empowers IDEs (VS Code) to catch type errors before runtime.
*   **Formatter**: Implied usage of standard formatters (like `black` or `autopep8`) for consistent style.

### 2.2 Frontend
*   **ESLint/Prettier**: Vue components follow standard indentation and templating rules.
*   **VLS (Vue Language Server)**: Provides real-time error checking in `.vue` files (e.g., accessing undefined props).

## 3. Performance Testing Analysis

### 3.1 Backend Bottlenecks
*   **Database**: The `JOIN` operations for fetching User profiles with Posts are the primary bottleneck.
    *   *Mitigation*: Implemented `joinedload` strategy in SQLAlchemy to optimize to a single query.
*   **AI Service**: High latency (2s+) from external LLM.
    *   *Mitigation*: Implemented Token Bucket Rate Limiting to prevent system overload and abuse.

### 3.2 Frontend Performance
*   **Asset Loading**: Large images/videos can block the main thread.
    *   *Optimization*: Use `lazy-load` and thumbnails.
*   **Bundle Size**: UniApp compilation optimizes unused modules (Tree Shaking).

## 4. Bug Tracking & Resolution Process
*   **Discovery**: Bugs identified during "Verification" phase of tasks (e.g., `401 Unauthorized` loop).
*   **Triage**: Impact assessment (Critical/Minor).
*   **Resolution**:
    1.  Reproduce in Dev environment.
    2.  Write regression test (if applicable).
    3.  Fix code.
    4.  Verify fix.
*   *Case Study*: The "AI 500 Error" was tracked to an improperly handled `None` return in `tags`. Fixed by defaulting to `[]` in the Pydantic model.
