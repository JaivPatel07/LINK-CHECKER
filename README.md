# 🔗 LinkScan — Link & Image Health Checker

A web-based tool that audits **broken links** and **missing images** on any webpage. Built with a Python/Flask backend and a modern dark-themed frontend.

## Features

- Scans all `<a>` links and `<img>` sources on a page
- Concurrent checking with a thread pool for speed
- Health score, working/broken stats for both links and images
- Filter results by status (All / Working / Broken)
- Export results to CSV
- Responsive dark UI with smooth animations

## Project Structure

```
LINK-CHECKER/
├── api.py            ← Flask backend (link & image checking API)
├── index.html        ← Frontend (open in browser after starting Flask)
├── requirements.txt  ← Python dependencies
├── .gitignore
└── README.md
```

## How It Works

```
Browser (index.html)
      │
      │  POST /check  { "url": "https://example.com" }
      ▼
Flask (api.py) on localhost:5000
      │
      ├── Fetches the target page
      ├── Extracts all <a> links and <img> sources
      ├── Checks each URL's HTTP status (concurrent)
      │
      └── Returns JSON { total, working, broken, health, links[], image_stats, images[] }
      │
      ▼
Browser renders results with stats, filters & CSV export
```

## Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Flask backend
```bash
python api.py
```
You'll see:
```
╔══════════════════════════════════════╗
║   🔗 Link Checker API — Running!    ║
║   http://localhost:5000              ║
╚══════════════════════════════════════╝
```

### 3. Open the frontend
Open `index.html` in your browser (double-click it or use Live Server).

### 4. Use it
- Enter any URL (e.g. `https://python.org`)
- Click **Scan →**
- View link and image stats, filter by Working/Broken, switch between Links & Images tabs
- Export results as CSV

## API Reference

### `GET /`
Returns a status message confirming the API is running.

### `POST /check`
**Request body:**
```json
{ "url": "https://example.com" }
```
**Response:**
```json
{
  "total": 42,
  "working": 39,
  "broken": 3,
  "health": 93,
  "links": [
    { "url": "https://example.com/page", "status": 200, "label": "OK", "ok": true, "time_ms": 245 },
    { "url": "https://example.com/missing", "status": 404, "label": "Not Found", "ok": false, "time_ms": 120 }
  ],
  "image_stats": {
    "total": 10,
    "working": 9,
    "broken": 1
  },
  "images": [
    { "url": "https://example.com/logo.png", "status": 200, "label": "OK", "ok": true, "time_ms": 80 }
  ]
}
```

## Tech Stack

- **Backend:** Python, Flask, requests, BeautifulSoup4
- **Frontend:** Vanilla HTML/CSS/JS
- **Fonts:** Syne, DM Mono (Google Fonts)
