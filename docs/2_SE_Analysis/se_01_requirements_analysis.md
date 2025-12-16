# Software Engineering Analysis 01: Requirements Analysis

## 1. Introduction
This document provides a formal requirement analysis for the "Moments" Multimedia Social Platform, utilizing standard functional and non-functional requirement frameworks to ensure alignment with business goals.

## 2. Requirement Mapping & Compliance Matrix

This section maps the implemented features against the original Course Project Requirements.

### 2.1 Mini Program Frontend (Client Side)

| ID | Requirement Description | Implementation Status | Feature Detail |
| :--- | :--- | :--- | :--- |
| **MP-01** | **Upload Content**: Image, Video, Text | ✅ **Completed** | Supports 9-grid images search or 60s video upload. |
| **MP-02** | **Manage Content**: View/Modify/Delete | ✅ **Completed** | Users can delete their own posts; My Posts tab. |
| **MP-03** | **Retrieval**: Tags, Date | ✅ **Completed** | **Tag System** implemented (Add/Search). |
| **MP-04** | **Interaction**: Rate/Comment | ✅ **Completed** | "Like" (Rating=5) and Text Comments supported. |
| **MP-05** | **Account**: Login/Password | ✅ **Completed** | JWT-based auth with password hashing. |
| **MP-06** | **Bonus: Friend Function** | 🌟 **Implemented** | Follow/Unfollow system; "Following" feed. |
| **MP-07** | **Bonus: Sensitive Word Filter** | 🌟 **Implemented** | "Sandwich Defense" (Pre/Post check) for text. |
| **MP-08** | **Bonus: Video Processing** | 🌟 **Implemented** | Video compression and thumbnail generation (via UniApp). |
| **MP-09** | **Bonus: AI Large Model** | 🌟 **Implemented** | **DeepSeek V3** integration for "Magic Compose" & "Vibe Check". |

### 2.2 Web Admin (Administrator Side)

| ID | Requirement Description | Implementation Status | Feature Detail |
| :--- | :--- | :--- | :--- |
| **ADM-01** | **Content Management**: Query/Delete | ✅ **Completed** | `Posts.vue` grid with delete actions. |
| **ADM-02** | **User Management**: Query/Delete | ✅ **Completed** | `Users.vue` table with ban/delete actions. |
| **ADM-03** | **Bonus: Statistical Analysis** | 🌟 **Implemented** | ECharts dashboard showing DAU, Content Distribution. |

## 3. Detailed Functional Requirements (FR)

### 3.1 User Module (MP)
*   **FR-USR-01 (Registration/Login)**: Users must be able to create accounts using a unique username and password. The system must employ JWT for stateless session management.
*   **FR-USR-02 (Profile Management)**: Users can update their nickname and avatar.
*   **FR-USR-03 (Social Graph)**: Users can follow/unfollow others. The system must maintain a many-to-many relationship mapping.

### 2.2 Content Module
*   **FR-CNT-01 (Post Creation)**:
    *   **Text content**: mandatory, max 1000 characters.
    *   **Multimedia**: Support for 1-9 images OR 1 short video (<60s).
    *   **Tags**: Support adding up to 5 topic tags per post.
*   **FR-CNT-02 (Feed Consumption)**:
    *   Users can view a chronological feed of posts from followed users.
    *   Users can view a "Discover" feed of all public posts.
*   **FR-CNT-03 (Interactions)**:
    *   **Like**: Toggleable like status with immediate UI feedback (Optimistic UI).
    *   **Comment**: Text-based comments on specific posts.
    *   **Delete**: Authors can delete their own posts.

### 2.3 AI Intelligence Module
*   **FR-AI-01 (Content Polishing)**: Use LLM to rewrite user input for better tone/clarity.
*   **FR-AI-02 (Sentiment Analysis)**: "Vibe Check" analyzes post sentiment and assigns an emoji/color label.
*   **FR-AI-03 (Summarization)**: Generate concise summaries for long posts.

### 2.4 Administrative Module
*   **FR-ADM-01 (Data Visualization)**: Dashboard showing DAU (Daily Active Users), Post volume, and Media type distribution.
*   **FR-ADM-02 (Content Moderation)**: Admins can view table lists of Users/Posts and ban users or delete posts violating terms.

## 3. Non-Functional Requirements (NFR)

### 3.1 Performance
*   **NFR-PER-01 (Latency)**: API response time < 200ms for 95% of requests.
*   **NFR-PER-02 (Throughput)**: Support 100 concurrent uploads without service degradation.
*   **NFR-PER-03 (Rendering)**: First Contentful Paint (FCP) on Mini Program < 1.5s.

### 3.2 Security
*   **NFR-SEC-01 (Authentication)**: All protected endpoints must validate `Authorization: Bearer <token>`.
*   **NFR-SEC-02 (Data Privacy)**: Passwords must be hashed with `bcrypt` (work factor > 12).
*   **NFR-SEC-03 (Input Validation)**: All user inputs must be sanitized to prevent XSS and SQL Injection (handled via Pydantic/SQLAlchemy).

### 3.3 Reliability & Availability
*   **NFR-REL-01 (Error Handling)**: System must degrade gracefully. If AI service is down, posting function must remain operational.
*   **NFR-REL-02 (Uptime)**: Target unavailability < 1 hour/month (99.9%).

### 3.4 Maintainability
*   **NFR-MNT-01 (Code Quality)**: Backend follows PEP8; Frontend follows Vue Style Guide (Priority B).
*   **NFR-MNT-02 (Documentation)**: API must have Swagger/OpenAPI documentation auto-generated.

## 4. User Stories & Acceptance Criteria

| ID | As a... | I want to... | So that... | Acceptance Criteria |
| :--- | :--- | :--- | :--- | :--- |
| US-01 | Creator | Upload a video | I can share dynamic moments | Video plays inline; < 60s restriction enforced. |
| US-02 | Reader | See a "Summary" button | I can skip reading long text | Clicking shows a valid <50 word summary. |
| US-03 | Admin | See daily stats | I know if the app is growing | Dashboard loads real DB counts, not mock data. |
