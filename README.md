# Company website

Website for a technology services company offering **website design and build**, **data services**, and **business automation and integration**.

The company name, logo and colours are placeholders ("Company Name", a dashed logo box, neutral greyscale) until the brand is decided. See [`website/BRIEF.md`](website/BRIEF.md).

## Structure

```
app.py                  Flask server: serves the site and receives contact-form enquiries
render.yaml             Render deployment blueprint (see DEPLOY.md)
DEPLOY.md               Hosting, email and custom-domain setup
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

The form posts JSON to `POST /api/contact`. Each valid enquiry is appended to `data/enquiries.jsonl` (not committed to git) and emailed to `ENQUIRY_TO` when the SMTP variables are set. See `.env.example` for the variables and `ENQUIRY_DIR` to store the file elsewhere.

## Deploy with a custom domain

See [DEPLOY.md](DEPLOY.md). The repo includes a `render.yaml` blueprint for Render, with step-by-step instructions for email settings, buying a domain and pointing it at the site.

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
