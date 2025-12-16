# Multimedia Social Platform - Detailed Running Guide

This guide provides step-by-step instructions to set up and run the entire Multimedia Social Platform system, including the Backend, Admin Web, and Mini Program.

## 1. System Requirements

Before you begin, ensure you have the following installed:
-   **Python 3.9+** (for Backend)
-   **Node.js 16+** (for Admin Web)
-   **HBuilderX** (Recommended for running the Uni-app Mini Program)

---

## 2. Backend Setup (FastAPI)

The backend handles all data logic, API requests, and database interactions.

### 2.1 Navigate to Directory
Open your terminal and switch to the backend folder:
```bash
cd backend
```

### 2.2 Create Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
# Activate on macOS/Linux:
source venv/bin/activate
# Activate on Windows:
.\venv\Scripts\activate
```

### 2.3 Configure Environment Variables (AI Setup)
The system requires an LLM provider for AI features. We use **OpenRouter**.
1.  Create a file named `.env` in the `backend/` directory.
2.  Add your API Key:
    ```env
    # Database: Default uses SQLite (Zero-config). No need to change.
    DATABASE_URL=sqlite+aiosqlite:///app.db
    
    # Security
    SECRET_KEY=change_this_to_a_secure_random_string
    
    # AI Service (OpenRouter)
    OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxx
    # REQUIRED: Use this exact model slug
    OPENROUTER_MODEL=deepseek/deepseek-chat
    ```


### 2.3 Install Dependencies
```bash
pip install -r requirements.txt
```

### 2.4 Initialize Database & Create Admin
You need to create an initial administrator account to access the Admin Web.
```bash
# Usage: python scripts/create_admin.py <username> <password>
python scripts/create_admin.py admin 123456
```

### 2.5 Start the Server
```bash
uvicorn main:app --reload --port 8000
```
*   **Success**: You should see logs indicating the server is running at `http://127.0.0.1:8000`.
*   **API Docs**: Visit `http://localhost:8000/docs` to verify.

---

## 3. Admin Web Setup (Vue 3 + Vite)

The web dashboard for administrators to manage users and content.

### 3.1 Navigate to Directory
Open a **new** terminal window:
```bash
cd admin-web
```

### 3.2 Install Dependencies
```bash
npm install
```

### 3.3 Start Development Server
```bash
npm run dev
```
*   **Note**: The port is configured to **5174** in `vite.config.ts` to avoid conflicts with other services.
*   **Access**: Open `http://localhost:5174` in your browser.

### 3.4 Login
*   **Username**: `admin`
*   **Password**: `123456` (or whatever you set in step 2.4)

---

## 4. Mini Program Setup (Uni-app)

The mobile interface for end-users.

### 4.1 Open in HBuilderX
1.  Launch **HBuilderX**.
2.  Click **File** -> **Open Directory**.
3.  Select the `mini-program` folder in the project.

### 4.2 Run in Browser (H5 Simulator)
1.  In the top menu, click **Run** -> **Run to Browser** -> **Chrome** (or your preferred browser).
2.  This will launch the mobile app simulator.
3.  **Tip**: Press `F12` in Chrome and toggle the "Device Toolbar" (mobile icon) to simulate a phone screen.

---

## 5. Feature Walkthrough & Testing

### 5.1 User Registration & Login (Mini Program)
1.  On the login page, click **"Register"** (toggle button).
2.  Enter a username (e.g., `testuser`) and password.
3.  (Optional) Enter a nickname.
4.  Click **Register**. You will be automatically logged in.

### 5.2 Posting Content
1.  Click the **+ (Plus)** floating button on the bottom right.
2.  Enter some text content.
3.  (Optional) Click the **+** grid item to upload images.
4.  Click **Publish**. You should be redirected to the Feed and see your new post.

### 5.3 Interactions
*   **Like**: Click the Heart icon ❤️. It turns red instantly. Click again to cancel.
*   **Comment**: Click the Chat icon 💬. Enter text and send. It appears immediately below the post.
*   **Follow**: Click the **"Follow"** button next to another user's name.
*   **Delete**: If you are the author of a post, click the **✕** icon in the top-right of the post card to delete it.

### 5.4 Profile Management
1.  Go to the **Profile** tab (bottom right).
2.  View your stats (Following, Followers, Posts).
3.  Click the **Settings (⚙️)** icon in the top-right corner to **Logout**.

### 5.5 Admin Management (Admin Web)
1.  Go to `http://localhost:5174` and login as admin.
2.  **Dashboard**: View real-time statistics and charts.
3.  **Users**: View list of registered users. You can delete users here.
4.  **Posts**: View all posts. You can filter by media type (Text/Image) and delete inappropriate posts.

---

## 6. Troubleshooting

*   **Port Conflicts**:
    *   If port 8000 is busy, kill the process using it or change the port in the `uvicorn` command.
    *   If port 5174 is busy, Vite will automatically try the next available port (e.g., 5175). Check the terminal output.
*   **CORS Errors**:
    *   Ensure the Backend is running. The frontend needs to talk to `http://localhost:8000`.
    *   If you see network errors, check the browser console (F12).
*   **Images Not Loading**:
    *   Ensure the `static/uploads` directory exists in the `backend` folder. The system should create it automatically, but permissions issues can sometimes occur.

---

**Enjoy your Multimedia Social Platform!** 🚀
