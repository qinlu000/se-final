# Frontend Technical Report: UniApp Implementation

## 1. Project Organization

### 1.1 Component Hierarchy tree
Visualizing the parent-child relationships in the UI:
```
App.vue (Global Context)
├── Pages (Router Views)
│   ├── Index (Feed)
│   │   ├── PostCard (Repeater)
│   │   │   └── AICard (Conditional)
│   │   │       ├── VibeChip
│   │   │       ├── TypewriterText
│   │   │       └── TagChip
│   │   └── FloatingActionButton (Post)
│   ├── Upload (Form)
│   │   ├── ImagePicker / VideoPicker
│   │   ├── TagsInput
│   │   └── MagicWandButton (ActionSheet)
│   └── Profile
└── Utils
    └── Request Interceptor
```

## 2. "Neu-Brutalism" Design System Implementation

### 2.1 Design Philosophy
Neu-Brutalism combines the "raw" aesthetic of Brutalism (bold borders, default fonts) with modern "Neu" sensibilities (vibrant colors, smooth animations).

### 2.2 Technical Implementation (CSS Variables)
We treat Design Tokens as first-class citizens in `App.vue`.

| Variable | Value | Usage |
| :--- | :--- | :--- |
| `--c-yellow` | `#FFE600` | Primary Actions, Active States, Highlights |
| `--border-thick` | `4rpx solid #000` | Card definitions, Buttons (Distinctive look) |
| `--shadow-hard` | `6rpx 6rpx 0 #000` | Depth perception (Pop-out effect) |

**Sample CSS Component:**
```css
/* Example: A neurological button */
.neu-btn {
  background: var(--c-white);
  border: var(--border-thick);
  box-shadow: var(--shadow-hard);
  transition: transform 0.1s;
}
.neu-btn:active {
  transform: translate(2rpx, 2rpx); /* Tactile Feedback */
  box-shadow: 2rpx 2rpx 0 #000;
}
```

## 3. Advanced Logic Implementation

### 3.1 Network Layer (`utils/request.js`)
We encapsulated `uni.request` to handle authentication transparently.

**Interceptor Pattern Logic**:
1.  **Request Phase**: Check `uni.getStorageSync('token')`. If present, append to `header['Authorization']`.
2.  **Response Phase**:
    - `2xx`: Return `res.data`.
    - `401`: Token expired. Redirect to Login.
    - `4xx/5xx`: Show `uni.showToast()` with error message.

### 3.2 AI Integration Logic (`AICard.vue`)
The AI Card is a self-contained "Smart Component".
- **Props**: Receives raw `content`.
- **Reactive State**: `summary`, `vibe`, `activeTab`.
- **Effect**: `onMounted` triggers the API call.
- **Visuals**: Uses `setInterval` to append characters to `displaySummary` ref every 30ms, creating a robotic/typing feel that aligns with the AI theme.

### 3.3 State Management Strategy
Given the app's moderate complexity, we chose **composition-based local state** over a global store (Pinia).
- **Global Data**: Auth User (stored in LocalStorage).
- **Page Data**: Feed List (stored in Page Ref).
- **Communication**: Event Emits (`$emit('like', id)`).

This reduces bundle size and boilerplate.
