# Prompt for AI Developer (GPT-5) - Step 8: Frontend Bonus Features

**Context:**
The Backend has the logic for "Friends" and "Sensitive Words".
Now we need to expose these features in the **Frontend** and add a **Statistics Dashboard**.

**Your Task:**
Implement the UI for Bonus Features in both Admin Web and Mini Program.

**Part 1: Backend Support (Statistics)**
-   **Router** (`backend/app/routers/stats.py`):
    -   `GET /stats/dashboard`: Return JSON `{ "total_users": 100, "total_posts": 500, "daily_active": [...] }`.
    -   *Note*: You can mock the daily trend data for now.
-   **Main**: Register `stats_router`.

**Part 2: Admin Web (Statistics)**
-   **Dependency**: Install `echarts` (`npm install echarts`).
-   **Page** (`admin-web/src/views/Stats.vue`):
    -   Fetch data from `/stats/dashboard`.
    -   Render a Line Chart (User Growth) and Pie Chart (Post Types) using ECharts.
-   **Router**: Add `/stats` route.

**Part 3: Mini Program (Friend System)**
-   **PostCard Component** (`mini-program/components/PostCard.vue`):
    -   Add "Follow" button next to the user's name.
    -   *Logic*:
        -   If `post.user_id == current_user.id`, hide button.
        -   Check `is_following` status (You might need to update `GET /posts` to include this field, or fetch separately. *Simplest approach*: Update `PostOut` schema in backend to include `is_following` boolean).
-   **Feed Page** (`mini-program/pages/index/index.vue`):
    -   Add a Segmented Control (Tabs) at top: `[ All | Following ]`.
    -   Clicking "Following" reloads list with `?filter=following`.
-   **Profile Page** (`mini-program/pages/profile/profile.vue`):
    -   Show "Followers: X" and "Following: Y" counts.
    -   (Optional) Click to view list.

**Technical Details:**
-   **Backend**: Update `PostOut` schema to include `is_following` (requires DB lookup in `list_posts`).
-   **Frontend**: Ensure UI matches the existing design style.

Please generate the code for:
1.  Backend: `routers/stats.py`, updated `schemas.py` (add `is_following`), updated `routers/posts.py` (populate `is_following`).
2.  Admin Web: `views/Stats.vue`.
3.  Mini Program: Updated `components/PostCard.vue`, `pages/index/index.vue`, `pages/profile/profile.vue`.
