# Fly.io Deployment Guide for SMS Guard

This guide explains how to deploy both the backend (Flask) and frontend (React/Vite) of SMS Guard on Fly.io.

---

## Prerequisites

- [Fly.io account](https://fly.io/)
- [Fly CLI installed](https://fly.io/docs/hands-on/install-flyctl/)
- Docker installed (for local builds)
- GitHub repo with your project code

---

## 1. Deploying the Backend (Flask API)

### 1.1. Dockerfile

Your backend/Dockerfile is already set up for Flask.

### 1.2. fly.toml

Your fly.toml is in the project root and points to backend/Dockerfile.

### 1.3. Environment Variables

Set required secrets for your backend:

```bash
fly secrets set SECRET_KEY=your_secret_key
fly secrets set DATABASE_URL=your_database_url
fly secrets set SENDGRID_API_KEY=your_sendgrid_api_key  # Optional
```

### 1.4. Launch and Deploy

```bash
cd /path/to/your/project
fly launch  # Only needed the first time
fly deploy
```

- The backend will be available at https://your-app-name.fly.dev

---

## 2. Deploying the Frontend (React/Vite)

### Option 1: Deploy on Fly.io (as a static site)

1. Build the frontend:
   ```bash
   npm run build
   ```
2. Create a Dockerfile in the frontend directory (or project root) for static file serving (e.g., with nginx or serve).
3. Add a fly.toml for the frontend app.
4. Set the environment variable `VITE_API_BASE_URL` to your backend's Fly.io URL.

### Option 2: Deploy on Netlify or Vercel

- Connect your repo and set the build command to `npm run build` and publish directory to `dist`.
- Set `VITE_API_BASE_URL` to your backend's Fly.io URL in the Netlify/Vercel dashboard.

---

## 3. CORS Configuration

- Ensure your backend allows CORS from your frontend domain (e.g., Netlify or Fly.io frontend URL).

---

## 4. Troubleshooting

- If you see "Internal Server Error" or "502 Bad Gateway," check your backend logs:
  ```bash
  fly logs
  ```
- Make sure all environment variables and secrets are set.
- Ensure the backend is listening on 0.0.0.0 and the correct port ($PORT or 8080).

---

## 5. Useful Commands

- Deploy: `fly deploy`
- View logs: `fly logs`
- Set secrets: `fly secrets set KEY=VALUE`
- Open app: `fly open`

---

## 6. Updating

- Push changes to your repo and run `fly deploy` to update your app.

---

## 7. Resources

- [Fly.io Docs](https://fly.io/docs/)
- [Flask Deployment on Fly.io](https://fly.io/docs/app-guides/python/)
- [React/Vite Deployment](https://vitejs.dev/guide/static-deploy.html)

---

## 8. Contact

For issues or questions, open an issue on GitHub or contact the maintainer.
