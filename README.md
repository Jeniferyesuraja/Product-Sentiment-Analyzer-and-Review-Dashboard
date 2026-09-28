# Product Sentiment Analyzer and Review Dashboard

Full-stack React and Flask app that analyzes product review sentiment using VADER and shows results in a dashboard.

## Features
- Sentiment classification (positive / neutral / negative)
- Dashboard with charts
- Reviews view
- MongoDB Atlas storage, with in-memory fallback locally

## Tech Stack
- Frontend: React, Vite, Axios
- Backend: Flask, VADER
- Database: MongoDB Atlas

## Run Locally

**Backend**
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python run.py

**Frontend**
cd frontend
npm install
npm run dev

## Project Structure
- backend/app - API routes, scraper, sentiment, database
- backend/seed.py - demo data
- frontend/src - components, pages, services
