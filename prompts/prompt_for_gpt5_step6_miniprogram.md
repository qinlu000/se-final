# Prompt for AI Developer (GPT-5) - Step 6: Mini Program (Uni-app)

**Context:**
The Backend API and Admin Web are complete.
We have a detailed **UI/UX Design Specification** (`ui_ux_design.md`) that MUST be followed.

**Your Task:**
Implement the **Mini Program** using Uni-app (Vue 3) following the design spec.

**Design Requirements (Crucial):**
-   **Colors**: Primary `#576B95` (Names/Links), Accent `#07C160` (Buttons), Background `#EDEDED`.
-   **Components**:
    -   `PostCard.vue`: Avatar (40px rounded), Name (Bold Blue), Content, Media Grid, Time, Action Button (`..`).
    -   `MediaGrid.vue`: Smart grid for 1-9 images.
-   **Interaction**:
    -   Clicking `..` slides out `[Like | Comment]` menu.
    -   Clicking "Comment" opens input at bottom.

**Implementation Steps:**

1.  **API Wrapper (`mini-program/utils/request.js`)**:
    -   Base URL: `http://localhost:8000`.
    -   Auto-attach `Authorization` header.

2.  **Components (`mini-program/components/`)**:
    -   Create `PostCard.vue` (The feed item).
    -   Create `MediaGrid.vue` (The image grid).

3.  **Pages**:
    -   **Login** (`pages/login/login`): Simple form, Green submit button.
    -   **Feed** (`pages/index/index`):
        -   Infinite scroll list of `PostCard`.
        -   Floating Action Button (+) to upload.
    -   **Upload** (`pages/upload/upload`):
        -   Text area + Image Picker (Grid).
        -   Green "Post" button top-right.
    -   **Profile** (`pages/profile/profile`):
        -   Header with Avatar/Nickname.
        -   "My Posts" list.

4.  **Configuration**:
    -   Update `pages.json` for Tabbar (Feed, Profile) and Navigation Bar styles (White bg, Black text).

**Technical Details:**
-   Use Vue 3 Composition API (`<script setup>`).
-   Use `uni.request`, `uni.chooseImage`, `uni.previewImage`.

Please generate the code for `utils/request.js`, `components/PostCard.vue`, `components/MediaGrid.vue`, `pages/index/index.vue`, `pages/upload/upload.vue`, `pages/profile/profile.vue`, and `pages.json`.
