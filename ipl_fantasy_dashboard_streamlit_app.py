import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="IPL Fantasy Dashboard", layout="wide")

# ----------------------
# SESSION STATE INIT
# ----------------------

if "teams" not in st.session_state:
    st.session_state.teams = {
        "Ankit": [],
        "Raghav": [],
        "Harsh": [],
        "Daksh": [],
        "Mukund": [],
        "Kundan": [],
        "Vansh": [],
        "Pryam & Nikunj": []
    }

if "history" not in st.session_state:
    st.session_state.history = []

# ----------------------
# POINT SYSTEM
# ----------------------

def calculate_batting_points(runs, fours, sixes, balls):
    pts = runs
    pts += fours * 4
    pts += sixes * 6

    if runs >= 50:
        pts += 8
    elif runs >= 30:
        pts += 4

    if balls >= 10:
        sr = (runs / balls) * 100
        if sr >= 170:
            pts += 6
        elif sr >= 150:
            pts += 4
        elif sr >= 130:
            pts += 2
        elif sr < 100:
            pts -= 4

    return pts


def calculate_bowling_points(wickets, economy):
    pts = wickets * 25

    if wickets >= 3:
        pts += 4

    if economy >= 12:
        pts -= 6
    elif economy >= 11:
        pts -= 4
    elif economy >= 10:
        pts -= 2

    return pts

# ----------------------
# SCRAPER (BASIC)
# ----------------------

def fetch_scorecard(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        st.warning("Auto scraping not fully reliable yet. Use manual entry if needed.")
        return []
    except:
        st.error("Failed to fetch scorecard")
        return []

# ----------------------
# SIDEBAR
# ----------------------

st.sidebar.title("IPL Fantasy Dashboard")
page = st.sidebar.radio("Navigate", ["Upload Match", "Teams", "Leaderboard", "Stats", "History"])

# ----------------------
# UPLOAD MATCH
# ----------------------

if page == "Upload Match":
    st.title("Upload Match")

    link = st.text_input("Paste Scorecard Link")

    st.subheader("Manual Player Entry (Accurate Mode)")

    player = st.text_input("Player Name")
    runs = st.number_input("Runs", 0)
    balls = st.number_input("Balls", 0)
    fours = st.number_input("4s", 0)
    sixes = st.number_input("6s", 0)
    wickets = st.number_input("Wickets", 0)
    economy = st.number_input("Economy", 0.0)
    catches = st.number_input("Catches", 0)

    if st.button("Calculate Player Points"):
        bat = calculate_batting_points(runs, fours, sixes, balls)
        bowl = calculate_bowling_points(wickets, economy)
        field = catches * 8

        total = bat + bowl + field

        st.success(f"Total Points: {total}")

    if st.button("Save Match"):
        st.session_state.history.append({"match": link, "data": "manual"})
        st.success("Match saved")

# ----------------------
# TEAMS
# ----------------------

elif page == "Teams":
    st.title("Teams Management")

    tabs = st.tabs(list(st.session_state.teams.keys()))

    for i, team in enumerate(st.session_state.teams):
        with tabs[i]:
            st.subheader(team)

            player_name = st.text_input(f"Add Player to {team}", key=team)

            if st.button(f"Add {team}"):
                if player_name:
                    st.session_state.teams[team].append(player_name)

            for p in st.session_state.teams[team]:
                col1, col2 = st.columns([3,1])
                col1.write(p)
                if col2.button("❌", key=p+team):
                    st.session_state.teams[team].remove(p)

# ----------------------
# LEADERBOARD
# ----------------------

elif page == "Leaderboard":
    st.title("Leaderboard")

    leaderboard = {}

    for match in st.session_state.history:
        pass

    st.info("Leaderboard will update after integrating auto scoring")

# ----------------------
# STATS
# ----------------------

elif page == "Stats":
    st.title("Stats")
    st.info("Coming soon: player analytics, top scorers, captain impact")

# ----------------------
# HISTORY
# ----------------------

elif page == "History":
    st.title("Match History")

    for m in st.session_state.history:
        st.write(m)
