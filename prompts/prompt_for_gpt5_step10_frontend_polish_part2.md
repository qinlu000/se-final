# Prompt for GPT-5: Frontend Polish Part 2 (Remaining Pages)

## Context
We are in the middle of a **Neubrutalism ("Playful Pop")** redesign.
The **Global Styles**, **Feed**, and **Login Page** are already completed (Verified).
Now we need to apply the same design language to the remaining pages.

**Reference**: `docs/ui_ux_design.md`

## Objective
Update the following files to match the Playful Pop aesthetic (Thick borders, Hard Shadows, Electric Yellow/Pink).

## Step-by-Step Instructions

### 1. Mini Program Profile Page
**Target File**: `mini-program/pages/profile/profile.vue`
*   **Header**: Remove the green gradient. Replace it with a white container featuring a `2px solid black` border and `4px` hard shadow.
*   **Stats**: Add distinct vertical dividers (`2px solid black`) between "Followers", "Following", and "Posts".
*   **Buttons**: Style status buttons (Edit Profile, etc.) using the `.neu-btn` class or similar logic (Yellow background, thick border).

### 2. Mini Program Upload Page
**Target File**: `mini-program/pages/upload/upload.vue`
*   **Text Area**: Enclose in a white box with a `2px solid black` border.
*   **Image Picker**:
    *   Style the "Add (+)" button as a dashed black border box (`2px dashed #000`).
    *   On hover/active, give it a yellow background.
*   **Submit Button**: Make it full width, Electric Yellow (`#FFE600`), thick border, hard shadow.

### 3. Admin Web Layout & Tables
**Target File**: `admin-web/src/layout/Layout.vue`
*   **Sidebar**: Change background to pure black (`#000000`).
*   **Menu Items**:
    *   Normal: White text.
    *   Active: Electric Yellow (`#FFE600`) background, Black text, `2px solid yellow` border box.

**Target File**: `admin-web/src/views/Posts.vue` (and `Users.vue` if applicable)
*   **Tables**: Override Element Plus table styles (using `:deep()`).
    *   Add `1px solid black` borders to all cells.
    *   Header: Black background, White text, Bold font.

## Constraints
*   **Consistency**: Reuse the `--c-yellow`, `--c-pink`, `--border-thick` variables defined in root.
*   **Functionality**: Do not break the existing logic (Upload, Logout, etc.).

## Deliverables
*   `mini-program/pages/profile/profile.vue`
*   `mini-program/pages/upload/upload.vue`
*   `admin-web/src/layout/Layout.vue`
*   `admin-web/src/views/Posts.vue`
