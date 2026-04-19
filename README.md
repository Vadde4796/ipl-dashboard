# IPL Dashboard 🏏

An interactive data science dashboard for Indian Premier League (IPL) statistics — seasons 2008 to 2024.

## Features

| Section | What you get |
|---|---|
| **Overview** | Season champions, match trends, toss impact |
| **Teams** | Win/loss records, head-to-head, win % pie chart |
| **Batsmen** | Top run scorers, strike rates, 50s & 100s |
| **Bowlers** | Top wicket takers, economy rates |
| **Seasons** | Year-by-year analysis, over-by-over run rates |

## Quick Start

```bash
# 1. Clone & enter project
git clone https://github.com/Vadde4796/ipl-dashboard.git
cd ipl-dashboard

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux / macOS

# 3. Install dependencies
pip install -r requirements.txt

# 4. Generate IPL data
python src/generate_data.py

# 5. Launch dashboard
streamlit run dashboard/app.py
```

## Project Structure

```
ipl-dashboard/
├── data/
│   ├── matches.csv          # Match-level data (2008-2024)
│   └── deliveries.csv       # Ball-by-ball data
├── dashboard/
│   └── app.py               # Streamlit dashboard (5 pages)
├── src/
│   ├── generate_data.py     # Synthetic IPL data generator
│   ├── data_loader.py       # Data loading utilities
│   └── analysis.py          # Analysis & aggregation functions
├── notebooks/
│   └── ipl_eda.ipynb        # Exploratory data analysis
├── requirements.txt
└── .gitignore
```

## Tech Stack

- **Python 3.12**
- **Streamlit** — interactive web dashboard
- **Pandas / NumPy** — data processing
- **Plotly** — interactive charts
- **Scikit-learn** — ML utilities
- **Jupyter** — exploratory notebooks
