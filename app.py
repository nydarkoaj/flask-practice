"""Company website server.

Serves the static site in website/ and accepts contact-form enquiries at POST /api/contact.
Enquiries are appended to data/enquiries.jsonl (not committed to git).
"""
import json
import os
import re
from datetime import datetime, timezone

from flask import Flask, abort, jsonify, request, send_from_directory

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SITE_DIR = os.path.join(BASE_DIR, "website")
DATA_DIR = os.environ.get("ENQUIRY_DIR", os.path.join(BASE_DIR, "data"))
ENQUIRY_FILE = os.path.join(DATA_DIR, "enquiries.jsonl")
SERVICES = {
    "Website design and build",
    "Data services",
    "Business automation and integration",
    "More than one",
    "Other",
}
LIMITS = {"name": 120, "company": 160, "contact": 160, "message": 5000}

app = Flask(__name__, static_folder=None)


@app.get("/")
def index():
    return send_from_directory(SITE_DIR, "index.html")


@app.get("/<path:filename>")
def site_files(filename):
    # Only serve the public site assets, never the brief or video source files.
    if filename.endswith((".md", ".js")) or filename.startswith("video/promo.html"):
        abort(404)
    return send_from_directory(SITE_DIR, filename)


@app.post("/api/contact")
def contact():
    data = request.get_json(silent=True) or request.form.to_dict()
    enquiry = {k: str(data.get(k, "")).strip()[:limit] for k, limit in LIMITS.items()}
    enquiry["service"] = data.get("service") if data.get("service") in SERVICES else "Other"

    if data.get("website"):  # honeypot field: real visitors leave it empty
        return jsonify(ok=True)
    if not enquiry["name"]:
        return jsonify(ok=False, error="Enter your name."), 400
    if not re.search(r"@|\d{6,}", re.sub(r"[\s()+-]", "", enquiry["contact"])):
        return jsonify(ok=False, error="Enter a valid email address or phone number."), 400

    enquiry["received_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(ENQUIRY_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(enquiry, ensure_ascii=False) + "\n")
    return jsonify(ok=True)


if __name__ == "__main__":
    app.run(debug=True)
