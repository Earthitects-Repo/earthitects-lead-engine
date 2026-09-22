# Earthitects UHNW Liquidity & ICP Lead Prospecting Engine

An automated, zero-cost intelligence system designed for **Earthitects** to identify and qualify ultra-high-net-worth (UHNW) prospects who have experienced recent liquidity events (IPOs, DRHP Offer for Sale filings, startup secondary share sales, promoter block deals, and executive transitions).

---

## 🎯 ICP Alignment (Handwritten Matrix)

The engine scores every public event against your exact criteria:
- **Budget / Deal Scale $\ge$ ₹9.5 Cr**: `+3 Points`
- **Company Valuation $\ge$ ₹50–100 Cr+ / Founder**: `+3 Points`
- **Location**: Bengaluru / Karnataka / South India (`+2 Points`) or Senior NRI (`+1 Point`)
- **Active Liquidity Window / Timeline $\le$ 12 Months**: `+2 Points`
- **Nature / Estate / Second Home Motive**: `+2 Points`

**Target Priority**: Leads with **Score $\ge$ 7** are classified as **Tier 1: VIP Priority Leads**.

---

## 🚀 Quick Start (Running Manually)

The engine is installed at:
`C:\Users\Systems\.gemini\antigravity\scratch\earthitects-lead-engine`

### 1. View Fresh Leads in Your Browser (No Email Setup Needed)
```powershell
cd C:\Users\Systems\.gemini\antigravity\scratch\earthitects-lead-engine
.\.venv\Scripts\python.exe run_engine.py --preview
```
This scans live feeds, calculates scores, extracts promoter/deal data, and immediately opens the generated luxury HTML briefing (`preview_latest_digest.html`) in your default web browser.

### 2. Dispatch Live Email to `faraz.z@earthitects.com`
```powershell
.\.venv\Scripts\python.exe run_engine.py --send
```

---

## 📬 Configuring Email Delivery (0-Cost SMTP)

Copy `.env.example` to `.env`:
```powershell
Copy-Item .env.example .env
```
Open `.env` and fill in your preferred outgoing email credentials:

### Recommended: Google Workspace / Gmail App Password (Free)
1. Go to your Google Account -> **Security** -> **2-Step Verification**.
2. Scroll to the bottom and create an **App Password** (name it `Earthitects Lead Engine`).
3. Set in `.env`:
   ```env
   RECIPIENT_EMAIL=faraz.z@earthitects.com
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your_email@earthitects.com
   SMTP_PASSWORD=your_16_char_app_password
   SENDER_EMAIL=your_email@earthitects.com
   ```

*(Alternative options for Office 365, Brevo, or SendGrid are also documented in `.env.example`).*

---

## ⏰ Automated Scheduling (Zero-Cost, Runs Daily at 8:00 AM IST)

### Option A: Local PC (Windows Task Scheduler)
Run the included PowerShell script once as Administrator:
```powershell
powershell -ExecutionPolicy Bypass -File .\setup_scheduler.ps1
```
This registers a daily task that runs silently in the background every morning at 8:00 AM IST.

### Option B: Cloud Automation (GitHub Actions)
If you push this folder to a private GitHub repository, the included `.github/workflows/daily_lead_digest.yml` will run automatically every morning at 8:00 AM IST on GitHub's cloud servers—**no need to keep your PC on**.

---

## 🛡️ Strategic Advisor Positioning
For every qualified prospect, the engine automatically pre-drafts an advisory outreach icebreaker featuring your handwritten discovery questions:
1. *"What does an ideal weekend or holiday look like for your family today?"*
2. *"When you think about a second home, what matters more to you: absolute privacy, effortless management, or multi-generational legacy?"*
