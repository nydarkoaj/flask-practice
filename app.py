"""Company website server.

Serves the static site in website/ and accepts contact-form enquiries at POST /api/contact.
Each enquiry is appended to data/enquiries.jsonl (not committed to git) and, when SMTP
settings are present, emailed to ENQUIRY_TO. See DEPLOY.md for the environment variables.
"""
import json
import logging
import os
import re
import smtplib
from datetime import datetime, timezone
from email.message import EmailMessage

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
log = logging.getLogger("website")


def email_enquiry(enquiry):
    """Email the enquiry if SMTP is configured. Returns True when sent or not configured."""
    host, to = os.environ.get("SMTP_HOST"), os.environ.get("ENQUIRY_TO")
    if not host or not to:
        return True
    msg = EmailMessage()
    msg["Subject"] = f"Website enquiry: {enquiry['service']} from {enquiry['name']}"
    msg["From"] = os.environ.get("SMTP_FROM") or os.environ.get("SMTP_USER") or to
    msg["To"] = to
    if "@" in enquiry["contact"]:
        msg["Reply-To"] = enquiry["contact"]
    msg.set_content("\n".join(f"{k.replace('_', ' ').title()}: {v}" for k, v in enquiry.items()))
    try:
        with smtplib.SMTP(host, int(os.environ.get("SMTP_PORT", "587")), timeout=15) as smtp:
            smtp.starttls()
            if os.environ.get("SMTP_USER"):
                smtp.login(os.environ["SMTP_USER"], os.environ.get("SMTP_PASSWORD", ""))
            smtp.send_message(msg)
        return True
    except Exception:  # keep the enquiry on disk and tell the visitor to use another channel
        log.exception("Could not email enquiry")
        return False


@app.after_request
def security_headers(resp):
    resp.headers.setdefault("X-Content-Type-Options", "nosniff")
    resp.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    resp.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
    if request.headers.get("X-Forwarded-Proto") == "https":
        resp.headers.setdefault("Strict-Transport-Security", "max-age=31536000")
    return resp


@app.get("/healthz")
def healthz():
    return "ok"


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
    if not email_enquiry(enquiry):
        return jsonify(ok=False, error="The enquiry could not be sent. Please contact us by phone or email."), 502
    return jsonify(ok=True)


if __name__ == "__main__":
    app.run(debug=True)
