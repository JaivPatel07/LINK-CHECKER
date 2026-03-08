# ════════════════════════════════════════════════════
#  Link Checker — Python Flask API
#  Run:  pip install flask flask-cors requests beautifulsoup4
#        python api.py
#  API runs at: http://localhost:5000
# ════════════════════════════════════════════════════

from flask import Flask, request, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import concurrent.futures

app = Flask(__name__)
CORS(app)  # Allow JS frontend to call this API

# ── Helper: get status label ─────────────────────────
def get_label(status):
    if isinstance(status, int):
        if status < 300:   return "OK"
        if status < 400:   return "Redirect"
        if status == 403:  return "Forbidden"
        if status == 404:  return "Not Found"
        if status >= 500:  return "Server Error"
    return str(status)

# ── Helper: check a single link ──────────────────────
def check_link(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        res = requests.head(url, timeout=8, allow_redirects=True, headers=headers)
        # Fallback to GET if HEAD is blocked
        if res.status_code in [405, 403]:
            res = requests.get(url, timeout=8, headers=headers)
        return res.status_code
    except requests.exceptions.ConnectionError:
        return "Connection Error"
    except requests.exceptions.Timeout:
        return "Timeout"
    except Exception as e:
        return "Error"

# ── Route: GET /  ─────────────────────────────────────
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Link Checker API is running!",
        "usage": "POST /check with { url: 'https://example.com' }"
    })

# ── Route: POST /check ────────────────────────────────
# Receives: { "url": "https://example.com" }
# Returns:  { "total": 10, "working": 8, "broken": 2, "health": 80, "links": [...] }
@app.route("/check", methods=["POST"])
def check():
    data = request.get_json()

    # Validate input
    if not data or "url" not in data:
        return jsonify({ "error": "Please provide a URL in the request body." }), 400

    target_url = data["url"].strip()
    if not target_url.startswith("http"):
        target_url = "https://" + target_url

    # Step 1: Fetch the page
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        page = requests.get(target_url, timeout=10, headers=headers)
        soup = BeautifulSoup(page.text, "html.parser")
    except Exception as e:
        return jsonify({ "error": f"Could not fetch page: {str(e)}" }), 500

    # Step 2: Extract all links and images
    links = set()
    for tag in soup.find_all("a", href=True):
        try:
            full_url = urljoin(target_url, tag["href"])
            if full_url.startswith("http"):
                links.add(full_url)
        except:
            pass

    images = set()
    for tag in soup.find_all("img", src=True):
        try:
            full_url = urljoin(target_url, tag["src"])
            if full_url.startswith("http"):
                images.add(full_url)
        except:
            pass

    if not links and not images:
        return jsonify({ "error": "No links or images found on this page." }), 404

    # Step 3: Check each link and image
    # Use threading to check URLs concurrently for better performance
    def check_url_worker(url):
        status = check_link(url)
        is_ok  = isinstance(status, int) and status < 400
        label  = get_label(status)
        return {
            "url":    url,
            "status": status,
            "label":  label,
            "ok":     is_ok
        }

    # Set limits for checking
    links_to_check = list(links)[:100]
    images_to_check = list(images)[:100]

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        link_results = list(executor.map(check_url_worker, links_to_check))
        image_results = list(executor.map(check_url_worker, images_to_check))

    # Calculate link stats
    link_working = sum(1 for r in link_results if r["ok"])
    link_broken  = len(link_results) - link_working
    link_total  = len(link_results)
    link_health = round((link_working / link_total) * 100) if link_total > 0 else 0

    # Calculate image stats
    image_working = sum(1 for r in image_results if r["ok"])
    image_broken = len(image_results) - image_working
    image_total = len(image_results)

    # Step 4: Return JSON response to frontend
    return jsonify({
        "total":   link_total,
        "working": link_working,
        "broken":  link_broken,
        "health":  link_health,
        "links":   link_results,
        "image_stats": {
            "total": image_total,
            "working": image_working,
            "broken": image_broken,
        },
        "images": image_results
    })

# ── Start server ──────────────────────────────────────
if __name__ == "__main__":
    print("╔══════════════════════════════════════╗")
    print("║   🔗 Link Checker API — Running!     ║")
    print("║   http://localhost:5000              ║")
    print("╚══════════════════════════════════════╝")
    app.run(debug=True, port=5000)
