# Admin Web Technical Report

## 1. Overview
The Admin Dashboard is the centralized control plane for the Moments platform. It is built as a **Single Page Application (SPA)** using **Vue 3 + TypeScript**.

## 2. Technical Stack Details

### 2.1 Framework: Vue 3 Eco-system
- **Core**: Vue 3 (Composition API).
- **Build**: Vite (Provides `<100ms` HMR).
- **Routing**: Vue Router (Hash mode for simple static hosting).
- **UI Toolkit**: **Element Plus** (Enterprise-grade components).

### 2.2 TypeScript Integration
We enforce strict typing to prevent runtime errors common in admin panels (e.g., missing data fields).

**Interface Definition (`src/types/index.ts`)**:
```typescript
interface User {
  id: number;
  username: string;
  is_admin: boolean;
  created_at: string;
  status: 'active' | 'banned';
}

interface Post {
  id: number;
  content: string;
  author: User;
  media_urls: string[];
}
```

## 3. Module Implementation

### 3.1 Role-Based Access Control (RBAC)
Implemented via a global Navigation Guard in `src/permission.ts`.

**Logic Flow**:
1.  **Intercept**: `router.beforeEach(to, from, next)`
2.  **Check Token**: `getToken()` from Cookie/LocalStorage.
3.  **Check Role**: Call `store.dispatch('user/getInfo')`.
    - If `user.roles` includes `admin`: `next()`.
    - Else: Redirect to `/401`.

### 3.2 Content Moderation Grid (`Posts.vue`)
Leverages `<el-table>` for high-density data display.

**Features**:
- **Lazy Loading Images**: Using `<el-image :preview-src-list="...">` allows moderators to preview reported images without leaving the table context.
- **Debounced Search**: The search input uses `lodash.debounce(300ms)` to prevent API hammering while typing keywords.

### 3.3 Dashboard Visualization (`Dashboard.vue`)
- **Library**: `ECharts` (via `vue-echarts` wrapper).
- **Data**: Fetches aggregated stats from `GET /admin/stats`.
- ** Charts**:
    - **Line Chart**: "New Users (7 Days)".
    - **Pie Chart**: "Post Distribution (Text vs Image)".

## 4. Development Workflow
- **Mock Service**: During early dev, we used **Mock.js** to simulate backend responses, allowing frontend/backend parallel development.
- **Environment Handling**:
    - `.env.development`: `VITE_BASE_API = '/dev-api'`
    - `.env.production`: `VITE_BASE_API = 'https://api.moments.com'`
