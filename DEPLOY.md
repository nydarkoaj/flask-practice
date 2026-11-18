# Deploying the website with a custom domain

The site runs on [Render](https://render.com) as a small Flask web service. Render builds from this GitHub repository, redeploys on every push, and issues free HTTPS certificates for your domain.

Rough cost: Render free plan ($0, sleeps after 15 minutes idle, so the first visit takes ~30 seconds) or Starter (about $7/month, always on). Domain about $10–20/year for `.com`.

---

## 1. Get the code onto the deploy branch

`render.yaml` deploys the `dev` branch. Merge `claude/ny-tech-company-brand-v0hpn0` into `dev` first, or change `branch:` in `render.yaml` to the branch you want live.

## 2. Create the Render service

1. Sign up at https://render.com with your GitHub account.
2. Click **New +** → **Blueprint**, then pick this repository.
3. Render reads `render.yaml` and asks for the values marked `sync: false`:

   | Variable | What to enter |
   |---|---|
   | `ENQUIRY_TO` | The inbox that should receive enquiries |
   | `SMTP_HOST` | Your email provider's SMTP server (see below) |
   | `SMTP_USER` | The sending account's email address |
   | `SMTP_PASSWORD` | An app password for that account, not your normal password |
   | `SMTP_FROM` | Optional. Leave empty to send from `SMTP_USER` |

4. Click **Apply**. After the build, the site is live at `https://company-website.onrender.com` (or the name Render assigns).
5. Open the site, send a test enquiry, and check it arrives in `ENQUIRY_TO`.

**SMTP settings for common providers**

| Provider | `SMTP_HOST` | Notes |
|---|---|---|
| Google Workspace / Gmail | `smtp.gmail.com` | Turn on 2-step verification, then create an app password at myaccount.google.com/apppasswords |
| Zoho Mail | `smtp.zoho.com` | Create an app-specific password in Zoho account security |
| Microsoft 365 | `smtp.office365.com` | SMTP AUTH must be enabled for the mailbox |
| Brevo (free transactional email) | `smtp-relay.brevo.com` | Use the SMTP key from Brevo as the password |

All use port `587`. If SMTP variables are empty, the form still saves enquiries to `data/enquiries.jsonl`, but on Render's free plan that file is wiped on each deploy, so set up email before launch.

## 3. Buy the domain

Once the company name is settled, buy the domain from any registrar:

- **`.com` and most others:** Cloudflare Registrar (at-cost pricing), Namecheap, or Porkbun.
- **`.com.gh`:** through an accredited Ghanaian registrar listed by NIC Ghana (nic.gh). Allow a few days and have business registration documents ready.

Buying both `yourname.com` and `yourname.com.gh` and forwarding one to the other is common for Ghana-based companies.

## 4. Connect the domain

1. In Render, open the service → **Settings** → **Custom Domains** → **Add Custom Domain**. Add both `yourdomain.com` and `www.yourdomain.com`.
   (Or uncomment the `domains:` block in `render.yaml`, replace `example.com`, and push.)
2. Render shows the DNS records to create. They normally look like this:

   | Type | Name / Host | Value |
   |---|---|---|
   | `A` | `@` (root domain) | The IP address Render shows (currently `216.24.57.1`) |
   | `CNAME` | `www` | `company-website.onrender.com` (your service's address) |

   Always copy the exact values from the Render dashboard; they take precedence over this table.
3. Add those records in your registrar's DNS settings. If using Cloudflare DNS, set the records to **DNS only** (grey cloud) so Render can issue the certificate.
4. Back in Render, click **Verify**. DNS usually updates within an hour (up to 48 hours). Render then issues the HTTPS certificate automatically.
5. Visit `https://yourdomain.com` and `https://www.yourdomain.com` to confirm both work.

## 5. Before launch checklist

- [ ] Replace `Company Name` in `website/index.html` and `website/video/promo.html` (re-render the video after editing)
- [ ] Replace the logo placeholder in the site header
- [ ] Add a phone number and email address to the contact section
- [ ] Set the SMTP variables and send a test enquiry
- [ ] Add the domain and confirm HTTPS works on both root and `www`
- [ ] Optional: set up a business email on the domain (Google Workspace or Zoho Mail) and use it for `ENQUIRY_TO`

## Running elsewhere

The included `Dockerfile` runs the same app with gunicorn on any container host (Railway, Fly.io, a VPS):

```bash
docker build -t company-website .
docker run -p 5000:5000 -e ENQUIRY_TO=... -e SMTP_HOST=... -e SMTP_USER=... -e SMTP_PASSWORD=... -v enquiries:/data company-website
```
