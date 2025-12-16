# Project Phase Record

## Phase: Video Support & UI Polish (2025-12-16)
- **Frontend**:
  - Implemented Neu-Brutalism UI theme (Solid borders, Cards, Popups).
  - Added `NeuPopup` component for consistent Modals/ActionSheets.
  - Updated `upload.vue` to support Video selection (Compressed, Max 60s).
  - Updated `PostCard.vue` to render Video.
- **Backend**:
  - Validated Database support for `video` MediaType.
  - Refactored `upload` API to use Streaming (Fixed OOM).
  - Added CORS configuration.
- **Bug Fixes**:
  - Restored accidental code deletion in `upload.vue`.
  - Added auto-redirect for 401 Unauthorized in `request.js`.
  - Improved error messages for upload failures.
