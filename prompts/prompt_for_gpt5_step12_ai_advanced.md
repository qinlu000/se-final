# Role: Senior Full-Stack Developer (FastAPI + Vue3/UniApp)

## Task
Implement **Advanced AI Features** (Magic Compose, Translation, Vibe Check) for the Social Media App, building upon the existing AI Assistant foundation.

## Context
- **Docs**: `docs/ai_assistant_design.md` (Updated with new specs).
- **Current Backend**: 
  - `schemas.py`: `AssistantRequest` has `mode`.
  - `routers/assistant.py`: Endpoint `/ai/assistant`.
  - `core/llm.py`: wrappers for OpenRouter.
- **Current Frontend**: 
  - `api/ai.js`.
  - `components/AICard.vue`.
  - `pages/upload/upload.vue`.

## Requirements

### 1. Backend Updates (`backend/`)

#### A. Schema Update (`app/schemas.py`)
- Update `AssistantRequest`:
  - `mode`: Expand Literal to include `"polish", "emojify", "title", "translate", "vibe"`.
  - `target_lang`: Optional[str] (default 'zh').
- Update `AssistantResponse`:
  - `translated_content`: Optional[str].
  - `vibe`: Optional[Dict] (structure: `{ "label": str, "score": float, "emoji": str, "color": str }`).

#### B. Logic Update (`app/core/llm.py` & `routers/assistant.py`)
- **Magic Compose** (Creator Modes):
  - `polish`: Rewrite content to be more fluent/correct.
  - `emojify`: Insert relevant emojis into the text.
  - `title`: Generate 3 catchy titles (return in `suggestions`).
- **Consumer Modes**:
  - `translate`: Translate content to `target_lang`.
  - `vibe`: Analyze sentiment. Return emotion label, emoji (🎉/👿/🌧️), and color code.
- **Prompt Engineering**:
  - Update `system_prompt` to handle these new modes instructions.
  - Ensure `response_format={"type": "json_object"}` matches the new schema.

### 2. Frontend Updates (`mini-program/`)

#### A. Magic Compose (`pages/upload/upload.vue`)
- Add a **"🪄 AI 帮写"** (Magic Wand) button near importance creation area.
- Click opens an ActionSheet: `["润色", "加Emoji", "生成标题"]`.
- Call API with `mode=polish/emojify/title`.
- Use `uni.showLoading`. On success, update the textarea value (or show titles for selection).

#### B. Vibe Check & Translate (`components/AICard.vue`)
- **Vibe UI**: 
  - Display the Vibe Emoji (e.g. 🎉) prominently in the card header.
  - Tint the card background/border using the Vibe Color (e.g. `var(--c-yellow)` vs `var(--c-red)`).
- **Translate UI**:
  - Add a "翻译" (Translate) button or tab.
  - Click triggers API call `mode=translate`.
  - Display translated text below original summary.

## Code Generation

Please generate/update the following files:
1. `backend/app/schemas.py` (Update Request/Response)
2. `backend/app/core/llm.py` (Handle new modes)
3. `mini-program/api/ai.js` (Ensure flexible params)
4. `mini-program/pages/upload/upload.vue` (Add Magic Compose)
5. `mini-program/components/AICard.vue` (Add Vibe & Translate)

**Style Note**: Maintain the **Neu-Brutalism** design (thick borders, hard shadows) for the new UI elements.
