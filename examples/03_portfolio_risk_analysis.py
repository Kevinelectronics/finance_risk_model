"""
Example 03 — Portfolio-level risk decomposition with Claude.

Fetches ERM3 decompositions for a multi-stock portfolio, aggregates
the exposures, and asks Claude to identify the dominant risk character:
alpha-driven vs beta-driven, and which positions to reduce first.

Setup:
    pip install requests anthropic python-dotenv
    Copy .env.example to .env and fill both API keys.
"""

import os
import json
import requests
import anthropic
from dotenv import load_dotenv

load_dotenv()

RISKMODELS_KEY = os.environ["RISKMODELS_API_KEY"]
ANTHROPIC_KEY = os.environ["ANTHROPIC_API_KEY"]
BASE = "https://riskmodels.app"
HEADERS = {
    "Authorization": f"Bearer {RISKMODELS_KEY}",
    "Content-Type": "application/json",
}


def get_risk_decomposition(ticker: str) -> dict:
    r = requests.post(
        f"{BASE}/api/decompose",
        headers=HEADERS,
        json={"ticker": ticker},
    )
    r.raise_for_status()
    return r.json()


def analyze_portfolio(tickers: list[str]) -> dict:
    portfolio = {}
    for ticker in tickers:
        try:
            decomp = get_risk_decomposition(ticker)
            exposure = decomp.get("exposure", {})
            portfolio[ticker] = {
                "market_er":    exposure.get("market", {}).get("er", 0),
                "sector_er":    exposure.get("sector", {}).get("er", 0),
                "subsector_er": exposure.get("subsector", {}).get("er", 0),
                "residual_er":  exposure.get("residual", {}).get("er", 0),
                "hedge_level":  decomp.get("hedge_levels", {}).get("recommended_level"),
            }
            print(f"  {ticker}: OK")
        except Exception as e:
            portfolio[ticker] = {"error": str(e)}
            print(f"  {ticker}: ERROR — {e}")
    return portfolio


def claude_portfolio_analysis(portfolio: dict) -> str:
    client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system="""You are a quantitative portfolio analyst with expertise in equity risk models.
When given ERM3 decomposition data, you:
1. Identify the dominant return source (market / sector / subsector / residual)
2. Interpret the recommended hedge level and what it isolates
3. Flag any unusual signal in the decomposition
Always reference specific numbers from the data. Be direct and concise.""",
        messages=[
            {
                "role": "user",
                "content": f"""Here is the ERM3 decomposition for a {len(portfolio)}-stock portfolio:

{json.dumps(portfolio, indent=2)}

1. Which position has the highest idiosyncratic alpha (residual_er)?
2. Which position is most exposed to systematic risk (market + sector)?
3. What is the overall portfolio's risk character — alpha-driven or beta-driven?
4. Which position would you reduce first to lower systematic exposure?""",
            }
        ],
    )
    return response.content[0].text


if __name__ == "__main__":
    tickers = ["NVDA", "MSFT", "AAPL", "GOOGL"]

    print(f"Fetching ERM3 decompositions for {tickers}...")
    portfolio = analyze_portfolio(tickers)

    print("\nSending to Claude for portfolio analysis...\n")
    analysis = claude_portfolio_analysis(portfolio)
    print(analysis)
