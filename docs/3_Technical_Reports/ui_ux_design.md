# UI/UX Specification: "Playful Pop" (Neubrutalism)

> [!IMPORTANT]
> This document acts as the **Source of Truth** for the Frontend Polish phase. All styles must strictly adhere to these rules.

## 1. Global Design System

### 1.1 CSS Variables (Root Level)
Define these in `App.vue` or a global CSS file.

```css
:root {
  /* Palette */
  --c-black: #000000;
  --c-white: #FFFFFF;
  --c-yellow: #FFE600;  /* Electric Yellow - Primary */
  --c-pink:   #FF6B6B;  /* Hot Pink - Danger/Like */
  --c-cyan:   #00F0FF;  /* Cyan Pop - Info/Links */
  --c-purple: #9D4EDD;  /* Deep Purple - Secondary */
  --c-bg:     #F3F3F3;  /* Dot Pattern Background Base */

  /* Borders & Shadows */
  --border-thick: 2px solid var(--c-black);
  --border-thin:  1px solid var(--c-black);
  --shadow-hard:  4px 4px 0px var(--c-black);
  --shadow-hover: 2px 2px 0px var(--c-black);
  --radius-s:     4px;
  --radius-m:     8px;
  --radius-full:  999px;
}
```

### 1.2 Core "Neubrutalism" Rules
1.  **Hard Borders**: Every functional element (Cards, Buttons, Inputs, Avatars) MUST have a `2px solid black` border. No exceptions.
2.  **Hard Shadows**: `box-shadow` must have **0 blur**.
3.  **No Gradients**: Use solid, high-saturation flat colors.
4.  **Monospace Headlines**: Use a monospaced font or a very bold sans-serif for headers to give a "raw" feel.

---

## 2. Component Specifications (Mini Program)

### A. The Feed Card (`PostCard.vue`)
*   **Container**:
    *   Background: `var(--c-white)`
    *   Border: `var(--border-thick)`
    *   Shadow: `var(--shadow-hard)`
    *   Radius: `var(--radius-m)`
    *   Margin: `16px` (Floating effect)
*   **Avatar**: Rounded circle with `2px solid black`.
*   **Tag/Pill**:
    *   Background: `var(--c-cyan)`
    *   Border: `var(--border-thick)`
    *   Text: Bold, Uppercase.

### B. Buttons (Primary Action)
*   **Normal State**:
    *   Bg: `var(--c-yellow)`
    *   Border: `var(--border-thick)`
    *   Shadow: `var(--shadow-hard)`
    *   Transform: `translate(0, 0)`
*   **Active/Pressed State**:
    *   Shadow: `none`
    *   Transform: `translate(4px, 4px)` (Physically moves down to cover the shadow)

### C. Bottom Tab Bar
*   Custom implementation (hide default Uni-app tabbar if possible, or style heavily).
*   **Style**: White strip with `top-border: 2px solid black`.
*   **Active Tab**: Yellow circle background behind the icon.

---

## 3. Component Specifications (Admin Web)

### A. Login Card
*   **Layout**: Centered box on a "Dot Matrix" background.
*   **Style**: Massive hard shadow (`8px 8px 0px black`).
*   **Inputs**:
    *   Bg: `white`
    *   Border: `2px solid black`
    *   Focus: Bg changes to `var(--c-yellow)` (light tint).

### B. Dashboard Cards (Stats)
*   Each Stat box is a "Sticker":
    *   Bg: Random pop colors (Yellow, Pink, Cyan).
    *   Border: `2px solid black`.
    *   Icon: Large, outlined.

---

## 4. Animation Micro-Interactions
*   **Like Action**: Heart icon scales up to 1.5x with a "spring" bounce.
*   **Page Load**: Cards slide up with a stagger effect (`staggered-fade-in`).
