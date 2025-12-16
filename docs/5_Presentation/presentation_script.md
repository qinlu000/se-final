# Final Project Defense Script (答辩讲稿大纲)

## Slide 1: Cover Page
*   **Project Title**: Multimedia Social Platform ("Moments")
*   **Team Member**: [Your Name]
*   **Course**: Software Engineering

## Slide 2: Project Background & Objectives
*   **Goal**: Develop a full-stack social media solution with modern features.
*   **Pain Points Solved**:
    *   Rich media sharing (Video/Image).
    *   Information overload (Solved via AI Summarization).
*   **Target Users**: Social sharers (App) and Platform Moderators (Web).

## Slide 3: Functional Overview (Demo)
*   **Mini Program (Frontend)**:
    *   *Core*: Post/Delete, Like/Comment.
    *   *Innovation*: **AI Assistant** (Vibe Check, Polish), **Video Upload**, **Tag System**.
*   **Admin Web (Backend)**:
    *   *Core*: User/Post Management.
    *   *Innovation*: **Real-time Data Visualization** (ECharts).

## Slide 4: System Architecture
*   **Tech Stack**:
    *   **Frontend**: UniApp (Vue 3) + Element Plus (Admin).
    *   **Backend**: FastAPI (Python) + SQLAlchemy (Async).
    *   **AI**: OpenRouter (DeepSeek V3) Integration.
*   **Design Pattern**: Separation of Concerns, MVVM, Micro-Monolith.

## Slide 5: Key Technical Challenges & Solutions
1.  **Challenge**: AI Response Latency.
    *   **Solution**: Optimistic UI (Frontend) + Semantic Caching (Backend, Reduces latency 95% for hits).
2.  **Challenge**: Large Video Uploads.
    *   **Solution**: Stream processing in FastAPI + Client-side compression.
3.  **Challenge**: Data Consistency.
    *   **Solution**: Transactional commits in Postgres/SQLite.

## Slide 6: Software Engineering Practices
*   **Requirement Analysis**: Detailed FR/NFR analysis.
*   **Quality Assurance**: Unit Tests (Pytest) + Manual E2E Testing.
*   **Documentation**: Comprehensive Technical Reports & User Manuals.

## Slide 7: Live Demonstration
*   *(Switch to App Emulator)*
*   Show: Login -> Post Video -> Add Tag -> Ask AI -> Publish.
*   *(Switch to Admin Web)*
*   Show: Dashboard Stats increase -> Delete the post -> Show it gone from App.

## Slide 8: Future Outlook
*   **RAG**: Personalized AI based on user history.
*   **Social**: Private Chat / Groups.
*   **Infrastructure**: Docker/K8s deployment.

## Slide 9: Q&A
*   Thank you for listening!
