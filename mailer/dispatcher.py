"""
Mailer Dispatcher: Sends the HTML intelligence digest to faraz.z@earthitects.com via SMTP
and saves a local browser preview.
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import webbrowser
from config import (
    RECIPIENT_EMAIL, SENDER_EMAIL, SMTP_HOST,
    SMTP_PORT, SMTP_USER, SMTP_PASSWORD, PREVIEW_HTML_FILE
)

class MailDispatcher:
    def __init__(self):
        self.recipient = RECIPIENT_EMAIL
        self.sender = SENDER_EMAIL or SMTP_USER

    def save_preview(self, html_content, open_browser=False):
        """Saves a local HTML file for instant offline preview."""
        with open(PREVIEW_HTML_FILE, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"[+] Saved local HTML digest preview at: {PREVIEW_HTML_FILE}")
        if open_browser:
            webbrowser.open(f"file:///{os.path.abspath(PREVIEW_HTML_FILE)}")

    def send_email(self, html_content, subject=None):
        """Dispatches email via standard SMTP."""
        if not subject:
            subject = "Earthitects • UHNW Liquidity & ICP Leads Digest"

        if not SMTP_USER or not SMTP_PASSWORD:
            print("[!] SMTP credentials not detected in .env.")
            print(f"[i] To send emails automatically, add your SMTP details to .env (see .env.example).")
            print(f"[i] The digest has been saved to: {PREVIEW_HTML_FILE}")
            return False

        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = self.sender or SMTP_USER
            msg["To"] = self.recipient

            part = MIMEText(html_content, "html", "utf-8")
            msg.attach(part)

            print(f"[*] Connecting to {SMTP_HOST}:{SMTP_PORT} for delivery to {self.recipient}...")
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
                server.starttls()
                server.login(SMTP_USER, SMTP_PASSWORD)
                server.sendmail(msg["From"], [self.recipient], msg.as_string())

            print(f"[OK] Successfully emailed digest to {self.recipient}!")
            return True
        except Exception as e:
            print(f"[FAIL] Failed to dispatch email: {e}")
            return False
