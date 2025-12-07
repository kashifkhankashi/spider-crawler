# Website Analysis Tool

A real-time website analysis tool similar to Ahrefs and Siteliner, built with Python (FastAPI) and Next.js. This tool performs comprehensive SEO audits, keyword analysis, duplicate content detection, and performance analysis without requiring a database.

## Features

- **Real-Time Website Crawling**: Fast crawling with Playwright for JS-rendered pages
- **SEO Technical Audit**: Comprehensive checks for missing titles, meta descriptions, duplicate H1s, broken links, redirects, and more
- **Keyword Analysis**: RAKE, N-grams, and TF-IDF keyword extraction with clustering
- **Duplicate Content Detection**: MinHash, Cosine Similarity, and Jaccard similarity algorithms
- **Performance Analysis**: Google PageSpeed API integration for Core Web Vitals
- **Beautiful Dashboard**: Modern Next.js UI with interactive charts and visualizations

## Tech Stack

### Backend
- Python 3.11
- FastAPI
- Playwright (for JS-rendered pages)
- BeautifulSoup + lxml
- Scrapy (for fast crawling)
- RAKE-NLTK, scikit-learn (for NLP)
- Datasketch (for MinHash)
- Celery + Redis (for async tasks)

### Frontend
- Next.js 14 (TypeScript)
- Tailwind CSS
- React Query
- Recharts

## Quick Start

### Prerequisites

- Python 3.11+ (or Python 3.13)
- Node.js 20+
- (Optional) Docker and Docker Compose
- (Optional) Google PageSpeed API key for performance analysis

### Installation

#### Option 1: Using Docker (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd Crawler
```

2. (Optional) Set up Google PageSpeed API key:
```bash
export GOOGLE_PAGESPEED_API_KEY=your_api_key_here
```

3. Start the services:
```bash
# For newer Docker versions (Docker Desktop 3.0+)
docker compose up --build

# For older versions, use:
# docker-compose up --build
```

4. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

#### Option 2: Manual Setup (Windows)

**Backend:**
1. Run the setup script:
```bash
setup-backend-windows.bat
```

2. Start the backend:
```bash
start-backend.bat
```

**Frontend:**
1. Open a new terminal:
```bash
cd frontend
npm install
npm run dev
```

**Access:** http://localhost:3000

## Manual Setup (Without Docker)

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
# On Windows (if you get "Unable to copy" error, see Troubleshooting below)
python -m venv venv

# If the above fails, try:
python -m venv venv --clear

# Or use the system Python directly (skip venv):
# Just install packages globally (not recommended but works)
```

3. Activate virtual environment:
```bash
# On Windows (Git Bash or Command Prompt):
venv\Scripts\activate

# On Windows (PowerShell):
venv\Scripts\Activate.ps1

# On Linux/Mac:
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Install Playwright browsers:
```bash
playwright install chromium
```

6. Download NLTK data:
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

7. Run the server:
```bash
# With virtual environment activated:
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or without venv (if venv creation failed):
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run development server:
```bash
npm run dev
```

4. Open http://localhost:3000 in your browser

## Usage

1. **Start a Scan**:
   - Enter a website URL on the home page
   - Set the maximum number of pages to scan (default: 50)
   - Click "Start Analysis"

2. **View Results**:
   - The scan will process in the background
   - Results are displayed in real-time as they become available
   - View comprehensive analysis including:
     - Crawl summary with statistics
     - SEO audit score and issues
     - Keyword analysis and clusters
     - Duplicate content detection
     - Performance metrics

## API Endpoints

### POST `/api/scan`
Start a new website scan.

**Request Body:**
```json
{
  "url": "https://example.com",
  "max_pages": 50,
  "include_external": false
}
```

**Response:**
```json
{
  "scan_id": "uuid",
  "status": "pending",
  "message": "Scan started successfully"
}
```

### GET `/api/scan/{scan_id}/status`
Get the status of a scan.

