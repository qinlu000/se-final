# Prompt for GPT-5: Frontend Polish (Neubrutalism Style)

## Context
You are an expert Frontend Engineer specializing in **Uni-app** (Vue 3) and **Element Plus**.
We are redesigning the UI of our "Multimedia Social Platform" to adopt a **Neubrutalism ("Playful Pop")** aesthetic.

**Reference Document**: `docs/ui_ux_design.md` (Contains exact CSS variables and rules).

## Objective
Update the styling of the **Mini Program** and **Admin Dashboard** to match the new design specification. The goal is to make the interface look "Bold, Raw, and Fun" with thick borders, hard shadows, and vibrant colors.

## Step-by-Step Instructions

### 1. Setup Global Design System (Mini Program)
**Target File**: `mini-program/App.vue`
*   In the `<style>` section, define the root CSS variables as specified in the Design Spec (Colors, Borders, Shadows).
*   Add a global class `.neu-card` that applies the standard border, shadow, and radius.
*   Add a global class `.neu-btn` for the button styles.

### 2. Redesign Feed Card (Mini Program)
**Target File**: `mini-program/components/PostCard.vue`
*   **Container**: Apply the `.neu-card` style. Add margin to separate cards distinctively.
*   **Avatar**: Add `2px solid black` border.
*   **Actions**: Replace the text/icon buttons with "Pill" shaped buttons.
    *   "Like" Button: When active (liked), change background to `var(--c-pink)` with a hard border.
    *   "Comment" Button: standard white with black border.
*   **Images**: Add `2px solid black` border to the image container or individual images.

### 3. Redesign Feed Page (Mini Program)
**Target File**: `mini-program/pages/index/index.vue`
*   **Background**: Set page background to `var(--c-bg)` (CSS radial-gradient dots if possible, or just the light gray).
*   **Floating Button (FAB)**: Style the "Add Post" button as a large `60px` yellow square with rounded corners (radius 16px) and thick borders. High contrast icon.

### 4. Admin Login Page Overhaul (Admin Web)
**Target File**: `admin-web/src/views/Login.vue`
*   **Card**: Transform the login form into a central "Pop Art" card with `8px` hard shadow.
*   **Input Fields**: Remove default Element Plus borders/shadows and apply `2px solid black` borders.
*   **Button**: Primary button should be Electric Yellow with black text and hard shadow.

---

## Constraints
*   **Do Not** modify backend logic.
*   **Do Not** break existing functionality (Like/Delete must still work).
*   **Strictly** follow the color codes: `#FFE600`, `#FF6B6B`, `#00F0FF`, `#000000`.
*   Use `scoped` CSS where appropriate, or utility classes from `App.vue`.

## Deliverables
*   Modified `mini-program/App.vue`.
*   Modified `mini-program/components/PostCard.vue`.
*   Modified `mini-program/pages/index/index.vue`.
*   Modified `admin-web/src/views/Login.vue`.
