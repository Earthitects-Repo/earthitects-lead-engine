"""
Executive HTML Digest Builder
Renders an elegant, publication-quality private intelligence briefing for Faraz at Earthitects.
"""
from datetime import datetime
from jinja2 import Template

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Earthitects Liquidity & Private Lead Intelligence</title>
<style>
  body {
    margin: 0;
    padding: 0;
    background-color: #F4F4F0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    color: #2D312E;
    line-height: 1.6;
  }
  .container {
    max-width: 680px;
    margin: 30px auto;
    background: #FFFFFF;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    border: 1px solid #E5E5DE;
  }
  .header {
    background: linear-gradient(135deg, #1C2D27 0%, #2A3F37 100%);
    color: #FFFFFF;
    padding: 36px 32px;
    text-align: left;
    border-bottom: 3px solid #C2A676;
  }
  .brand {
    font-size: 13px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #C2A676;
    font-weight: 700;
    margin-bottom: 6px;
  }
  .header h1 {
    margin: 0 0 8px 0;
    font-size: 24px;
    font-weight: 600;
    letter-spacing: -0.5px;
  }
  .header p {
    margin: 0;
    font-size: 14px;
    color: #CBD5CE;
  }
  .stats-bar {
    display: flex;
    background: #FAF8F5;
    border-bottom: 1px solid #EBE8E1;
    padding: 16px 32px;
    justify-content: space-between;
  }
  .stat-item {
    text-align: center;
  }
  .stat-value {
    font-size: 20px;
    font-weight: 700;
    color: #1C2D27;
  }
  .stat-label {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #717A74;
  }
  .content {
    padding: 32px;
  }
  .section-title {
    font-size: 16px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #1C2D27;
    border-left: 4px solid #C2A676;
    padding-left: 12px;
    margin: 28px 0 18px 0;
    font-weight: 700;
  }
  .lead-card {
    background: #FFFFFF;
    border: 1px solid #E5E5DE;
    border-radius: 10px;
    padding: 22px;
    margin-bottom: 22px;
    transition: all 0.2s ease;
  }
  .lead-card.vip {
    border-left: 5px solid #C2A676;
    background: #FCFAF7;
  }
  .card-top {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 12px;
  }
  .entity-title {
    font-size: 18px;
    font-weight: 700;
    color: #1C2D27;
    margin: 0;
  }
  .persona-badge {
    display: inline-block;
    font-size: 12px;
    font-weight: 600;
    color: #3B5249;
    background: #E8EFEA;
    padding: 2px 8px;
    border-radius: 4px;
    margin-top: 4px;
  }
  .score-badge {
    background: #1C2D27;
    color: #C2A676;
    font-weight: 800;
    font-size: 13px;
    padding: 6px 12px;
    border-radius: 20px;
    white-space: nowrap;
    border: 1px solid #C2A676;
  }
  .headline {
    font-size: 15px;
    font-weight: 600;
    color: #333;
    margin: 10px 0 6px 0;
  }
  .headline a {
    color: #1C2D27;
    text-decoration: none;
  }
  .headline a:hover {
    text-decoration: underline;
    color: #C2A676;
  }
  .summary {
    font-size: 13px;
    color: #555E58;
    margin-bottom: 14px;
  }
  .meta-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 14px;
  }
  .meta-chip {
    font-size: 11px;
    padding: 3px 9px;
    border-radius: 4px;
    background: #F0EDE6;
    color: #4A4A44;
    font-weight: 500;
  }
  .meta-chip.highlight {
    background: #EAE3D4;
    color: #614D25;
    font-weight: 600;
  }
  .advisor-box {
    background: #F4F6F4;
    border: 1px dashed #A3B8AD;
    border-radius: 8px;
    padding: 14px;
    margin-top: 14px;
  }
  .advisor-title {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #2D4C3E;
    font-weight: 700;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .advisor-text {
    font-size: 12px;
    color: #38423C;
    white-space: pre-line;
    line-height: 1.5;
  }
  .actions-row {
    margin-top: 14px;
    display: flex;
    gap: 10px;
  }
  .btn {
    display: inline-block;
    font-size: 12px;
    font-weight: 600;
    padding: 6px 14px;
    border-radius: 6px;
    text-decoration: none;
    text-align: center;
  }
  .btn-primary {
    background: #1C2D27;
    color: #FFFFFF !important;
  }
  .btn-secondary {
    background: #ECEAE4;
    color: #3D443F !important;
  }
  .footer {
    background: #FAF8F5;
    border-top: 1px solid #EBE8E1;
    padding: 24px 32px;
    text-align: center;
    font-size: 12px;
    color: #8C948E;
  }
  .footer a {
    color: #1C2D27;
    text-decoration: none;
    font-weight: 600;
  }
</style>
</head>
<body>

<div class="container">
  <!-- Header -->
  <div class="header">
    <div class="brand">EARTHITECTS • PRIVATE INTELLIGENCE BRIEFING</div>
    <h1>UHNW Liquidity & ICP Leads Digest</h1>
    <p>Filtered for capacity &ge; ₹10–15 Cr, IPOs, secondary cash exits, and executive transitions.</p>
  </div>

  <!-- Stats Banner -->
  <div class="stats-bar">
    <div class="stat-item">
      <div class="stat-value">{{ total_scanned }}</div>
      <div class="stat-label">Articles Scanned</div>
    </div>
    <div class="stat-item">
      <div class="stat-value">{{ vip_count }}</div>
      <div class="stat-label">VIP Leads (&ge;7 Score)</div>
    </div>
    <div class="stat-item">
      <div class="stat-value">{{ generated_date }}</div>
      <div class="stat-label">Generated Date</div>
    </div>
  </div>

  <div class="content">
    {% if vip_leads %}
    <div class="section-title">🌟 Tier 1: High-Priority Liquidity Leads (Score &ge; 7)</div>
    {% for lead in vip_leads %}
    <div class="lead-card vip">
      <div class="card-top">
        <div>
          <h2 class="entity-title">{{ lead.company }}</h2>
          <span class="persona-badge">{{ lead.persona_type }}</span>
        </div>
        <div class="score-badge">SCORE: {{ lead.score }}/10</div>
      </div>

      <div class="headline">
        <a href="{{ lead.link }}" target="_blank">{{ lead.title }}</a>
      </div>
      
      <div class="summary">{{ lead.summary }}</div>

      <div class="meta-row">
        <span class="meta-chip highlight">Trigger: {{ lead.event_type }}</span>
        <span class="meta-chip highlight">Scale: {{ lead.amount_str }}</span>
        <span class="meta-chip">Source: {{ lead.source }}</span>
        {% for reason in lead.score_breakdown %}
        <span class="meta-chip">{{ reason }}</span>
        {% endfor %}
      </div>

      <div class="advisor-box">
        <div class="advisor-title">🛡️ Strategic Advisor Outreach Blueprint</div>
        <div class="advisor-text">{{ lead.advisor_angle }}</div>
      </div>

      <div class="actions-row">
        <a href="{{ lead.link }}" target="_blank" class="btn btn-primary">Read News Story</a>
        <a href="{{ lead.linkedin_search_url }}" target="_blank" class="btn btn-secondary">Search Founder on LinkedIn</a>
      </div>
    </div>
    {% endfor %}
    {% endif %}

    {% if strong_leads %}
    <div class="section-title">📈 Tier 2: Liquidity Pipeline & Market Intelligence</div>
    {% for lead in strong_leads %}
    <div class="lead-card">
      <div class="card-top">
        <div>
          <h2 class="entity-title">{{ lead.company }}</h2>
          <span class="persona-badge">{{ lead.persona_type }}</span>
        </div>
        <div class="score-badge">SCORE: {{ lead.score }}/10</div>
      </div>

      <div class="headline">
        <a href="{{ lead.link }}" target="_blank">{{ lead.title }}</a>
      </div>

      <div class="meta-row">
        <span class="meta-chip highlight">{{ lead.event_type }}</span>
        <span class="meta-chip">Scale: {{ lead.amount_str }}</span>
        <span class="meta-chip">Source: {{ lead.source }}</span>
      </div>

      <div class="actions-row">
        <a href="{{ lead.link }}" target="_blank" class="btn btn-secondary">Read Article</a>
        <a href="{{ lead.linkedin_search_url }}" target="_blank" class="btn btn-secondary">Find on LinkedIn</a>
      </div>
    </div>
    {% endfor %}
    {% endif %}

    {% if not vip_leads and not strong_leads %}
    <div style="text-align: center; padding: 40px 20px; color: #666;">
      <p style="font-size: 16px;">No high-probability liquidity events matched today's scan threshold.</p>
      <p style="font-size: 13px;">The harvester will re-check all real-time DRHP, IPO, and venture feeds on the next scheduled cycle.</p>
    </div>
    {% endif %}
  </div>

  <!-- Footer -->
  <div class="footer">
    <p>Curated for Faraz at <strong>Earthitects</strong> | Managed Nature Estates in Coorg, Chikmagalur & Wayanad</p>
    <p>Scoring Formula: Capacity &ge; 9.5 Cr (+3) | Founder 50-100 Cr+ (+3) | Nature Motive (+2) | South India / NRI (+2)</p>
  </div>
</div>

</body>
</html>
"""

class DigestBuilder:
    def __init__(self):
        self.template = Template(HTML_TEMPLATE)

    def build_digest(self, scored_leads, total_scanned=0):
        vip_leads = [l for l in scored_leads if l["score"] >= 7]
        strong_leads = [l for l in scored_leads if 5 <= l["score"] < 7]

        rendered_html = self.template.render(
            vip_leads=vip_leads[:15],       # Top 15 VIP leads
            strong_leads=strong_leads[:15], # Top 15 strong pipeline leads
            total_scanned=total_scanned,
            vip_count=len(vip_leads),
            generated_date=datetime.now().strftime("%d %b %Y, %I:%M %p")
        )
        return rendered_html
