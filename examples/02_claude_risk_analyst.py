"""
Example 02 — Claude as a quantitative analyst over ERM3 decomposition.

Fetches four-layer risk decomposition from RiskModels, passes it to Claude
with a quant analyst persona, and prints a structured interpretation.

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


def analyze_with_claude(ticker: str, decomp: dict) -> str:
    client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)

    message = client.messages.create(
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
                "content": f"""Analyze the following ERM3 decomposition for {ticker}:

{json.dumps(decomp, indent=2)}

Provide:
- The dominant return driver
- The recommended hedge and what it achieves
- Whether the residual signal is strong, weak, or neutral
- One actionable takeaway for a long-only portfolio manager""",
            }
        ],
    )
    return message.content[0].text


if __name__ == "__main__":
    ticker = "NVDA"
    print(f"Fetching ERM3 decomposition for {ticker}...")
    decomp = get_risk_decomposition(ticker)

    print("Sending to Claude for analysis...\n")
    analysis = analyze_with_claude(ticker, decomp)
    print(analysis)
