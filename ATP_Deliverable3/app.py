import pandas as pd
import streamlit as st

st.set_page_config(page_title="ATP 2025 Tennis Analysis", page_icon="🎾", layout="wide")
st.title("🎾 ATP 2025 Tennis Match Analysis")
st.write("Explore ATP match results by court surface, rankings, and serving performance.")
st.caption("Audience: tennis players, coaches, fans, and sports analysts. Data: ATP 2025 match archive (includes late-2024 tournament start dates).")

@st.cache_data
def load_data():
    from pathlib import Path
data = pd.read_csv(Path(__file__).resolve().parent / "dashboard_data.csv")
    data["tourney_date"] = pd.to_datetime(data["tourney_date"], errors="coerce")
    return data

data = load_data()
st.sidebar.header("Filters")
surfaces = st.sidebar.multiselect("Court surface", sorted(data["surface"].dropna().unique()), default=sorted(data["surface"].dropna().unique()))
filtered = data[data["surface"].isin(surfaces)].copy()
tournaments = sorted(filtered["tourney_name"].dropna().unique())
chosen_tournaments = st.sidebar.multiselect("Tournament (optional)", tournaments, default=[])
if chosen_tournaments:
    filtered = filtered[filtered["tourney_name"].isin(chosen_tournaments)]

if filtered.empty:
    st.warning("No matches match these filters. Select a surface or clear the tournament selection.")
    st.stop()

ranked = filtered["higher_ranked_won"].dropna()
rate = ranked.mean() * 100 if not ranked.empty else None
winner_serve = filtered["w_first_serve_win_pct"].mean()

c1, c2, c3 = st.columns(3)
c1.metric("Matches", f"{len(filtered):,}")
c2.metric("Higher-ranked player wins", f"{rate:.1f}%" if rate is not None else "N/A", help="Only matches with valid, different ATP rankings")
c3.metric("Winner first-serve points won", f"{winner_serve:.1f}%" if pd.notna(winner_serve) else "N/A", help="Average across matches with recorded service statistics")

st.subheader("1. Matches by court surface")
counts = filtered["surface"].value_counts().rename_axis("Surface").reset_index(name="Matches")
st.bar_chart(counts.set_index("Surface"), y="Matches", x_label="Court surface", y_label="Number of matches")
st.write("This chart shows how many matches in the selected data were played on each court surface. It describes the dataset, not which surface is more difficult.")

st.subheader("2. Higher-ranked player win rate by surface")
rates = (filtered.groupby("surface")["higher_ranked_won"].mean() * 100).dropna().sort_values(ascending=False)
if rates.empty:
    st.info("No matches with valid rankings are available for these filters.")
else:
    st.bar_chart(rates.rename("Win rate (%)"), y_label="Win rate (%)", x_label="Court surface")
    st.write("A lower ATP ranking number means a better ranking. This chart compares how often the higher-ranked player won on each surface, excluding matches with missing or tied rankings.")

st.subheader("3. First-serve points won: winners vs. losers")
serve = pd.Series({"Match winners": filtered["w_first_serve_win_pct"].mean(), "Match losers": filtered["l_first_serve_win_pct"].mean()}, name="First-serve points won (%)").dropna()
if serve.empty:
    st.info("No first-serve statistics are available for these filters.")
else:
    st.bar_chart(serve, y_label="First-serve points won (%)", x_label="Match result")
    st.write("This compares the average percentage of first-serve points won by winners and losers. It shows an association, not proof that serving alone causes a victory.")

st.subheader("Explore the filtered matches")
st.dataframe(filtered[["tourney_name", "tourney_date", "surface", "round", "winner_name", "loser_name", "winner_rank", "loser_rank"]], use_container_width=True, hide_index=True)
st.caption("Source: tennis-sackmann archive, ATP 2025 match results. Missing rankings and serving statistics are not estimated.")
