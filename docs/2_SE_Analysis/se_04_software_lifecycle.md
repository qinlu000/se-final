# Software Engineering Analysis 04: SDLC & Project Management

## 1. Software Development Lifecycle (SDLC) Model

This project follows an **Iterative and Incremental (Agile-like)** model.

### 1.1 Why Agile?
*   **Unclear Requirements**: Initial "Social App with AI" is broad. Features like "Vibe Check" or "Video Upload" were discovered/refined during development.
*   **Rapid Feedback**: The ability to view the Mini Program simulator immediately after code changes allows for tight feedback loops.

### 1.2 Iteration History
*   **Iteration 1 (MVP)**: Basic Auth, SQLite DB, Text Posting.
*   **Iteration 2 (frontend-polish)**: Neu-Brutalism UI implementation, Admin Dashboard.
*   **Iteration 3 (AI-Integration)**: LLM integration, "Magic Compose", backend migration to Async.
*   **Iteration 4 (Multimedia & Refinement)**: Video support, Tag system, Real Data stats.

## 2. Version Control Strategy (Git)

### 2.1 Workflow
*   **Single Trunk (Main branch)**: Due to the small team size (1-2 devs), we commit directly to `main` after local verification.
*   **Atomic Commits**: Commits are grouped by logical task (e.g., "Fix: AI rate limit bug", "Feat: Add Video Upload").

### 2.2 Dependency Management
*   **Backend**: `requirements.txt` locks library versions to ensure reproducibility.
*   **Frontend**: `package.json` & `package-lock.json` manage NPM dependencies clearly.

## 3. Configuration Management

### 3.1 Environment Variables (`.env`)
*   **Separation of Config and Code**: API Keys, DB URLs, and Secrets are strictly kept in `.env` and NOT committed to Git (via `.gitignore`).
    *   *SE Principle*: The "Twelve-Factor App" config principle.

## 4. Release Management
*   **Deployment Units**:
    *   **Backend**: Python process (Uvicorn).
    *   **Admin**: Static HTML/JS bundle (Dist).
    *   **Mini Program**: Proprietary package format (mp-weixin).
*   **Rollback Strategy**: Since the DB schema is managed via SQLAlchemy models, rollback involves reverting code and potentially manually adjusting DB schema if migrations aren't strictly versioned (a simplified approach for this prototype).
