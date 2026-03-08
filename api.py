# ════════════════════════════════════════════════════
#  LinkScan — Python Flask API
#  Run:  pip install flask flask-cors requests beautifulsoup4
#        python api.py
#  API runs at: http://localhost:5000
# ════════════════════════════════════════════════════

from flask import Flask, request, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import requests
import concurrent.futures
import time
import ipaddress
import socket

app = Flask(__name__)
CORS(app)

MAX_LINKS  = 150
MAX_IMAGES = 150
MAX_WORKERS = 15

def is_safe_url(url):
    try:
        parsed = urlparse(url)
        hostname = parsed.hostname
        if not hostname:
            return False
        addr = socket.getaddrinfo(hostname, None, socket.AF_UNSPEC, socket.SOCK_STREAM)
        for family, _, _, _, sockaddr in addr:
            ip = ipaddress.ip_address(sockaddr[0])
            if ip.is_private or ip.is_loopback or ip.is_reserved or ip.is_link_local:
                return False
        return True
    except (socket.gaierror, ValueError, OSError):
        return False

def get_label(status):
    if isinstance(status, int):
        if status < 300:   return "OK"
        if status < 400:   return "Redirect"
        if status == 403:  return "Forbidden"
        if status == 404:  return "Not Found"
        if status >= 500:  return "Server Error"
    return str(status)

def check_link(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        start = time.monotonic()
        res = requests.head(url, timeout=8, allow_redirects=True, headers=headers)
        if res.status_code in (405, 403):
            res = requests.get(url, timeout=8, headers=headers, stream=True)
        elapsed = round((time.monotonic() - start) * 1000)
        return res.status_code, elapsed
    except requests.exceptions.ConnectionError:
        return "Connection Error", 0
    except requests.exceptions.Timeout:
        return "Timeout", 0
    except requests.exceptions.RequestException:
        return "Error", 0

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Link Checker API is running!",
        "usage": "POST /check with { url: 'https://example.com' }"
    })

@app.route("/check", methods=["POST"])
def check():
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({ "error": "Please provide a URL in the request body." }), 400

    target_url = data["url"].strip()
    if not target_url.startswith("http"):
        target_url = "https://" + target_url

    parsed = urlparse(target_url)
    if not parsed.scheme or not parsed.hostname:
        return jsonify({ "error": "Invalid URL format." }), 400

    if not is_safe_url(target_url):
        return jsonify({ "error": "Cannot scan internal or private network addresses." }), 400

    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        page = requests.get(target_url, timeout=10, headers=headers)
        soup = BeautifulSoup(page.text, "html.parser")
    except requests.exceptions.RequestException as e:
        return jsonify({ "error": f"Could not fetch page: {str(e)}" }), 502

    links = set()
    for tag in soup.find_all("a", href=True):
        href = tag["href"]
        full_url = urljoin(target_url, href)
        if full_url.startswith("http"):
            links.add(full_url)

    images = set()
    for tag in soup.find_all("img", src=True):
        src = tag["src"]
        full_url = urljoin(target_url, src)
        if full_url.startswith("http"):
            images.add(full_url)

    if not links and not images:
        return jsonify({ "error": "No links or images found on this page." }), 404

    def check_url_worker(url):
        status, time_ms = check_link(url)
        is_ok  = isinstance(status, int) and status < 400
        label  = get_label(status)
        return {
            "url":     url,
            "status":  status,
            "label":   label,
            "ok":      is_ok,
            "time_ms": time_ms
        }

    links_to_check  = list(links)[:MAX_LINKS]
    images_to_check = list(images)[:MAX_IMAGES]

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        link_results  = list(executor.map(check_url_worker, links_to_check))
        image_results = list(executor.map(check_url_worker, images_to_check))

    link_results.sort(key=lambda r: (r["ok"], r["url"]))
    image_results.sort(key=lambda r: (r["ok"], r["url"]))

    link_working = sum(1 for r in link_results if r["ok"])
    link_broken  = len(link_results) - link_working
    link_total  = len(link_results)
    link_health = round((link_working / link_total) * 100) if link_total > 0 else 0

    image_working = sum(1 for r in image_results if r["ok"])
    image_broken = len(image_results) - image_working
    image_total = len(image_results)

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

if __name__ == "__main__":
    print("╔══════════════════════════════════════╗")
    print("║   🔗 Link Checker API — Running!     ║")
    print("║   http://localhost:5000              ║")
    print("╚══════════════════════════════════════╝")
    app.run(debug=True, port=5000)
