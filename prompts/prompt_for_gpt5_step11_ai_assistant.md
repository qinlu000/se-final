# Role: Senior Full-Stack Developer (FastAPI + Vue3/UniApp)

## Task
Implement the **AI Assistant** feature (Twitter Grok-style) for our Social Media App, ensuring strict adherence to the existing **Neu-Brutalism** design system.

## Context

### 1. Project Architecture
- **Backend**: Python FastAPI with SQLAlchemy (Async).
  - Models: `app/models/` (User, Post with `media_type`).
  - Schemas: `app/schemas.py` (Pydantic models).
  - Auth: JWT Bearer.
- **Frontend**: UniApp (Vue 3 script setup) for Mini Program.
  - CSS Variables: `var(--c-yellow)`, `var(--c-bg)`, `var(--border-thick)`, `var(--shadow-hard)`.
  - Design Style: High contrast, thick borders, brutalist shadows, glassmorphism accents.

### 2. Design Spec (`docs/ai_assistant_design.md`)
- **Goal**: "Ask AI" button on feed cards to get Summary/Tags/Reply Suggestions.
- **LLM**: DeepSeek-V3 via OpenRouter (`core/llm.py`).
- **Safety**: Sensitive word filtering before/after LLM call.

## Implementation Steps

### Step 1: Backend Implementation (`backend/`)

1.  **`app/core/llm.py`**
    - Implement `ask_ai_assistant` using `AsyncOpenAI` client.
    - **Prompt Engineering**: System prompt must enforce JSON output: `{ "summary": "...", "tags": [...], "suggestions": [...] }`.
    - **Tone**: Support `friendly` | `professional` | `humorous`.

2.  **`app/routers/assistant.py`**
    - Endpoint: `POST /ai/assistant`
    - **Logic sequence**:
      1. Check Input Sensitive Words -> Return valid `AIResponse(status="sensitive")` if hit.
      2. Check Rate Limit (IP based, 10 req/min).
      3. Check Cache (SHA256 of content).
      4. Call LLM.
      5. Check Output Sensitive Words.
      6. Return Success.

3.  **`app/main.py`**
    - Register the router: `app.include_router(assistant.router)`.

### Step 2: Frontend Implementation (`mini-program/`)

1.  **`api/ai.js`**
    - Export `askAI({ content, features, tone })` wrapper around `uni.request`.

2.  **`components/AICard.vue` (New Component)**
    - **Design**: Glassmorphism card to appear *inside* the feed item.
    - **Style**:
      ```css
      .ai-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border: var(--border-thin);
        border-radius: 16rpx;
        padding: 24rpx;
        margin-top: 24rpx;
        animation: slideDown 0.3s ease-out;
      }
      .summary-text { font-family: monospace; color: #333; }
      .tag { background: var(--c-yellow); border: 2rpx solid #000; }
      ```
    - **Features**:
      - Typewriter effect for displaying the summary.
      - Clickable "Quick Reply" chips that emit `select-reply`.

3.  **`components/PostCard.vue`**
    - Add "🤖 AI解读" Action Button to the footer (consistent with Like/Comment buttons).
    - Logic:
      - Click -> state `aiLoading = true`.
      - Call API.
      - Success -> `aiLoading = false`, show `<AICard />`.
      - Error -> Toast message.

## Code Generation

Please generate the full code for:
1. `backend/app/core/llm.py`
2. `backend/app/routers/assistant.py`
3. `backend/app/main.py` (Modification)
4. `mini-program/api/ai.js`
5. `mini-program/components/AICard.vue`
6. `mini-program/components/PostCard.vue` (Modification)

**CRITICAL**: Ensure the Frontend code strictly uses `rpx` for units and follows the `var(--c-yellow)` / `var(--border-thick)` styling theme found in `pages/index/index.vue`.
