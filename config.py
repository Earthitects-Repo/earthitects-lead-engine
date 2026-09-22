"""
Earthitects Liquidity & ICP Lead Prospecting Engine - Configuration
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# Recipient & Sender settings
DEFAULT_RECIPIENT = "faraz.z@earthitects.com"
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL", DEFAULT_RECIPIENT)
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "")
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")

# Search Feeds & Google News RSS Queries (Real-time, zero-cost, no API key needed)
# Targeted specifically to Indian financial media, SEBI filings, IPOs, secondary exits, and CXOs.
RSS_QUERIES = [
    # 1. IPOs & DRHP filings with Offer For Sale (OFS = Promoters cashing out liquid wealth)
    {
        "category": "IPO & Liquidity Exits",
        "query": '(IPO OR DRHP OR "Offer for Sale" OR "OFS" OR "listing gain" OR "promoter stake sale") AND (founder OR promoter OR CEO) AND (India OR Bengaluru OR Mumbai)',
        "weight": 3
    },
    # 2. Startup Secondary Sales & ESOP Buybacks (Founders/early team pocketing cash)
    {
        "category": "Secondary Share Sales & Buybacks",
        "query": '("secondary sale" OR "secondary round" OR "ESOP buyback" OR "shares buyback" OR "cash exit") AND (founder OR startup OR employees) AND India',
        "weight": 3
    },
    # 3. Growth Stage Fundraises (Series B/C/D+ indicating ₹50-100 Cr+ minimum valuations)
    {
        "category": "Growth Fundraises & Valuations (₹50-100 Cr+)",
        "query": '("Series B" OR "Series C" OR "Series D" OR "unicorn" OR "soonicorn" OR "raised $" OR "raised ₹") AND (founder OR co-founder) AND (Bengaluru OR Bangalore OR India)',
        "weight": 2
    },
    # 4. Promoter Block Deals & Large Stake Sales
    {
        "category": "Promoter Block Deals & Liquidations",
        "query": '("promoter sells" OR "block deal" OR "stake offloaded" OR "bulk deal" OR "family office investment") AND (promoter OR founder) AND India',
        "weight": 3
    },
    # 5. Senior Tech / MNC CXO Leadership moves in Bengaluru & South India
    {
        "category": "Senior CXO & Executive Transitions",
        "query": '("appointed as CEO" OR "named Managing Director" OR "joins as VP" OR "named President" OR "promoted to CXO") AND (Bengaluru OR Bangalore OR Hyderabad)',
        "weight": 2
    },
    # 6. High-net-worth NRIs & Global Indian Founders
    {
        "category": "NRI & Global Indian Wealth",
        "query": '(NRI OR "Indian-origin" OR "diaspora") AND ("family office" OR "luxury real estate" OR "invests in India" OR "second home") AND (Singapore OR Dubai OR UAE OR London OR US)',
        "weight": 2
    }
]

# Dedicated RSS feeds from top Indian startup & business portals
DEDICATED_FEEDS = [
    {"source": "Entrackr", "url": "https://entrackr.com/feed/", "category": "Startup Exits & Funding"},
    {"source": "Inc42", "url": "https://inc42.com/feed/", "category": "Startup Exits & Funding"},
    {"source": "YourStory", "url": "https://yourstory.com/feed", "category": "Entrepreneurs & Exits"},
]

# Keywords for geographical prioritization
SOUTH_INDIA_HUBS = ["bengaluru", "bangalore", "karnataka", "coorg", "chikmagalur", "wayanad", "mysore", "hyderabad", "chennai"]
GLOBAL_NRI_HUBS = ["singapore", "dubai", "uae", "abu dhabi", "london", "uk", "bay area", "san francisco", "silicon valley", "california", "new york", "usa"]

# Archive & State Paths
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
SEEN_LEADS_FILE = os.path.join(DATA_DIR, "seen_leads.json")
PREVIEW_HTML_FILE = os.path.join(os.path.dirname(__file__), "preview_latest_digest.html")
