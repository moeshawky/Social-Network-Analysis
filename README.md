# Network Intelligence Engine

A production-grade, multi-platform network intelligence engine designed for career intelligence and relationship mapping. This system aggregates data from Facebook, LinkedIn, Twitter, and PowerMem to construct a unified social graph, resolve cross-platform identities, and compute advanced network metrics.

## Features

- **Multi-Source Data Ingestion**: Load data from Facebook, LinkedIn, Twitter, and CSV/JSON.
- **Cross-Platform Identity Resolution**: Automatically merge profiles representing the same person using weighted confidence scoring.
- **Advanced Graph Analysis**: Compute Centrality (Degree, Closeness, Betweenness, Eigenvector, PageRank, Katz), Communities, and Pathfinding.
- **Interactive Visualization**: Generate high-quality visualizations of networks, communities, and introduction paths.
- **Structured Reporting**: Export analysis as JSON or human-readable Markdown briefings.
- **PowerMem Integration**: Read/Write analysis results to a semantic memory store.

## Installation

```bash
git clone <repository-url>
cd network_intelligence
pip install -e .
```

## Quick Start

### 1. Analyze a specific company network
```bash
python -m network_intelligence --from-file relationships.csv --company "Egis Group" --all-centrality --visualize full
```

### 2. Find an introduction path
```bash
python -m network_intelligence --from-all --client "Ahmed Elshenawy" --target "Sarah Johnson" --visualize path
```

### 3. Run full analysis and export report
```bash
python -m network_intelligence --from-facebook ./fb_data/ --company "TechCorp" --output-format markdown
```

## Configuration

Configuration is managed via environment variables (see `network_intelligence/config.py`).

| Variable | Default | Description |
|----------|---------|-------------|
| `POWERMEM_URL` | `http://127.0.0.1:43117` | URL for PowerMem API |
| `IDENTITY_CONFIDENCE_THRESHOLD` | `0.70` | Threshold to consider a match |
| `IDENTITY_AUTO_MERGE_THRESHOLD` | `0.90` | Threshold to automatically merge identities |
| `VIZ_DARK_MODE` | `true` | Enable dark mode for visualizations |

## Data Sources

The engine supports multiple input formats:

- **Facebook**: SNAP edge list or JSON export.
- **LinkedIn**: CSV exports from "Download Your Data".
- **Twitter**: JSON archive or scraped data.
- **CSV**: Generic edge list with columns `source`, `target`, `platform`.

## Identity Resolution

The system uses a weighted scoring algorithm to resolve identities across platforms:

1. **Name Similarity** (30%)
2. **Handle Similarity** (15%)
3. **Company Match** (20%)
4. **Title Match** (10%)
5. **Mutual Connections** (25%)

Matches with confidence ≥ 0.90 are auto-merged. Matches between 0.50 and 0.89 are flagged for review.

## Visualization

Generate publication-quality graphs:

- **Full Network**: `python -m network_intelligence --visualize full`
- **Communities**: `python -m network_intelligence --visualize communities`
- **Path Analysis**: `python -m network_intelligence --visualize path --client A --target B`
- **Centrality**: `python -m network_intelligence --visualize centrality`

## Testing

Run the test suite to verify functionality and regression against known baselines:

```bash
pip install -r requirements-dev.txt
pytest tests/ -v
```

## Architecture

```
Data Sources (FB, LI, TW)
       ↓
Identity Resolution (Entity Merging)
       ↓
Graph Builder (MultiGraph Construction)
       ↓
Analysis Engine (Centrality, Pathfinding, Communities)
       ↓
Output & Visualization (JSON, Markdown, PNG)
```
