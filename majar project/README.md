# Product Sentiment Analyzer and Review Dashboard

A full-stack React and Flask application that analyzes product review sentiment with VADER, stores results in MongoDB Atlas when configured, and falls back to an in-memory demo database locally.

## Project map

- `backend/app/routes/__init__.py`: REST API routes
- `backend/app/scraper.py`: safe sample review source; no CAPTCHA or anti-bot bypass
- `backend/app/sentiment.py`: VADER classification
- `backend/app/database.py`: MongoDB and local fallback persistence
- `backend/app/utils.py`: review text cleaning
- `frontend/src/components/`: reusable dashboard UI and charts
- `frontend/src/pages/`: Home, Dashboard, and Reviews views
- `frontend/src/services/api.js`: configurable Axios client
- `backend/seed.py`: inserts ten demo products and analyzed reviews

The frontend includes routed Home, Dashboard, Products, Product Search, Reviews, Sentiment Analysis, Analytics, Trends, Scraper, Reports, History, Favorites, Settings, and Help workspaces. The sidebar collapses into a mobile menu and Settings persists the theme preference in local storage.

## 1. Start the backend

Open a VS Code terminal in the project root:

```powershell
cd "backend"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python run.py
```

Expected output includes Flask running at `http://127.0.0.1:5000`.

The demo works without MongoDB. To use Atlas, open `backend/.env` and set:

```env
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
MONGODB_DATABASE=product_sentiment
CORS_ORIGINS=http://localhost:5173
FLASK_ENV=development
```

In MongoDB Atlas, create a free cluster, create a database user, add your development IP to Network Access, and copy the Driver connection string. Never commit `.env`.

## 2. Start the frontend

Open a second VS Code terminal:

```powershell
cd "frontend"
npm install
npm run dev
```

Open the URL printed by Vite, normally `http://localhost:5173`.

To use another backend URL, create `frontend/.env`:

```env
VITE_API_URL=http://localhost:5000/api
```

## 3. Test the API

With Flask running, these URLs can be opened in a browser or tested with PowerShell:

```powershell
Invoke-RestMethod http://localhost:5000/api/health
Invoke-RestMethod "http://localhost:5000/api/search?product=iPhone%2015"
Invoke-RestMethod http://localhost:5000/api/products
Invoke-RestMethod "http://localhost:5000/api/reviews?product=iPhone%2015"
Invoke-RestMethod http://localhost:5000/api/sentiment/iPhone%2015
Invoke-RestMethod http://localhost:5000/api/analytics/iPhone%2015
```

The search endpoint cleans text, scores each review, stores it, and returns summary metrics plus reviews. Known demo products include iPhone 15, Samsung Galaxy S24, OnePlus 12, Dell Laptop, and Sony Headphones. Unknown products receive a safe sample fallback so the app remains usable when live ecommerce pages are inaccessible.

Additional API routes include:

- `POST /api/sentiment/analyze` and `POST /api/sentiment/bulk`
- `POST /api/scraper/start` for safe demo imports
- `GET/POST/DELETE /api/products` and product detail routes
- `GET/POST/DELETE /api/reviews`
- `GET /api/analytics/overview`, `/sentiment`, and `/trends`
- `GET/DELETE /api/history`
- `GET/POST /api/favorites`

To seed the demo catalog:

```powershell
cd backend
python seed.py
```

## Production build

```powershell
cd frontend
npm run build
```

This creates `frontend/dist`. For deployment, set a real `MONGO_URI`, restrict `CORS_ORIGINS` to your frontend domain, and use a production Flask server such as Gunicorn or Waitress.
