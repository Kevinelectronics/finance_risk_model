"""
Example 01 — Risk Decomposition for NVDA using RiskModels API.

Fetches a four-layer risk decomposition (market, sector, subsector, residual)
and a metrics snapshot, then formats the output as structured context
suitable for LLM prompts or downstream analysis.

Setup:
    pip install requests python-dotenv
    Copy .env.example to .env and add your API key.
"""

import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ["RISKMODELS_API_KEY"]
TICKER = "NVDA"
BASE = "https://riskmodels.app"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}


def get_metrics(ticker: str) -> dict:
    r = requests.get(f"{BASE}/api/metrics/{ticker}", headers=HEADERS)
    r.raise_for_status()
    return r.json()


def get_decomposition(ticker: str) -> dict:
    r = requests.post(
        f"{BASE}/api/decompose",
        headers={**HEADERS, "Content-Type": "application/json"},
        json={"ticker": ticker},
    )
    r.raise_for_status()
    return r.json()


def format_for_llm(metrics: dict, decomp: dict) -> str:
    return f"""
=== Risk Analysis: {TICKER} ===

Metrics Snapshot:
{json.dumps(metrics, indent=2)}

Four-Layer Risk Decomposition (market / sector / subsector / residual):
{json.dumps(decomp, indent=2)}
""".strip()


if __name__ == "__main__":
    metrics = get_metrics(TICKER)
    decomp = get_decomposition(TICKER)

    context = format_for_llm(metrics, decomp)
    print(context)
