# Quick Start Guide

## Using Docker (Recommended)

1. **Clone and navigate to the project:**
   ```bash
   cd Crawler
   ```

2. **Start all services:**
   ```bash
   # For newer Docker versions (Docker Desktop 3.0+)
   docker compose up --build
   
   # For older versions, use:
   # docker-compose up --build
   ```

3. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

4. **Stop services:**
   ```bash
   docker compose down
   # or: docker-compose down
   ```

## Manual Setup

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## First Scan

1. Open http://localhost:3000
2. Enter a website URL (e.g., `https://example.com`)
3. Set max pages (recommended: 50 for first test)
4. Click "Start Analysis"
5. Wait for results (usually 1-5 minutes depending on site size)

## Troubleshooting

### Backend won't start
- Make sure Python 3.11+ is installed
- Install Playwright: `playwright install chromium`
- Download NLTK data: `python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"`

### Frontend won't start
- Make sure Node.js 20+ is installed
- Run `npm install` in the frontend directory
- Check if port 3000 is available

### Docker issues
- Make sure Docker Desktop is installed (download from https://www.docker.com/products/docker-desktop)
- On Windows, use `docker compose` (space) instead of `docker-compose` (hyphen) for newer versions
- Try: `docker compose down -v` to remove volumes and start fresh
- Check logs: `docker compose logs backend` or `docker compose logs frontend`
- If Docker isn't installed, use the Manual Setup instructions below

### Scan fails
- Check backend logs for errors
- Make sure the website URL is accessible
- Try with a smaller max_pages value
- Some websites may block crawlers - try a different site

