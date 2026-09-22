"""
ICP Scorer & Entity Intelligence Extractor
Codifies the Earthitects ICP rules, scores liquidity events, and crafts bespoke advisor outreach angles.
"""
import re
from config import SOUTH_INDIA_HUBS, GLOBAL_NRI_HUBS

class ICPScorer:
    def __init__(self):
        # High-liquidity trigger terms indicating money directly in pockets
        self.liquidity_patterns = [
            (r"\b(offer for sale|ofs)\b", "IPO Offer for Sale (OFS - Promoter Cash-Out)", 3),
            (r"\b(secondary sale|secondary round|esop buyback|shares? buyback)\b", "Secondary Liquidity / Buyback", 3),
            (r"\b(promoter (?:sells|offloaded|divests)|block deal|bulk deal)\b", "Promoter Stake Sale", 3),
            (r"\b(ipo|drhp|listing|market debut|sebi approval)\b", "Upcoming / Recent IPO", 2),
            (r"\b(series [b-z]|raises? \$[0-9]+(?:\.[0-9]+)?\s*(?:m|million|cr|crore)|unicorn|soonicorn)\b", "Growth Fundraise (Valuation ₹50-100Cr+)", 2),
            (r"\b(acquired by|merger|buyout|exit)\b", "M&A Corporate Exit", 3),
            (r"\b(appointed (?:as )?ceo|named md|named president|promoted to cxo|joins as vp)\b", "CXO / Executive Transition", 2),
        ]

        # Financial value extraction patterns
        self.k_cr_pattern = r"([0-9,]+(?:\.[0-9]+)?)\s*(?:k|thousand)\s*(?:cr|crore|crores)"
        self.cr_pattern = r"(?:₹|rs\.?)\s*([0-9,]+(?:\.[0-9]+)?)\s*(?:cr|crore|crores)?"
        self.generic_cr_pattern = r"([0-9,]+(?:\.[0-9]+)?)\s*(?:cr|crore|crores)"
        self.usd_m_pattern = r"(?:\$|usd)\s*([0-9,]+(?:\.[0-9]+)?)\s*(?:m|million|b|billion)?"

    def extract_deal_amount(self, text):
        """Extracts any mentioned financial figure and normalizes to estimated Crores (INR)."""
        text_lower = text.lower()

        # Check for '1.5k crore' pattern
        k_match = re.search(self.k_cr_pattern, text_lower)
        if k_match:
            try:
                num = float(k_match.group(1).replace(",", "")) * 1000
                return f"₹{num:,.0f} Cr", num
            except ValueError:
                pass

        # Check standard Crores
        cr_match = re.search(self.generic_cr_pattern, text_lower)
        if cr_match:
            try:
                num = float(cr_match.group(1).replace(",", ""))
                return f"₹{num:,.1f} Cr", num
            except ValueError:
                pass

        # Check USD Million / Billion
        usd_match = re.search(r"\$\s*([0-9,]+(?:\.[0-9]+)?)\s*(m|million|b|billion)", text_lower)
        if usd_match:
            try:
                num = float(usd_match.group(1).replace(",", ""))
                unit = usd_match.group(2)
                multiplier = 8300 if "b" in unit else 8.3  # $1B ≈ ₹8,300 Cr, $1M ≈ ₹8.3 Cr
                cr_val = num * multiplier
                return f"${num}{unit.upper()[0]} (~₹{cr_val:,.1f} Cr)", cr_val
            except ValueError:
                pass

        return None, 0.0

    def extract_entities(self, title, summary):
        """Extracts primary subject/company/founders from headline and summary."""
        full_text = f"{title} {summary}"

        # Clean title to extract key company/entity
        cleaned = re.sub(r"^(tech\d+|watch|analysis|exclusive|live|report):\s*", "", title, flags=re.IGNORECASE)
        company = "Leadership & Promoters"

        # Regex for common headlines: "Company raises...", "Company files DRHP...", "Founder of Company..."
        m_founder_of = re.search(r"founder\s+of\s+([A-Za-z0-9\s\-]+?)(?:,|on|\s+files|\s+raises|\s+sells)", cleaned, re.IGNORECASE)
        m_promoter = re.search(r"([A-Za-z0-9\s\-]+?)\s+promoter\s+sells", cleaned, re.IGNORECASE)
        m_files = re.search(r"([A-Za-z0-9\s\-]+?)\s+(?:files|gets|secures|raises|pauses|plans)\s+(?:for\s+)?(?:ipo|drhp|\$|funding)", cleaned, re.IGNORECASE)

        if m_founder_of:
            company = m_founder_of.group(1).strip()
        elif m_promoter:
            company = m_promoter.group(1).strip()
        elif m_files:
            company = m_files.group(1).strip()
        elif ":" in cleaned:
            company = cleaned.split(":")[0].strip()
        elif "|" in cleaned:
            parts = [p.strip() for p in cleaned.split("|")]
            company = parts[0] if len(parts[0]) > 3 else (parts[1] if len(parts) > 1 else cleaned)
        else:
            words = cleaned.split()
            if len(words) >= 3:
                company = " ".join(words[:4])

        # Trim excessively long company names
        if len(company) > 35:
            company = company[:35] + "..."

        # Persona identification
        persona_type = "Executive / Promoter"
        if re.search(r"\b(founder|co-founder)\b", full_text, re.IGNORECASE):
            persona_type = "Founder / Entrepreneur"
        elif re.search(r"\b(promoter|promoters)\b", full_text, re.IGNORECASE):
            persona_type = "Company Promoter"
        elif re.search(r"\b(ceo|managing director|md|cxo|president|partner|vp)\b", full_text, re.IGNORECASE):
            persona_type = "C-Suite / Tech CXO"
        elif re.search(r"\b(nri|diaspora|indian-origin)\b", full_text, re.IGNORECASE):
            persona_type = "Senior NRI / Global Executive"

        return company, persona_type

    def score_lead(self, article):
        """
        Applies Earthitects ICP scoring criteria:
        - Budget Confirm >= 9.5 Cr: +3
        - Valuation 50-100 Cr+ / Founder: +3
        - Already owns holiday home / nature affinity: +2
        - NRI / Multi-city Property Owner: +1
        - Active Liquidity / Timeline <= 12m: +2
        Target ideal score >= 7-8
        """
        text = f"{article['title']} {article['summary']}".lower()
        score = 0
        score_breakdown = []
        event_type = "General Market Liquidity"

        # 1. Detect Liquidity Trigger & Event Type
        for pattern, label, weight in self.liquidity_patterns:
            if re.search(pattern, text):
                event_type = label
                break

        # 2. Financial Scale & Capacity
        amount_str, amount_cr = self.extract_deal_amount(text)
        if amount_cr >= 9.5 or "ofs" in text or "secondary" in text or "promoter sells" in text or "ipo" in text:
            score += 3
            score_breakdown.append("Budget / Liquidity Event >= ₹9.5 Cr (+3)")
        elif amount_cr > 0:
            score += 2
            score_breakdown.append(f"Substantial Financial Event ({amount_str}) (+2)")

        # 3. Founder / Company Valuation >= 50-100 Cr
        if re.search(r"\b(founder|promoter|co-founder|unicorn|soonicorn|listed company)\b", text):
            score += 3
            score_breakdown.append("Founder / Promoter of ₹50-100 Cr+ Enterprise (+3)")
        elif re.search(r"\b(ceo|managing director|md|president|vp|director)\b", text):
            score += 2
            score_breakdown.append("High-Comp CXO / Tech Executive (+2)")

        # 4. Geography: South India / Bengaluru Hub (+2) OR NRI / Multi-city (+1)
        is_south_india = any(hub in text for hub in SOUTH_INDIA_HUBS)
        is_nri = any(hub in text for hub in GLOBAL_NRI_HUBS)

        if is_south_india:
            score += 2
            score_breakdown.append("Bengaluru / Karnataka / South India Location (+2)")
        elif is_nri:
            score += 1
            score_breakdown.append("NRI / Global Presence (US/UAE/Singapore) (+1)")

        # 5. Timeline <= 12 Months (Liquidity actively unfolding)
        if any(w in text for w in ["ipo", "drhp", "secondary", "debut", "files for", "closing round", "bought", "divests", "buyback", "raises"]):
            score += 2
            score_breakdown.append("Immediate / 12-Month Liquidity Horizon (+2)")

        # 6. Holiday Home / Nature / Plantation / Estate Affinity
        if any(w in text for w in ["nature", "estate", "plantation", "coffee", "retreat", "luxury home", "second home", "villa"]):
            score += 2
            score_breakdown.append("Explicit Second Home / Nature Motive (+2)")

        company, persona_type = self.extract_entities(article["title"], article["summary"])
        advisor_angle = self.generate_advisor_angle(persona_type, company, event_type, amount_str)

        # Classification tier
        if score >= 7:
            tier = "Tier 1: VIP Priority Lead"
            tier_class = "vip"
        elif score >= 5:
            tier = "Tier 2: Strong Liquidity Prospect"
            tier_class = "strong"
        else:
            tier = "Tier 3: Market Intelligence / Nurture"
            tier_class = "nurture"

        # Search query for LinkedIn
        search_terms = f"{company} Founder" if company != "Leadership & Promoters" else f"{article['title'][:30]} Founder"
        encoded_search = re.sub(r"[^a-zA-Z0-9\s]", "", search_terms).strip().replace(" ", "%20")

        return {
            "title": article["title"],
            "link": article["link"],
            "source": article["source"],
            "published": article["published"],
            "summary": article["summary"],
            "company": company,
            "persona_type": persona_type,
            "event_type": event_type,
            "amount_str": amount_str or "Multi-Crore Event",
            "score": score,
            "score_breakdown": score_breakdown,
            "tier": tier,
            "tier_class": tier_class,
            "advisor_angle": advisor_angle,
            "linkedin_search_url": f"https://www.linkedin.com/search/results/all/?keywords={encoded_search}"
        }

    def generate_advisor_angle(self, persona, company, event_type, amount):
        """Generates a non-salesy, consultative icebreaker rooted in Earthitects philosophy."""
        amt_context = f" on the recent {amount} milestone" if amount else ""
        return (
            f"Advisor Strategy: Congratulate {company} leadership{amt_context} ({event_type}). "
            f"Position as an advisor curating private, low-density coffee & plantation estates in Western Ghats (Coorg/Chikmagalur/Wayanad) "
            f"designed for generational family legacy with managed operational ease.\n\n"
            f"Discovery Openers:\n"
            f"1. 'What does an ideal weekend or holiday look like for your family today?'\n"
            f"2. 'When you think about a second home, what matters more to you: absolute privacy, effortless management, or multi-generational legacy?'"
        )
