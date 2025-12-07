# How to Run the Website Analysis Tool

## Quick Start Guide

### Step 1: Start the Backend Server

Open a **Terminal/Command Prompt** and navigate to the project:

```bash
cd C:\Users\LENOVO\Desktop\Crawler\backend
```

Activate the virtual environment:
```bash
venv\Scripts\activate
```

Start the backend server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**You should see:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Keep this terminal window open!** The backend must stay running.

---

### Step 2: Start the Frontend Server

Open a **NEW Terminal/Command Prompt** window (keep the backend running) and navigate to:

```bash
cd C:\Users\LENOVO\Desktop\Crawler\frontend
```

Start the frontend server:
```bash
npm run dev
```

**You should see:**
```
  ▲ Next.js 14.0.4
  - Local:        http://localhost:3000
  - Ready in X seconds
```

**Keep this terminal window open too!**

---

### Step 3: Open the Application

Open your web browser and go to:

**http://localhost:3000**

You should see the Website Analysis Tool homepage!

---

### Step 4: Run Your First Scan

1. Enter a website URL (e.g., `https://example.com`)
2. Set the maximum pages (start with 10-20 for testing)
3. Click **"Start Analysis"**
4. Wait for the scan to complete (usually 1-5 minutes)
5. View the results!

---

## Using the Batch Scripts (Easier Method)

If you prefer, you can use the batch scripts I created:

### Option A: Start Backend
Double-click: `start-backend.bat`

### Option B: Start Frontend  
Double-click: `start-frontend.bat`

**Note:** You need to run both scripts (in separate windows or one after the other).

---

## Troubleshooting

### Backend won't start?
- Make sure you're in the `backend` directory
- Make sure the virtual environment is activated (`venv\Scripts\activate`)
- Check if port 8000 is already in use

### Frontend won't start?
- Make sure you're in the `frontend` directory
- Run `npm install` first if you haven't
- Check if port 3000 is already in use

### Can't connect to backend?
- Make sure the backend is running on port 8000
- Check the backend terminal for errors
- Try accessing http://localhost:8000/api/health in your browser

### Scan fails?
- Check the backend terminal for error messages
- Try with a smaller website first (fewer pages)
- Make sure the URL starts with `http://` or `https://`

---

## Stopping the Application

1. **Stop Frontend:** Press `Ctrl+C` in the frontend terminal
2. **Stop Backend:** Press `Ctrl+C` in the backend terminal

---

## Quick Reference

| Service | URL | Port |
|---------|-----|------|
| Frontend | http://localhost:3000 | 3000 |
| Backend API | http://localhost:8000 | 8000 |
| API Docs | http://localhost:8000/docs | 8000 |

---

## What You Need Running

✅ **Two terminal windows:**
- Terminal 1: Backend server (uvicorn)
- Terminal 2: Frontend server (npm run dev)

✅ **One browser window:**
- http://localhost:3000

That's it! 🎉

