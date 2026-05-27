# Finance Risk Model — Python Examples with RiskModels API

Practical Python examples for **quantitative risk analysis** of stocks using the [RiskModels API](https://riskmodels.app). Each example demonstrates a specific use case — from four-layer risk decomposition and hedge ratio extraction to formatting risk data as structured context for LLM-powered financial agents.

## What This Repo Covers

- **Risk decomposition** — break down stock risk into market, sector, subsector, and residual components
- **Metrics snapshots** — hedge ratios, explained risk, and rolling volatility for any ticker
- **LLM-ready context** — format risk data as structured text for use with Claude, GPT, or any AI model
- **Batch analysis** — analyze multiple positions at once (upcoming examples)
- **Macro factor correlation** — map stocks to macro drivers (upcoming examples)

## Examples

| File | Description |
|------|-------------|
| [`examples/01_risk_decomposition_nvda.py`](examples/01_risk_decomposition_nvda.py) | Four-layer risk decomposition + metrics snapshot for NVDA, formatted for LLM context |

More examples coming soon: portfolio-level risk, batch screeners, time-series hedge ratios, and AI agent integrations.

## Setup

```bash
git clone https://github.com/Kevinelectronics/finance_risk_model.git
cd finance_risk_model
pip install -r requirements.txt
cp .env.example .env          # add your RiskModels API key
```

Edit `.env`:
```
RISKMODELS_API_KEY=your_api_key_here
```

## Run an Example

```bash
python examples/01_risk_decomposition_nvda.py
```

## API Reference

- [RiskModels API Docs](https://riskmodels.app/docs)
- Endpoints used: `/api/metrics/{ticker}`, `/api/decompose`

## License

MIT
