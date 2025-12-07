# Setup Instructions

## Option 1: Manual Setup (Recommended if Docker is not installed)

Since Docker is not installed, you can run the application manually. Both Python and Node.js are already installed on your system.

### Step 1: Setup Backend

1. **Run the backend setup script:**
   ```bash
   setup-backend.bat
   ```

   Or manually:
   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   playwright install chromium
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
   ```

### Step 2: Setup Frontend

1. **Run the frontend setup script:**
   ```bash
   setup-frontend.bat
   ```

   Or manually:
   ```bash
   cd frontend
   npm install
   ```

### Step 3: Start the Application

You need to run both backend and frontend in separate terminal windows:

**Terminal 1 - Backend:**
```bash
start-backend.bat
```
Or manually:
```bash
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
start-frontend.bat
```
Or manually:
```bash
cd frontend
npm run dev
```

### Step 4: Access the Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Option 2: Install Docker Desktop (Alternative)

If you prefer using Docker:

1. **Download Docker Desktop for Windows:**
   - Visit: https://www.docker.com/products/docker-desktop
   - Download and install Docker Desktop

2. **After installation, restart your terminal and run:**
   ```bash
   docker compose up --build
   ```

## Troubleshooting

### Backend Issues

- **Module not found errors**: Make sure you activated the virtual environment (`venv\Scripts\activate`)
- **Playwright errors**: Run `playwright install chromium` in the backend directory
- **NLTK errors**: Run `python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"`

### Frontend Issues

- **Port 3000 already in use**: Change the port in `package.json` or stop the process using port 3000
- **npm install fails**: Make sure Node.js is installed and try `npm cache clean --force`

### Connection Issues

- **Frontend can't connect to backend**: Make sure backend is running on port 8000
- **CORS errors**: The backend CORS is configured for localhost:3000, make sure frontend runs on that port


