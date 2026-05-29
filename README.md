# Finance Risk Model — Agentic Risk Analysis with RiskModels

Practical examples for **AI-native quantitative risk analysis** using [RiskModels](https://riskmodels.app). Start with Claude + MCP for an agentic workflow, then inspect the Python examples to see the API calls underneath.

## What This Repo Covers

- **Risk decomposition** — break down stock risk into market, sector, subsector, and residual components
- **Metrics snapshots** — hedge ratios, explained risk, and rolling volatility for any ticker
- **Claude/MCP workflow** — connect an AI agent directly to structured ERM3 risk data
- **LLM-ready context** — format risk data as structured text for use with Claude, GPT, or any AI model
- **Portfolio analysis** — aggregate ERM3 exposures across multiple positions and separate stock-specific from systematic risk
- **Macro factor correlation** — map stocks to macro drivers (upcoming examples)

## Agentic Quick Start

Install the RiskModels MCP server for Claude:

```bash
RISKMODELS_API_KEY=your_api_key_here npx -y riskmodels@latest install
```

Then ask Claude:

> Use RiskModels to decompose CRM. Explain the result like a quantitative portfolio analyst. Which risk layer dominates, what ETF hedge isolates residual risk, and what would this mean for an AI portfolio assistant?

The Python examples below show the same workflow through explicit HTTP calls.

## Examples

| File | Description |
|------|-------------|
| [`examples/01_risk_decomposition_crm.py`](examples/01_risk_decomposition_crm.py) | Four-layer risk decomposition + metrics snapshot for CRM (Salesforce), formatted for LLM context |
| [`examples/02_claude_risk_analyst.py`](examples/02_claude_risk_analyst.py) | Claude acts as a quant analyst: interprets ERM3 decomposition and gives actionable portfolio insights |
| [`examples/03_portfolio_risk_analysis.py`](examples/03_portfolio_risk_analysis.py) | Multi-stock portfolio decomposition: Claude identifies stock-specific vs systematic risk character and which positions drive systematic risk |

More examples coming soon: batch screeners, time-series hedge ratios, automated daily reports, and 13F fund analysis.

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

For the Claude example, also set:
```
ANTHROPIC_API_KEY=your_anthropic_key_here
```

## Run an Example

```bash
python examples/01_risk_decomposition_crm.py
```

## API Reference

- [RiskModels API Docs](https://riskmodels.app/docs)
- Endpoints used: `/api/metrics/{ticker}`, `/api/decompose`

### Reading `/decompose`

- **`er`** — explained-risk contribution at each layer (not expected return); values typically behave like variance fractions and sum to ~1 at L3, though small negative layer contributions can occur after orthogonalization
- **`hr`** — dollars of ETF per $1 of stock; any leg may be negative after orthogonalization
- **`exposure`** — L3 layer breakdown; use **`hedge_levels[recommended_level]`** for hedge ratios that match the model’s recommended depth

## License

MIT
