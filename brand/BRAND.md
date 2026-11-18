# Company brief (placeholder brand)

The company name, logo and design language are **not decided yet**. Everything uses placeholders:
- Name: "Company Name" (search and replace it in `index.html` and `video/promo.html`)
- Logo: dashed "LOGO" box
- Design: neutral greyscale, Inter for text and IBM Plex Mono for labels. All colours are tokens at the top of `index.html`, so the real palette can be dropped in later.

## What we market
1. **Website design and build**: company websites and online stores, mobile-friendly, search engine setup, hosting and maintenance.
2. **Data services**: pipelines, warehouses, cleaning and migration, dashboards and reporting.
3. **Business automation and integration**: API integrations, order/invoice/approval workflows, scheduled reports and alerts, document search assistants.

Also available (one line on the site): mobile apps, ERP and hospital management systems, stock and inventory systems.
Marketing analytics and the founder credentials section are removed for now.

## Tone
Serious and direct. Plain descriptions of what is delivered; no slogans. Layout uses ruled rows and a label column instead of cards.

## Files
- `index.html`: website (open directly, or run the Flask app and visit `/site/`)
- `video/promo.mp4`: 17-second promo (1280×720). Re-render with `node video/render.js` after editing `video/promo.html`.
- `video/still-*.png`: stills for thumbnails and social posts
