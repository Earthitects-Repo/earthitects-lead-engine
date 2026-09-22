"""
Earthitects Liquidity & ICP Lead Prospecting Engine - Master Runner
Usage:
    python run_engine.py --preview        # Harvests live feeds, builds digest, and opens preview in browser
    python run_engine.py --send           # Harvests live feeds, builds digest, and emails faraz.z@earthitects.com
    python run_engine.py --force          # Re-scores without skipping previously seen articles
"""
import argparse
import sys
import io

# Ensure UTF-8 output even on legacy Windows terminals
if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from scraper.harvester import LiquidityHarvester
from analyzer.icp_scorer import ICPScorer
from mailer.digest_builder import DigestBuilder
from mailer.dispatcher import MailDispatcher

def main():
    parser = argparse.ArgumentParser(description="Earthitects Liquidity & ICP Lead Prospecting Engine")
    parser.add_argument("--preview", action="store_true", help="Generate HTML digest and open in browser")
    parser.add_argument("--send", action="store_true", help="Send email digest to faraz.z@earthitects.com via SMTP")
    parser.add_argument("--force", action="store_true", help="Bypass deduplication cache to re-score all feeds")
    args = parser.parse_args()

    print("=" * 70)
    print("EARTHITECTS • UHNW LIQUIDITY & ICP PROSPECTING ENGINE")
    print("=" * 70)

    # 1. Harvest Articles
    harvester = LiquidityHarvester()
    articles = harvester.harvest_all(deduplicate=not args.force)

    if not articles:
        print("[i] No new articles found since last cycle.")
        if not args.force:
            print("[i] Use --force if you want to re-process all feeds.")
            return

    # 2. Score & Extract Entities
    scorer = ICPScorer()
    print(f"[*] Analyzing and scoring {len(articles)} articles against Earthitects ICP...")
    scored_leads = []
    for art in articles:
        lead = scorer.score_lead(art)
        scored_leads.append(lead)

    # Sort descending by score
    scored_leads.sort(key=lambda x: x["score"], reverse=True)

    vip_leads = [l for l in scored_leads if l["score"] >= 7]
    strong_leads = [l for l in scored_leads if 5 <= l["score"] < 7]

    print("\n" + "-" * 70)
    print(f"SUMMARY REPORT: {len(vip_leads)} VIP Leads (Score >= 7) | {len(strong_leads)} Strong Pipeline Leads")
    print("-" * 70)
    for idx, lead in enumerate(vip_leads[:6], 1):
        print(f"{idx}. [{lead['score']}/10] {lead['company']} ({lead['persona_type']})")
        print(f"   Event: {lead['event_type']} | Scale: {lead['amount_str']}")
        print(f"   Title: {lead['title'][:70]}...")
        print(f"   Link:  {lead['link']}")
        print()

    # 3. Build HTML Digest
    builder = DigestBuilder()
    html_content = builder.build_digest(scored_leads, total_scanned=len(articles))

    # 4. Dispatch or Preview
    dispatcher = MailDispatcher()
    
    # Save preview locally
    dispatcher.save_preview(html_content, open_browser=args.preview)

    # Send email if requested or if configured
    if args.send:
        subject = f"Earthitects Lead Digest: {len(vip_leads)} VIP Liquidity Leads Found ({len(articles)} Scanned)"
        dispatcher.send_email(html_content, subject=subject)
    else:
        print("\n[i] Run with '--send' to dispatch email to faraz.z@earthitects.com")
        print(f"[i] To inspect results in browser, open preview_latest_digest.html or run with '--preview'")

    # Mark as seen so we don't repeat alerts tomorrow
    if not args.force:
        harvester.mark_as_seen(articles)

    print("\n[SUCCESS] Lead intelligence cycle complete.")

if __name__ == "__main__":
    main()
