
import streamlit as st
import pandas as pd
from pathlib import Path

# Page settings
st.set_page_config(
    page_title="ATP 2025 Tennis Analysis",
    page_icon="🎾",
    layout="wide"
)

# Load the dataset
@st.cache_data
def load_data():
    file_path = Path(__file__).resolve().parent / "dashboard_data.csv"
    data = pd.read_csv(file_path)

    data["tourney_date"] = pd.to_datetime(
        data["tourney_date"], errors="coerce"
    )

    return data


data = load_data()

# Dashboard title
st.title("🎾 ATP 2025 Tennis Match Analysis")

st.write(
    "This dashboard analyzes ATP tennis match results, "
    "court surfaces, player rankings, and serving statistics."
)

st.caption(
    "Audience: tennis players, coaches, fans, and sports analysts. "
    "Data: ATP 2025 match archive, including tournaments "
    "that started in late 2024."
)

# Sidebar filters
st.sidebar.header("Filters")

surfaces = st.sidebar.multiselect(
    "Select court surface",
    options=sorted(data["surface"].dropna().unique()),
    default=sorted(data["surface"].dropna().unique())
)

filtered = data[data["surface"].isin(surfaces)].copy()

tournaments = st.sidebar.multiselect(
    "Select tournament",
    options=sorted(filtered["tourney_name"].dropna().unique()),
    default=sorted(filtered["tourney_name"].dropna().unique())
)

filtered = filtered[
    filtered["tourney_name"].isin(tournaments)
].copy()

players = sorted(
    set(filtered["winner_name"].dropna()) |
    set(filtered["loser_name"].dropna())
)

selected_player = st.sidebar.selectbox(
    "Select player",
    options=["All players"] + players
)

if selected_player != "All players":
    filtered = filtered[
        (filtered["winner_name"] == selected_player) |
        (filtered["loser_name"] == selected_player)
    ].copy()

# Stop if no matches match the filters
if filtered.empty:
    st.warning(
        "No matches found for these filters. "
        "Please change your selections."
    )
    st.stop()

# Summary metrics
st.subheader("Summary Statistics")

total_matches = len(filtered)

ranking_data = filtered["higher_ranked_won"].dropna()

if len(ranking_data) > 0:
    higher_rank_win_rate = ranking_data.mean() * 100
else:
    higher_rank_win_rate = 0

average_aces = pd.concat([
    filtered["w_ace"],
    filtered["l_ace"]
]).mean()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Matches", f"{total_matches:,}")

with col2:
    st.metric(
        "Higher-Ranked Player Win Rate",
        f"{higher_rank_win_rate:.1f}%"
        if len(ranking_data) > 0 else "N/A"
    )

with col3:
    st.metric(
        "Average Aces per Player",
        f"{average_aces:.1f}"
        if pd.notna(average_aces) else "N/A"
    )

st.divider()

# Chart 1
st.subheader("1. Matches by Court Surface")

surface_counts = filtered["surface"].value_counts()

st.bar_chart(
    surface_counts,
    x_label="Court Surface",
    y_label="Number of Matches"
)

st.write(
    "This chart shows how many matches were played on each "
    "court surface in the selected data. It helps us understand "
    "the distribution of matches across hard, clay, and grass courts."
)

st.divider()

# Chart 2
st.subheader("2. Higher-Ranked Player Win Rate by Surface")

ranking_by_surface = (
    filtered.dropna(subset=["higher_ranked_won"])
    .groupby("surface")["higher_ranked_won"]
    .mean()
    .mul(100)
    .sort_values(ascending=False)
)

if not ranking_by_surface.empty:
    st.bar_chart(
        ranking_by_surface,
        x_label="Court Surface",
        y_label="Higher-Ranked Player Win Rate (%)"
    )
else:
    st.info("No ranking information is available.")

st.write(
    "This chart shows how often the higher-ranked player won "
    "on each surface. A higher percentage means that rankings "
    "were more successful at predicting the winner. "
    "Matches without usable rankings are excluded."
)

st.divider()

# Chart 3
st.subheader("3. First-Serve Points Won: Winners vs. Losers")

serve_comparison = pd.Series({
    "Match Winners": filtered["w_first_serve_win_pct"].mean(),
    "Match Losers": filtered["l_first_serve_win_pct"].mean()
})

serve_comparison = serve_comparison.dropna()

if not serve_comparison.empty:
    st.bar_chart(
        serve_comparison,
        x_label="Match Result",
        y_label="Average First-Serve Points Won (%)"
    )
else:
    st.info("No first-serve statistics are available.")

st.write(
    "This chart compares the average percentage of first-serve "
    "points won by match winners and losers. It helps show "
    "the relationship between serving performance and "
    "winning tennis matches."
)

st.divider()

# Additional player information
if selected_player != "All players":
    st.subheader(f"Player Summary: {selected_player}")

    player_wins = (
        filtered["winner_name"] == selected_player
    ).sum()

    player_losses = (
        filtered["loser_name"] == selected_player
    ).sum()

    player_win_rate = (
        player_wins / total_matches * 100
        if total_matches > 0 else 0
    )

    p1, p2, p3 = st.columns(3)

    with p1:
        st.metric("Wins", player_wins)

    with p2:
        st.metric("Losses", player_losses)

    with p3:
        st.metric("Win Rate", f"{player_win_rate:.1f}%")

st.divider()

# Match data table
st.subheader("Explore the Match Data")

st.write(
    "The table below displays the matches included "
    "after applying your selected filters."
)

display_columns = [
    "tourney_date",
    "tourney_name",
    "surface",
    "round",
    "winner_name",
    "loser_name",
    "winner_rank",
    "loser_rank"
]

st.dataframe(
    filtered[display_columns],
    use_container_width=True,
    hide_index=True
)

# Conclusions
st.subheader("Key Findings")

st.write(
    "1. Court surfaces help us compare how ATP matches "
    "are distributed across different playing conditions."
)

st.write(
    "2. ATP rankings are useful for studying match outcomes, "
    "but lower-ranked players can still win."
)

st.write(
    "3. First-serve performance is an important statistic "
    "when comparing match winners and losers."
)

st.caption(
    "Data source: ATP 2025 match results from the "
    "tennis-sackmann archive. "
    "Dashboard created using Python, Pandas, and Streamlit."
)
