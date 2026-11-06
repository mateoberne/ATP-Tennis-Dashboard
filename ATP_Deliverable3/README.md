# ATP 2025 Tennis Match Analysis Dashboard

## Project
This Streamlit dashboard continues my Deliverable 2 Python analysis of ATP tennis match results. It examines how match results differ across court surfaces, whether higher-ranked players usually win, and how first-serve performance compares between match winners and losers.

## Dataset and source
ATP 2025 match results from the [tennis-sackmann archive](https://github.com/Aneeshers/tennis-sackmann-archive/blob/main/atp/atp_matches_2025.csv). The included `dashboard_data.csv` is the cleaned, reduced CSV exported from my Deliverable 2 notebook. The source includes matches with tournament start dates in late 2024. Missing rankings and serve statistics were left missing, not estimated. Check the original dataset's license and attribution requirements before redistribution.

## Intended audience
Tennis players, coaches, fans, and sports analysts.

## Analysis questions
1. How do match results differ across court surfaces?
2. How often does the higher-ranked player win?
3. How are serving statistics related to winning?

## Dashboard features
- Three charts: matches by surface, higher-ranked player win rate by surface, and first-serve points won for winners versus losers.
- Three summary metrics: number of matches, higher-ranked player win rate, and winners' average first-serve points won.
- Two interactive controls: court surface and tournament. Both update the charts and metrics.

## Run locally
Install dependencies with `pip install -r requirements.txt`, then run `streamlit run app.py`.

## Published app
**App URL:** ADD_YOUR_PUBLISHED_STREAMLIT_URL_HERE

## AI-use statement
I used ChatGPT to help write and organize the Streamlit code, interactive filters, and README. I am responsible for checking the results, testing the dashboard, and explaining the findings.
