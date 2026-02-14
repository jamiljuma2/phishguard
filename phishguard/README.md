# PhishGuard

PhishGuard is a full-stack AI-powered phishing email detection app. It features a React + Vite + Tailwind frontend and a Flask backend with a trained scikit-learn model.

## Features
- Real-time phishing detection using ML
- Dashboard with live stats
- Scan history with detailed reports
- Modern, responsive UI

## Project Structure
```
phishguard/
  backend/      # Flask API, model, utils, scan history
  frontend/     # React app, Tailwind, Vite
```

## Getting Started

### Backend
1. Install Python 3.10+ and pip
2. Install dependencies:
   ```
   cd phishguard/backend
   pip install -r requirements.txt
   ```
3. Ensure `phishing_model.pkl` is present in `backend/`
4. Run the server:
   ```
   python app.py
   ```
   The API will be available at http://localhost:5000

### Frontend
1. Install Node.js 18+
2. Install dependencies:
   ```
   cd phishguard/frontend
   npm install
   ```
3. Start the dev server:
   ```
   npm run dev
   ```
   The app will be available at http://localhost:5173 (or next available port)

## API Endpoints
- `POST /predict` — Analyze email (JSON: `{ email_text, email, subject }`)
- `GET /history` — Get scan history
- `GET /dashboard_stats` — Get dashboard stats
- `GET /health` — Health check

## CI/CD
- GitHub Actions workflows for backend (Python) and frontend (Node.js) included in `.github/workflows/`

## License
MIT
