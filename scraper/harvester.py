"""
Liquidity Harvester: Fetches real-time market filings, IPO news, secondary exits, and funding alerts.
"""
import urllib.parse
import feedparser
import requests
from bs4 import BeautifulSoup
import json
import os
import re
from datetime import datetime
from config import RSS_QUERIES, DEDICATED_FEEDS, SEEN_LEADS_FILE, DATA_DIR

class LiquidityHarvester:
    def __init__(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        self.seen_leads = self._load_seen_leads()

    def _load_seen_leads(self):
        if os.path.exists(SEEN_LEADS_FILE):
            try:
                with open(SEEN_LEADS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def save_seen_leads(self):
        try:
            with open(SEEN_LEADS_FILE, "w", encoding="utf-8") as f:
                json.dump(self.seen_leads, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Failed to save seen leads cache: {e}")

    def clean_html_text(self, raw_html):
        if not raw_html:
            return ""
        soup = BeautifulSoup(raw_html, "html.parser")
        text = soup.get_text(separator=" ")
        return re.sub(r"\s+", " ", text).strip()

    def fetch_google_news_rss(self, query, category):
        """Fetches real-time articles from Google News RSS using targeted query dorks."""
        encoded_query = urllib.parse.quote(query)
        rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-IN&gl=IN&ceid=IN:en"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        articles = []
        try:
            feed = feedparser.parse(rss_url, request_headers=headers)
            for entry in feed.entries[:12]:  # Top 12 per query
                title = entry.get("title", "")
                link = entry.get("link", "")
                published = entry.get("published", "")
                summary = self.clean_html_text(entry.get("summary", ""))
                
                # Source extraction from title (Google News formats titles as "Headline - Publisher")
                source = "Google News"
                if " - " in title:
                    parts = title.rsplit(" - ", 1)
                    title = parts[0]
                    source = parts[1]

                article_id = link or title
                articles.append({
                    "id": article_id,
                    "title": title,
                    "link": link,
                    "source": source,
                    "published": published,
                    "summary": summary,
                    "category": category
                })
        except Exception as e:
            print(f"Error fetching Google News query '{query[:30]}...': {e}")

        return articles

    def fetch_dedicated_feed(self, feed_info):
        """Fetches articles from direct RSS feeds (Inc42, Entrackr, YourStory)."""
        articles = []
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            feed = feedparser.parse(feed_info["url"], request_headers=headers)
            for entry in feed.entries[:10]:
                title = entry.get("title", "")
                link = entry.get("link", "")
                published = entry.get("published", "")
                summary = self.clean_html_text(entry.get("summary", ""))

                article_id = link or title
                articles.append({
                    "id": article_id,
                    "title": title,
                    "link": link,
                    "source": feed_info["source"],
                    "published": published,
                    "summary": summary,
                    "category": feed_info["category"]
                })
        except Exception as e:
            print(f"Error fetching feed '{feed_info['source']}': {e}")
        return articles

    def harvest_all(self, deduplicate=True):
        """Harvests from all queries and sources, deduplicating past sightings."""
        raw_articles = []

        print(f"[*] Harvesting liquidity news from {len(RSS_QUERIES)} targeted financial dorks...")
        for item in RSS_QUERIES:
            arts = self.fetch_google_news_rss(item["query"], item["category"])
            raw_articles.extend(arts)

        print(f"[*] Harvesting dedicated Indian startup feeds ({len(DEDICATED_FEEDS)} sources)...")
        for f_info in DEDICATED_FEEDS:
            arts = self.fetch_dedicated_feed(f_info)
            raw_articles.extend(arts)

        unique_articles = []
        current_seen = set()

        for art in raw_articles:
            art_id = art["id"]
            title_norm = re.sub(r"[^a-zA-Z0-9]", "", art["title"]).lower()[:60]

            # In-batch duplicate check
            if art_id in current_seen or title_norm in current_seen:
                continue

            current_seen.add(art_id)
            current_seen.add(title_norm)

            # Historical duplicate check
            if deduplicate and (art_id in self.seen_leads or title_norm in self.seen_leads):
                continue

            unique_articles.append(art)

        print(f"[+] Total fresh raw articles captured: {len(unique_articles)}")
        return unique_articles

    def mark_as_seen(self, articles):
        """Records articles into the historical seen cache."""
        now_str = datetime.now().isoformat()
        for art in articles:
            art_id = art.get("id", "")
            title_norm = re.sub(r"[^a-zA-Z0-9]", "", art.get("title", "")).lower()[:60]
            if art_id:
                self.seen_leads[art_id] = now_str
            if title_norm:
                self.seen_leads[title_norm] = now_str
        self.save_seen_leads()
