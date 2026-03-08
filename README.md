# 🔗 Link Checker

A web-based link checker with a Python/Flask backend and a clean HTML frontend.

## Project Structure

```
link-checker/
├── app.py            ← Flask backend (runs the actual link checking)
├── index.html        ← Frontend (open in browser after starting Flask)
├── requirements.txt  ← Python dependencies
└── README.md
```

## How It Works

```
Browser (index.html)
      │
      │  POST /scan  { "url": "https://example.com" }
      ▼
Flask (app.py) on localhost:5000
      │
      ├── Fetches the target page
      ├── Extracts all links
      ├── Checks each link's HTTP status
      │
      └── Returns JSON { total, working, broken, health, results[] }
      │
      ▼
Browser renders results + insight + CSV export
```

## Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Flask backend
```bash
python app.py
```
You'll see:
```
╔══════════════════════════════════╗
║   🔗 LINK CHECKER — Flask API   ║
║   Running on http://localhost:5000║
╚══════════════════════════════════╝
```

### 3. Open the frontend
Open `index.html` in your browser (double-click it or use Live Server).

### 4. Use it
- Enter any URL (e.g. `https://python.org`)
- Click **Scan Links**
- View results, filter by Working/Broken, export to CSV

## API Reference

### `POST /scan`
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
  "results": [
    { "url": "https://example.com/page", "status": 200, "ok": true },
    { "url": "https://example.com/missing", "status": 404, "ok": false }
  ]
}
```
