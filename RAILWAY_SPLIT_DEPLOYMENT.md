# Railway Split Deployment (Frontend + Backend)

This project needs two Railway services:
- Frontend: Vite static site (already deployed)
- Backend: Flask API (new service)

Once the backend is live, the frontend will call it via `VITE_API_BASE_URL` and auth/login will work (no more 405).

## 1) Create Backend Service
- New Service → From GitHub → select this repo
- Root Directory: `backend`
- Build command:
  ```
  pip install -r requirements.txt
  ```
- Start command (Procfile already added):
  ```
  gunicorn -w 2 -b 0.0.0.0:$PORT app:app
  ```
- Enable Public Networking → copy the URL (e.g. `https://your-backend.up.railway.app`)

## 2) Backend Environment Variables
Set these in the backend service Variables tab:
- `DATABASE_URL=postgresql://postgres:Faviskido1!@db.tctodpkxuiuszxyeskwe.supabase.co:5432/postgres`
- `SECRET_KEY=<strong-random-string>`
- `JWT_SECRET_KEY=<strong-random-string>`
- (Optional) `SENDGRID_API_KEY=<your-sendgrid-key>`
- (Optional) `FLASK_ENV=production`

Tables will be created automatically on startup via `db.create_all()`.

## 3) Point Frontend to Backend
In your existing Vite static site service (the frontend) Variables tab:
- `VITE_API_BASE_URL=https://your-backend.up.railway.app/api`

Save to trigger redeploy. The frontend code already reads this variable.

## 4) Verify
- Open `https://your-backend.up.railway.app/api/health` → should return success JSON
- Open your frontend domain and try login/register

## Notes
- If you see 405 on `/api/auth/*`, it means requests are still going to the static site. Ensure `VITE_API_BASE_URL` is set to the backend URL + `/api` and the frontend has redeployed.
- If backend fails to boot, check logs; ensure `DATABASE_URL` is correct and Supabase password is valid.
- Local dev uses `.env` in `backend/`. Production uses Railway Variables.
