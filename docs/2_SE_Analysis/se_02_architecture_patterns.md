# Software Engineering Analysis 02: Architecture & Design Patterns

## 1. Architectural Style

The system adopts a **Separation of Frontend and Backend** architecture, evolving towards a **Micro-Monolith**.

### 1.1 Backend: Layered Architecture
The FastAPI backend is structured into distinct logical layers to enforce separation of concerns:
1.  **Presentation Layer (`routers/`)**: Handles HTTP requests, parameter parsing, and response formatting.
2.  **Service/Logic Layer (`core/`, implied)**: Contains business rules (e.g., AI rate limiting, Auth logic). 
    *   *Note: In this project, service logic is often co-located in routers for simplicity, but extracted for complex features like `llm.py`.*
3.  **Data Access Layer (`models/`)**: Abstracts database interactions using SQLAlchemy ORM.
4.  **Domain Layer (`schemas/`)**: Defines data structures (DTOs) using Pydantic, ensuring type safety.

### 1.2 Frontend: MVVM Pattern
Both the Admin Web (Vue 3) and Mini Program (UniApp) utilize the **Model-View-ViewModel (MVVM)** pattern.
*   **Model**: JavaScript Objects / Refs storing state (e.g., `const posts = ref([])`).
*   **View**: Template (`<template>`) defining the UI structure.
*   **ViewModel**: The reactive glues (`<script setup>`) that binds Model to View automatically.

## 2. Design Patterns Applied

### 2.1 Factory Pattern (Backend)
*   **Usage**: In `main.py`, the `logging` setup and `app` creation follow a factory-like initialization sequence to configure middleware and routes dynamically.

### 2.2 Singleton Pattern (Backend)
*   **Usage**: The `AsyncOpenAI` client in `app/core/llm.py` is instantiated once and reused across requests to maintain connection pooling.
*   **Usage**: Database configuration (`SessionLocal`) acts as a singleton registry for connection pools.

### 2.3 Dependency Injection (DI)
*   **Usage**: Crucial in FastAPI. `Depends(get_current_user)` injects the authenticated user object into route handlers.
    *   *Benefit*: Decouples authentication logic from business logic; makes testing easier (can override dependencies).

### 2.4 Proxy Pattern (AI Service)
*   **Usage**: The Backend acts as a **Proxy** between the Client and the LLM Provider (OpenRouter).
    *   *Benefit*: Hides API keys from the client; enforces rate limiting; allows switching providers transparently.

### 2.5 Observer/Publish-Subscribe (Frontend)
*   **Usage**: Vue's Reactivity System. When `ref` data changes, all dependent DOM elements automatically update.
*   **Usage**: `uni.$emit` / `uni.$on` (used in older UniApp patterns, though we prefer Props/Emits) for cross-component communication.

## 3. Data Flow Architecture

### 3.1 Unidirectional Data Flow (Frontend)
In `PostCard.vue`:
*   **Props Down**: `Post` data is passed from Parent (`index.vue`).
*   **Events Up**: Actions like `@like` or `@delete` emit events back to the Parent to modify the source list.

### 3.2 Stateless REST API
The API adheres to RESTful principles:
*   **Stateless**: No session data stored on server RAM (uses JWT).
*   **Resource-Based**: URLs represent resources (`/posts`, `/users/{id}`).
*   **Standard Methods**: GET (read), POST (create), DELETE (remove).

## 4. Concurrency Model
*   **AsyncIO**: The backend uses Python's `async/await` pattern.
    *   Blocking I/O operations (DB queries, HTTP requests to AI) are awaited, allowing the single-threaded Event Loop to handle other requests concurrently.
    *   *Impact*: High throughput for I/O-bound tasks typical in social media apps.
