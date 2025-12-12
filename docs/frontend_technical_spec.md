# Neubrutalism ("Playful Pop") Frontend Technical Specification

## 1. Overview
This document details the technical implementation of the **Neubrutalism** (internal codename: "Playful Pop") design language across the Multimedia Social Platform.

**Core Philosophy**:
1.  **Honesty**: Structure is visible. Borders are thick (`2px`) and black.
2.  **Playfulness**: High-saturation, solid colors (Yellow/Pink/Cyan).
3.  **Dimensions**: Depth is conveyed through "Hard Shadows" (offset solid blocks), not gradients or blur.

---

## 2. Design Tokens (CSS Variables)
The design system is driven by a set of root-level CSS variables.

### 2.1 Color Palette
| Variable | Value | Usage |
| :--- | :--- | :--- |
| `--c-black` | `#000000` | Borders, Text, Shadows |
| `--c-white` | `#FFFFFF` | Card Backgrounds, Text on Dark |
| `--c-yellow` | `#FFE600` | **Primary Brand**, Buttons, Highlights |
| `--c-pink` | `#FF6B6B` | Like buttons, Errors, "Hot" actions |
| `--c-cyan` | `#00F0FF` | Accents, Links, Info tags |
| `--c-purple` | `#9D4EDD` | Secondary figures, Charts |

### 2.2 Interface Dimensions
| Variable | Value | Description |
| :--- | :--- | :--- |
| `--border-thick` | `2px solid var(--c-black)` | The standard border for **everything**. |
| `--border-thin` | `1px solid var(--c-black)` | Inner dividers, grid lines (Admin). |
| `--shadow-hard` | `4px 4px 0px var(--c-black)` | Standard component shadow. |
| `--shadow-card` | `8px 8px 0px var(--c-black)` | Large floating cards (Login). |
| `--radius-m` | `8px` (MP) / `12px` (Admin) | Standard corner radius. |

---

## 3. Mini Program Implementation (Uni-app)

### 3.1 Global Styles (`App.vue`)
We define the tokens in the `:root` scope and apply a global background pattern.
```css
page {
  background-color: #f3f3f3;
  /* Dot Matrix Pattern */
  background-image: radial-gradient(#dcdcdc 1px, transparent 1px);
  background-size: 18px 18px;
}
```

### 3.2 Utility Classes
We avoid using too many utility libraries (like Tailwind) to maintain strict control over the specific "Pop" look. Instead, we use specific reusable classes:

*   `.neu-card`: Applies white bg, thick border, hard shadow.
*   `.neu-btn`: Primary action button. Electric yellow, thick border.
    *   **Active State**: `transform: translate(4rpx, 4rpx); box-shadow: none;` (Depress effect).

### 3.3 Component Pattern: `PostCard.vue`
*   **Avatar**: `border: 2px solid black`.
*   **Action Pills**: Instead of plain icons, we use "Pills" (Icon + Text) with borders.
*   *Why?* It increases the touch target and fits the "chunky" aesthetic.

### 3.4 Special Components: AI Intelligence
For AI features, we introduce a **Glassmorphism** variant to signify "Magic/Future".
*   **Base Style**: `backdrop-filter: blur(10px); background: rgba(255,255,255,0.8);`
*   **Vibe Check Colors**:
    *   Positive: `background: #FFE60022` (Yellow Tint)
    *   Negative: `background: #93C5FD22` (Blue Tint)
*   **Typography**: Use monospaced font (`DM Mono`) for AI generated text to simulate a terminal/robot effect.

---

## 4. Admin Web Implementation (Vue 3 + Element Plus)

### 4.1 Element Plus Overrides
Admin Web relies heavily on **UI Library Overrides** to force Element Plus into the Neubrutalism style. This is done via `:deep()` selectors in `Layout.vue` or specific views.

**Example: Tables**
```css
:deep(.el-table) {
  border: 1px solid black;
  box-shadow: 4px 4px 0px black;
}
:deep(.el-table th) {
  background: black;
  color: white;
  font-weight: 900;
}
:deep(.el-table td) {
  border: 1px solid black; /* Visible grid lines */
}
```

### 4.2 Layout Strategy
*   **Sidebar**: Pure Black (`#000`) sidebar to contrast with the colorful content.
*   **Menu Items**:
    *   **Active**: Yellow background box with black text and border.
    *   **Inactive**: White text on black.

### 4.3 Data Visualization (ECharts)
Charts in `Stats.vue` must adhere to the style:
1.  **No Gradients**: Use solid fill colors defined in the Palette.
2.  **Thick Lines**: Axis lines and Series lines use `width: 2` or `3`.
3.  **Black Text**: All labels/legends must be `#000` (Bold).

---

## 5. Developer Guide: How to Add New UI

### 5.1 Creating a New Button
**Do NOT** use a standard blue button.
**DO** use the `.neu-btn` class (MP) or `<el-button type="primary">` (Admin) which is already overridden to be Yellow.

```html
<!-- Mini Program -->
<button class="neu-btn">Action</button>

<!-- Admin Web -->
<el-button type="primary">Action</el-button>
```

### 5.2 Creating a New Card
Wrap your content in a container with the standard borders.

```css
.my-new-card {
  background: white;
  border: var(--border-thick);
  box-shadow: var(--shadow-hard);
  border-radius: var(--radius-m);
}
```

### 5.3 Typography Rules
*   **Headings**: Font-weight `700` or `900`. Letter-spacing `0.5px`.
*   **Body**: Standard sans-serif. Color `#1f2937` (Dark Grey) for readability inside cards.

---

## 6. Maintenance
*   **Changing the Theme**: To change the primary color (e.g., from Yellow to Green), modify `--c-yellow` in `App.vue` (MP) and `Layout.vue` (Admin).
*   **Icons**: We use Emojis (Admin sidebar) or standard SVG icons. Ensure they are high-contrast (black/white).
