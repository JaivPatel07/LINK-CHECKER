# LinkScan - Link and Image Health Checker

LinkScan checks a webpage for broken links and broken images.
It uses a Flask API (`api.py`) and a static frontend (`index.html` + `style.css`).

## Current Features

- Scans `<a href>` links and `<img src>` images from a target URL
- Concurrent URL checking using `ThreadPoolExecutor`
- Link summary cards: total, working, broken, health score
- Image summary cards: total, loading, broken
- Result tabs: `Links` and `Images`
- Filters: `All`, `Working`, `Broken`
- CSV export for active tab results
- Light/Dark theme toggle (saved in browser `localStorage`)
- Inline GitHub source icon in footer
- Responsive UI for desktop and mobile

## Project Structure

```text
LINK-CHECKER/
  api.py
  index.html
  style.css
  requirements.txt
  README.md
```

## Requirements

- Python 3.10+

Install dependencies:

```bash
pip install -r requirements.txt
```

`requirements.txt` currently includes:

- `flask>=3.0`
- `flask-cors>=4.0`
- `requests>=2.31`
- `beautifulsoup4>=4.12`

## Run Locally

1. Start backend:

```bash
python api.py
```

2. Open frontend:

- Open `index.html` in a browser.
- The frontend calls API at `http://localhost:5000/check`.

## UI Walkthrough (Screenshots/GIF)

### 1. Scan

1. Enter a URL in the input field (for example, `https://python.org`).
2. Click `Scan`.
3. Wait for results to load in stats cards and list.

Screenshot/GIF placeholder:

```text
docs/media/scan.gif
```

### 2. Switch Theme

1. Click the top-right theme toggle button (`Light` or `Dark`).
2. Confirm colors update across cards, toolbar, and results.
3. Refresh page to verify theme preference is remembered.

Screenshot/GIF placeholder:

```text
docs/media/switch-theme.gif
```

### 3. Export CSV

1. Run a scan first.
2. Choose tab: `Links` or `Images`.
3. Click `Export CSV`.
4. Confirm file downloads as `linkscan-<tab>-YYYY-MM-DD.csv`.

Screenshot/GIF placeholder:

```text
docs/media/export-csv.gif
```

Tip: Replace the placeholder paths with actual screenshot or GIF files after you add them.

## API

### `GET /`

Health/status endpoint.

### `POST /check`

Request body:

```json
{ "url": "https://example.com" }
```

Response shape:

```json
{
  "total": 0,
  "working": 0,
  "broken": 0,
  "health": 0,
  "links": [],
  "image_stats": {
    "total": 0,
    "working": 0,
    "broken": 0
  },
  "images": []
}
```

Each link/image result contains:

- `url`
- `status` (HTTP code or error text)
- `label`
- `ok` (boolean)
- `time_ms`

## Backend Rules and Limits

- Rejects invalid URLs
- Blocks private/internal/loopback/reserved/link-local targets
- Max scan size:
  - `MAX_LINKS = 150`
  - `MAX_IMAGES = 150`
- Parallel workers:
  - `MAX_WORKERS = 15`

## Notes

- For some servers, `HEAD` can fail (`405`/`403`), so API falls back to `GET`.
- Results are sorted with broken items first for faster troubleshooting.
- If no links/images are found, API returns an error message.
