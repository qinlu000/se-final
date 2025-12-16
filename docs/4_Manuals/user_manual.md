# User Operations Manual (用户操作手册)

## 1. Introduction
Welcome to the **Moments Multimedia Social Platform**! This manual guides you through the features of our Mini Program and Admin Dashboard.

---

## 2. Mini Program (Mobile App)

### 2.1 Getting Started
*   **Launch**: Open the app in HBuilderX or WeChat DevTools.
*   **Login**:
    *   Enter Username: `testuser`
    *   Enter Password: `password`
    *   *First time?* Toggle to **"Register"** mode at the bottom.

### 2.2 Exploring the Feed
*   **Home Tab**: Shows the latest posts from everyone (Moments style).
    *   **Refresh**: Pull down from the top to load new posts.
    *   **Load More**: Scroll to the bottom to fetch older posts.
*   **Interactions**:
    *   ❤️ **Like**: Tap the heart icon to like a post.
    *   💬 **Comment**: Tap the chat bubble to write a comment.
    *   🤖 **AI Insight**: Tap the "Ask AI" button to get a deep summary or vibe check.

### 2.3 Posting Content
1.  Tap the **(+)** floating button in the bottom-right corner.
2.  **Write**: Enter your thoughts in the text box.
3.  **Media**:
    *   Tap `+` to select **Images** (up to 9).
    *   OR tap "Video" to record/upload a **Short Video**.
4.  **Tags**: Type a tag (e.g., "Food") in the tag bar and press Enter.
5.  **AI Assist**: Click "AI 帮写" to polish your text or generate a title.
6.  **Publish**: Hit the Cyan "Publish" button.

### 2.4 Managing Your Profile
*   Go to the **"Me" (我的)** tab.
*   **My Posts**: View a timeline of your own history.
*   **Delete**: Tap the `×` on any of your own posts to remove them.
*   **Logout**: Accessible via the Settings icon.

---

## 3. Admin Dashboard (Web)

### 3.1 Access
*   URL: `http://localhost:5174`
*   Admin Account: `admin` / `123456`

### 3.2 Dashboard Overview
*   **Stats Cards**: View Total Users, Total Posts, and Total Interactions.
*   **Charts**:
    *   *User Growth*: Line chart showing registrations over the last 7 days.
    *   *Content Mix*: Pie chart comparing Text vs. Image vs. Video posts.

### 3.3 Content Moderation
*   Navigate to **"Post Management"**.
*   **Search**: Filter posts by User ID or Keyword.
*   **Audit**: Preview images/videos directly in the table.
*   **Action**: Click "Delete" (Red button) to remove violating content.

### 3.4 User Management
*   Navigate to **"User Management"**.
*   **Action**: Ban/Unban users who violate community guidelines.

---

## 4. FAQ
*   **Q: Why is my video upload failing?**
    *   A: Ensure the video is under 60 seconds and less than 50MB.
*   **Q: AI says "Unavailable"?**
    *   A: You might be hitting the rate limit (10 requests/minute). Please wait a moment.
