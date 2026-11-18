# Company website

Website for a technology services company offering **website design and build**, **data services**, and **business automation and integration**.

The company name, logo and colours are placeholders ("Company Name", a dashed logo box, neutral greyscale) until the brand is decided. See [`website/BRIEF.md`](website/BRIEF.md).

## Structure

```
app.py                  Flask server: serves the site and receives contact-form enquiries
website/index.html      The website (single page)
website/BRIEF.md        Positioning, services, tone and placeholder notes
website/video/          17-second promo video, its HTML source and render script
archive/flask-practice/ The original Flask practice project, kept for reference
```

## Run locally

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask --app app run --debug
```

Open http://127.0.0.1:5000. You can also open `website/index.html` directly in a browser; the contact form only sends when the Flask app is running.

## Contact form

The form posts JSON to `POST /api/contact`. Valid enquiries are appended to `data/enquiries.jsonl` (one JSON object per line, not committed to git). Set `ENQUIRY_DIR` to store them elsewhere.

Next step before launch: forward enquiries to an inbox (for example via an SMTP or email API call in `app.py`).

## Docker

```bash
docker build -t company-website .
docker run -p 5000:5000 -v enquiries:/data company-website
```

The container runs the app with gunicorn and writes enquiries to the `/data` volume.

## Re-render the promo video

Requires Node with Playwright and ffmpeg.

```bash
node website/video/render.js
```

Edit `website/video/promo.html` first to change the text, then re-render. This writes `promo.mp4` and the still images.

## Replacing the placeholders

- **Name:** search for `Company Name` in `website/index.html` and `website/video/promo.html`.
- **Logo:** replace the `.logo-ph` box in the header.
- **Colours and fonts:** edit the tokens at the top of the `<style>` block in `website/index.html`.
