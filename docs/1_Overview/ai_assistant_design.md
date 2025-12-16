# AI Assistant Feature Design

## Goal
- Provide a lightweight “Ask AI” helper (Twitter/X style) to summarize a post and suggest tags/replies without blocking the user flow.
- Keep compute cheap and safe by using deterministic mock logic that can be swapped for a real LLM later.

## Scope (v1)
- Surface: Mini Program feed cards show an “AI解读” entry that returns a short summary + tag suggestions for that post’s text.
- **[NEW] Magic Compose**: Helper in `Upload` page to polish text, add emojis, or generate titles.
- **[NEW] Translation**: Translate feed content to user's language.
- **[NEW] Vibe Check**: Visualize emotion with color/emoji in AI card.
- API: `POST /ai/assistant` with expanded modes.
- Safety: Input and output both run through sensitive-word check.
- Auth: Optional; prefer signed-in users but allow anonymous for demo.

## Non-Goals (v1)
- No real LLM calls or streaming responses.
- No long-term conversation memory.
- No per-user quotas dashboard (manual rate limiting only).

## API Contract
- **Endpoint:** `POST /ai/assistant`
- **Request body:**
  - `content` (string, required): text to analyze.
  - `mode` (enum): 
    - Consumer: `summary` | `reply` | `tags` | `translate` | `vibe`
    - Creator: `polish` | `emojify` | `title`
  - `tone` (string enum): `friendly` | `professional` | `humorous` (default `friendly`).
  - `target_lang` (string, optional): for `translate` mode (default "zh").
- **Response:**
  - `status` (string): `success` | `sensitive` | `error`.
  - `summary` (string | null): concise TL;DR or Polished Text.
  - `translated_content` (string | null): result for `translate` mode.
  - `vibe` (object | null): `{ score: -1~1, label: "happy", emoji: "🎉", color: "yellow" }`.
  - `suggestions` (string[]): candidate replies or titles.
  - `tags` (string[]): inferred tags.
- **Errors:**
  - Return 200 with `status="sensitive"` if content hits safety filters (friendly error handling).
  - 400 on invalid input, 500 on internal errors.

## Backend Design
- New router `routers/assistant.py` (`/ai/assistant`, tag `ai`).
- Reuse `check_sensitive_words` on input; sanitize output by trimming length.
- Heuristics:
  - `summary`: take key sentences/keywords, clamp to ~120 chars.
  - `tags`: reuse `analyze_content` keyword detector.
  - `reply`: template-based candidate replies influenced by `tone`.
- **Caching**: Compute SHA-256 of `content` + `features` + `tone` to cache results (LRU, short TTL) to save compute.
- Optional auth: attempt bearer token decode; proceed anonymously if absent.
- Extensibility: `core/llm.py` gains a helper that can be swapped with a real LLM call.

## Frontend Design (Mini Program)
- Add an “AI解读” action pill on each feed card.
- On tap: call `/ai/assistant` with `mode=summary` (includes vibe check).
- **Vibe Check**: Show dynamic emoji/color background in the AI card header based on sentiment.
- **Translate**: Tab/Button in AI card to toggle translation.

### Frontend Design (Upload Page)
- **Magic Wand Button**: In the text input area.
- Options: "🪄 润色", "🔥 加Emoji", "📰 生成标题".
- Result: Directly replace or append to the input box.

## Safety & Limits
- Sensitive-word check before processing; drop response if summary/suggestions are empty.
- Client debounce: disable button while loading.
- **Rate Limiting (v1)**: Simple IP-based or UserID-based throttle (e.g., 10 req/min) to prevent abuse of the mock endpoint.
- (Future) add server-side rate limiting and output filtering once real LLM is wired.

## Rollout & Testing
- Manual check: ensure API returns deterministic data for sample posts.
- UI check: action pill works on feed cards, renders summary/tags with no layout break.
- Backward compatibility: no existing endpoints touched; new route added and optional.
