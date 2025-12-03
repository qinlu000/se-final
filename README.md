# Multimedia Social Platform ("Moments" Clone)

This project is a multimedia social platform consisting of:
- **Backend**: Python FastAPI (`/backend`)
- **Admin Web**: Vue 3 + Vite (`/admin-web`)
- **Mini Program**: Uni-app (`/mini-program`)

## Setup & Development
For detailed step-by-step instructions, please refer to [RUNNING_GUIDE.md](./RUNNING_GUIDE.md).

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Admin Web
```bash
cd admin-web
npm install
npm run dev
```

### Mini Program
Open `/mini-program` in HBuilderX or run via CLI if configured.

## Architecture
See [project_blueprint.md](./project_blueprint.md) for detailed design and implementation steps.