**Response:**
```json
{
  "scan_id": "uuid",
  "status": "processing" | "completed" | "error"
}
```

### GET `/api/scan/{scan_id}/results`
Get the complete results of a scan.

**Response:**
```json
{
  "crawl_results": {...},
  "seo_audit": {...},
  "keywords": {...},
  "duplicates": {...},
  "performance": {...}
}
```

## Project Structure

```
Crawler/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── crawler/
│   │   │   └── spider.py        # Website crawler
│   │   ├── audit/
│   │   │   └── seo_audit.py     # SEO audit module
│   │   ├── analysis/
│   │   │   ├── keywords.py      # Keyword analysis
│   │   │   └── duplicates.py    # Duplicate detection
│   │   ├── performance/
│   │   │   └── pagespeed.py     # PageSpeed integration
│   │   └── tasks/
│   │       └── celery_app.py    # Celery configuration
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── app/                 # Next.js app directory
│   │   ├── components/          # React components
│   │   └── lib/                 # Utilities
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## Configuration

### Environment Variables

- `GOOGLE_PAGESPEED_API_KEY`: (Optional) Google PageSpeed API key for performance analysis
- `REDIS_URL`: Redis connection URL (default: `redis://localhost:6379/0`)

### Backend Configuration

The crawler can be configured in `backend/app/crawler/spider.py`:
- `max_pages`: Maximum pages to crawl (default: 100)
- `include_external`: Whether to include external links (default: False)

## Features in Detail

### Website Crawler
- Async crawling with Playwright for JavaScript-rendered pages
- Extracts: URLs, titles, meta descriptions, headings, content, links, images
- Tracks: status codes, load times, word counts, content hashes

### SEO Audit
- Missing titles and meta descriptions
- Short content detection
- Duplicate H1 tags
- Broken links (4xx, 5xx)
- Redirect chains
- Canonical issues
- Duplicate titles and meta descriptions
- Page depth analysis

### Keyword Analysis
- **RAKE**: Rapid Automatic Keyword Extraction
- **N-grams**: Unigrams, bigrams, trigrams
- **TF-IDF**: Term Frequency-Inverse Document Frequency
- Keyword clustering based on semantic similarity

### Duplicate Detection
- **MinHash**: Fast approximate similarity
- **Cosine Similarity**: Vector-based similarity
- **Jaccard Similarity**: Set-based similarity

### Performance Analysis
- Google PageSpeed API integration
- Core Web Vitals: LCP, CLS, FID, FCP, TTI
- Performance recommendations

## Limitations

- No database: All results are stored in memory and lost on server restart
- Rate limiting: Be respectful when crawling websites
- PageSpeed API: Requires API key for real analysis (mock data provided without key)
- Large websites: May take significant time for large sites (>100 pages)

## Troubleshooting

### Virtual Environment Creation Error (Windows)
If you get "Unable to copy venvlauncher.exe" error:

**Solution 1: Delete existing venv and recreate**
```bash
cd backend
rmdir /s /q venv  # Remove existing venv
python -m venv venv --clear
```

**Solution 2: Use system Python (skip venv)**
```bash
cd backend
# Skip venv creation, install directly
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

**Solution 3: Run as Administrator**
- Right-click Command Prompt/PowerShell
- Select "Run as Administrator"
- Then try: `python -m venv venv`

**Solution 4: Check antivirus**
- Temporarily disable antivirus
- Try creating venv again
- Re-enable antivirus after

### Playwright Installation Issues
If Playwright fails to install:
```bash
cd backend
playwright install chromium
```

### NLTK Data Missing
If you see NLTK errors:
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

### Port Conflicts
If ports 3000 or 8000 are in use, modify `docker-compose.yml` to use different ports.

### Quick Start (Windows - Without Venv)
If venv keeps failing, you can run without it:
```bash
cd backend
pip install -r requirements.txt
playwright install chromium
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

## Support

For issues and questions, please open an issue on GitHub.

# spider-crawler
