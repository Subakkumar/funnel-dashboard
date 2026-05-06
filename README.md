# Funnel Analysis — Interactive Dashboard

A fully interactive e-commerce conversion funnel analysis dashboard built with Plotly Dash. Analyze 50,000 user sessions with live filters across device, traffic source, country, and category.

## Features

- Live KPIs — users, conversions, CVR, revenue, AOV
- Interactive funnel visualization with drop-off rates
- CVR breakdown by device, traffic source, category, country
- Monthly trend with dual-axis (CVR + volume)
- Revenue intelligence by category and source
- Day-of-week conversion patterns
- All charts update instantly on filter change

## Tech Stack

- **Python** — Dash, Plotly, Pandas
- **Data** — 50,000 simulated e-commerce sessions

## Setup

1. Clone the repo
2. `python -m venv venv` then activate
3. `pip install -r requirements.txt`
4. Place `funnel_data.csv` in `data/` folder
5. `python app.py`
6. Open `http://localhost:8050`