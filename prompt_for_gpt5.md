# Prompt for AI Developer (GPT-5)

**Role:** You are an expert Full Stack Developer specializing in Python (FastAPI) and Vue 3.

**Context:**
I am building a Multimedia Social Platform ("Moments" Clone).
I have already designed the system and set up the initial project skeleton.
The detailed requirements, database schema, and API design are documented in `project_blueprint.md` located in the root directory.

**Current Project Structure:**
- `project_blueprint.md`: **READ THIS FIRST.** It contains the Source of Truth.
- `backend/`: FastAPI skeleton (main.py, requirements.txt).
- `admin-web/`: Vue 3 + Element Plus skeleton.
- `mini-program/`: Uni-app skeleton.

**Your Task:**
Please act as the lead developer and start implementing **Phase 1: Backend Core** as described in the blueprint.

**Step 1:**
1.  Analyze `project_blueprint.md` to understand the Data Models (User, Post, Comment, Rating, Tag).
2.  Implement the **SQLAlchemy Models** in `backend/app/models/`.
3.  Set up the **Database Connection** (Async) in `backend/app/core/database.py`.

Please generate the code for the database connection and the models.
