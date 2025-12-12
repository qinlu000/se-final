# Role: Senior Frontend Developer (UniApp/Vue3)

## Task
Implement the **Full AI Assistant Feature Suite** for the frontend, connecting to the now-ready Backend API.

## Context
- **Backend API**: `POST /ai/assistant` is ready. 
  - Params: `content`, `mode` (summary/polish/emojify/etc.), `tone`, `target_lang`.
  - Response: `status`, `summary`, `suggestions`, `tags`, `translated_content`, `vibe`.
- **Design System**: Neu-Brutalism (Use `rpx`, `var(--c-yellow)`, `var(--border-thick)`, `var(--shadow-hard)`).

## Implementation Requirements

### 1. API Service (`mini-program/api/ai.js`)
- **Action**: Create new file.
- **Function**: `export const askAI = (data) => request.post('/ai/assistant', data)`.
- **Note**: Ensure robust error handling (toast on failure).

### 2. Consumer Features (Feed)

#### A. Intelligence Card (`mini-program/components/AICard.vue`)
- **Action**: Create new file.
- **UI Design**:
  - **Container**: Glassmorphism (`backdrop-filter: blur(10px)`, `background: rgba(255,255,255,0.8)`), heavy border.
  - **Header**:
    - Left: "✨ AI 解读"
    - Right (Vibe): Show `vibe.emoji` + `vibe.label`. Background color = `vibe.color`.
  - **Content Area**:
    - **Tab Switcher**: [ 摘要 ] [ 翻译 ].
    - **Summary View**: Typewriter text effect.
    - **Translate View**: Show `translated_content`. If missing, show "Translating..." and call API with `mode='translate'`.
  - **Tags**: Yellow chips (`var(--c-yellow)`).
  - **Suggestions**: Clickable chips. On click -> Emit `reply` event.

#### B. Post Integration (`mini-program/components/PostCard.vue`)
- **Action**: Modify existing file.
- **UI**: Add "🤖 AI" button in the action bar (next to Comment).
- **Logic**:
  - Click -> Toggle `showAI`.
  - If `showAI` is true -> Render `<AICard :content="post.content" />` below the content.
  - Pass `post.content` to AICard.
  - Handle `@reply` event from AICard -> Fill comment box (if applicable) or copy to clipboard.

### 3. Creator Features (Upload)

#### C. Magic Compose (`mini-program/pages/upload/upload.vue`)
- **Action**: Modify existing file.
- **UI**: Add a floating or toolbar button: "🪄 AI 帮写" (Magic Wand).
- **Logic**:
  - Click -> Show ActionSheet: `['润色 (Polish)', '加 Emoji (Emojify)', '起标题 (Title)']`.
  - Selection -> Call `askAI({ mode: ... })` with current textarea content.
  - **Handling Results**:
    - `polish/emojify`: Replace textarea content with `res.summary`.
    - `title`: Show a modal/list of `res.suggestions`. User clicks one -> Append to textarea.

## Code Generation

Please generate the complete code for:
1. `mini-program/api/ai.js`
2. `mini-program/components/AICard.vue` (New)
3. `mini-program/components/PostCard.vue` (Updated)
4. `mini-program/pages/upload/upload.vue` (Updated)

**Style Constraint**: All CSS must strict follow the project's **Neu-Brutalism** theme. Use `rpx` for all dimensions.
