import pandas as pd
import streamlit as st
import plotly.express as px
import requests

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Cricket Analytics",
    page_icon="🏏",
    layout="wide"
)

# =========================================================
# MODERN DASHBOARD UI
# =========================================================

st.markdown("""
<style>

/* Main App */

.stApp {
    background-color: #F8FAFC;
}

/* Main Title */

h1 {
    color: #0F172A;
    text-align: center;
    font-size: 52px;
    font-weight: bold;
}

/* Sub Headings */

h2, h3 {
    color: #1E293B;
    font-weight: 600;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #0F172A,
        #1E293B
    );
}

/* Sidebar Text */

section[data-testid="stSidebar"] * {
    color: white;
}

/* Metric Cards */

div[data-testid="metric-container"] {

    background: white;

    border-radius: 18px;

    padding: 20px;

    border: 1px solid #E2E8F0;

    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);

    transition: 0.3s;
}

/* Metric Hover */

div[data-testid="metric-container"]:hover {

    transform: translateY(-3px);

    box-shadow: 0px 8px 18px rgba(0,0,0,0.12);
}

/* Tables */

[data-testid="stDataFrame"] {

    border-radius: 15px;

    overflow: hidden;

    border: 1px solid #E2E8F0;
}

/* Select Boxes */

div[data-baseweb="select"] {

    background-color: white;

    border-radius: 12px;
}

/* Remove Streamlit Footer */

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD DATA
# =========================================================

batters = pd.read_csv("data/IPL2025Batters.csv")
bowlers = pd.read_csv("data/IPL2025Bowlers.csv")

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.header("📊 Dashboard Menu")

option = st.sidebar.selectbox(
    "Select Option",
    [
        "🔍 Player Search",
        "⚔️ Player Comparison",
        "🔥 Top Batters",
        "🎯 Top Bowlers",
	"🏆 Team Analytics",
	"🟠 Orange & Purple Cap",
	 "🤖 Match Prediction",
	"⚔️ Head To Head",
        "🔴 UPCOMING INDIA MATCHES"
    ],
    key="main_menu"
)

# =========================================================
# 🔍 PLAYER SEARCH
# =========================================================

if option == "🔍 Player Search":

    st.title("🏏 AI Cricket Analytics")

    st.markdown(
        "## IPL 2025 Advanced Player Analytics Dashboard"
    )

    st.subheader("🔍 Search IPL Player")

    all_players = sorted(
        list(set(
            batters["Player Name"].tolist() +
            bowlers["Player Name"].tolist()
        ))
    )

    player_name = st.selectbox(
        "Select Player Name",
        all_players
    )

    batter_result = batters[
        batters["Player Name"] == player_name
    ]

    bowler_result = bowlers[
        bowlers["Player Name"] == player_name
    ]

    # =====================================================
    # BATTING ANALYTICS
    # =====================================================

    if not batter_result.empty:

        st.success("🏏 Batting Records Found")

        row = batter_result.iloc[0]

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Runs", row["Runs"])
        col2.metric("Average", row["AVG"])
        col3.metric("Strike Rate", row["SR"])
        col4.metric("Highest Score", row["HS"])

        col5, col6, col7, col8 = st.columns(4)

        col5.metric("Fours", row["4s"])
        col6.metric("Sixes", row["6s"])
        col7.metric("50s", row["50s"])
        col8.metric("100s", row["100s"])

        st.subheader("📋 Complete Batting Statistics")

        st.dataframe(batter_result)

        st.subheader("📊 Batting Performance Graph")

        batting_graph = pd.DataFrame({

            "Statistic": [
                "Runs",
                "Strike Rate",
                "Fours",
                "Sixes"
            ],

            "Value": [
                row["Runs"],
                row["SR"],
                row["4s"],
                row["6s"]
            ]
        })

        fig = px.bar(
            batting_graph,
            x="Statistic",
            y="Value",
            color="Statistic",
            text="Value",
            title=f"{player_name} Batting Analysis"
        )

        st.plotly_chart(fig, use_container_width=True)

    # =====================================================
    # BOWLING ANALYTICS
    # =====================================================

    if not bowler_result.empty:

        st.success("🎯 Bowling Records Found")

        row2 = bowler_result.iloc[0]

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Wickets", row2["WKT"])
        col2.metric("Economy", row2["ECO"])
        col3.metric("Average", row2["AVG"])
        col4.metric("Strike Rate", row2["SR"])

        st.subheader("📋 Complete Bowling Statistics")

        st.dataframe(bowler_result)

        st.subheader("📊 Bowling Performance Graph")

        bowling_graph = pd.DataFrame({

            "Statistic": [
                "Wickets",
                "Economy",
                "Average",
                "Strike Rate"
            ],

            "Value": [
                row2["WKT"],
                row2["ECO"],
                row2["AVG"],
                row2["SR"]
            ]
        })

        fig2 = px.bar(
            bowling_graph,
            x="Statistic",
            y="Value",
            color="Statistic",
            text="Value",
            title=f"{player_name} Bowling Analysis"
        )

        st.plotly_chart(fig2, use_container_width=True)

# =========================================================
# ⚔️ PLAYER COMPARISON
# =========================================================

elif option == "⚔️ Player Comparison":

    st.title("🏏 AI Cricket Analytics")

    st.markdown(
        "## IPL 2025 Advanced Player Analytics Dashboard"
    )

    st.subheader("⚔️ Compare Two Players")

    all_players = sorted(
        batters["Player Name"].unique()
    )

    player1 = st.selectbox(
        "Select First Player",
        all_players
    )

    player2 = st.selectbox(
        "Select Second Player",
        all_players
    )

    player1_data = batters[
        batters["Player Name"] == player1
    ]

    player2_data = batters[
        batters["Player Name"] == player2
    ]

    if not player1_data.empty and not player2_data.empty:

        row1 = player1_data.iloc[0]
        row2 = player2_data.iloc[0]

        comparison_df = pd.DataFrame({

            "Statistic": [
                "Runs",
                "Average",
                "Strike Rate",
                "Fours",
                "Sixes",
                "50s",
                "100s"
            ],

            player1: [
                row1["Runs"],
                row1["AVG"],
                row1["SR"],
                row1["4s"],
                row1["6s"],
                row1["50s"],
                row1["100s"]
            ],

            player2: [
                row2["Runs"],
                row2["AVG"],
                row2["SR"],
                row2["4s"],
                row2["6s"],
                row2["50s"],
                row2["100s"]
            ]
        })

        st.dataframe(comparison_df)

        graph_df = pd.DataFrame({

            "Statistic": [
                "Runs",
                "Strike Rate",
                "Fours",
                "Sixes"
            ],

            player1: [
                row1["Runs"],
                row1["SR"],
                row1["4s"],
                row1["6s"]
            ],

            player2: [
                row2["Runs"],
                row2["SR"],
                row2["4s"],
                row2["6s"]
            ]
        })

        fig = px.bar(
            graph_df,
            x="Statistic",
            y=[player1, player2],
            barmode="group",
            title=f"{player1} vs {player2}"
        )

        st.plotly_chart(fig, use_container_width=True)

# =========================================================
# 🔥 TOP BATTERS
# =========================================================

elif option == "🔥 Top Batters":

    st.title("🏏 AI Cricket Analytics")

    st.markdown(
        "## IPL 2025 Advanced Player Analytics Dashboard"
    )

    st.subheader("🔥 Top 10 Run Scorers")

    top_runs = batters.sort_values(
        by="Runs",
        ascending=False
    ).head(10)

    fig = px.bar(
        top_runs,
        x="Player Name",
        y="Runs",
        color="Runs",
        text="Runs",
        title="Top 10 Run Scorers IPL 2025"
    )

    import pandas as pd
import streamlit as st
import plotly.express as px
import requests

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Cricket Analytics",
    page_icon="🏏",
    layout="wide"
)

# =========================================================
# MODERN DASHBOARD UI
# =========================================================

st.markdown("""
<style>

/* Main App */

.stApp {
    background-color: #F8FAFC;
}

/* Main Title */

h1 {
    color: #0F172A;
    text-align: center;
    font-size: 52px;
    font-weight: bold;
}

/* Sub Headings */

h2, h3 {
    color: #1E293B;
    font-weight: 600;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #0F172A,
        #1E293B
    );
}

/* Sidebar Text */

section[data-testid="stSidebar"] * {
    color: white;
}

/* Metric Cards */

div[data-testid="metric-container"] {

    background: white;

    border-radius: 18px;

    padding: 20px;

    border: 1px solid #E2E8F0;

    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);

    transition: 0.3s;
}

/* Metric Hover */

div[data-testid="metric-container"]:hover {

    transform: translateY(-3px);

    box-shadow: 0px 8px 18px rgba(0,0,0,0.12);
}

/* Tables */

[data-testid="stDataFrame"] {

    border-radius: 15px;

    overflow: hidden;

    border: 1px solid #E2E8F0;
}

/* Select Boxes */

div[data-baseweb="select"] {

    background-color: white;

    border-radius: 12px;
}

/* Remove Streamlit Footer */

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD DATA
# =========================================================

batters = pd.read_csv("data/IPL2025Batters.csv")
bowlers = pd.read_csv("data/IPL2025Bowlers.csv")

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.header("📊 Dashboard Menu")

option = st.sidebar.selectbox(
    "Select Option",
    [
        "🔍 Player Search",
        "⚔️ Player Comparison",
        "🔥 Top Batters",
        "🎯 Top Bowlers",
	"🏆 Team Analytics",
	"🟠 Orange & Purple Cap",
	 "🤖 Match Prediction",
	"⚔️ Head To Head",
        "🔴 UPCOMING INDIA MATCHES"
    ],
    key="main_menu"
)

# =========================================================
# 🔍 PLAYER SEARCH
# =========================================================

if option == "🔍 Player Search":

    st.title("🏏 AI Cricket Analytics")

    st.markdown(
        "## IPL 2025 Advanced Player Analytics Dashboard"
    )

    st.subheader("🔍 Search IPL Player")

    all_players = sorted(
        list(set(
            batters["Player Name"].tolist() +
            bowlers["Player Name"].tolist()
        ))
    )

    player_name = st.selectbox(
        "Select Player Name",
        all_players
    )

    batter_result = batters[
        batters["Player Name"] == player_name
    ]

    bowler_result = bowlers[
        bowlers["Player Name"] == player_name
    ]

    # =====================================================
    # BATTING ANALYTICS
    # =====================================================

    if not batter_result.empty:

        st.success("🏏 Batting Records Found")

        row = batter_result.iloc[0]

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Runs", row["Runs"])
        col2.metric("Average", row["AVG"])
        col3.metric("Strike Rate", row["SR"])
        col4.metric("Highest Score", row["HS"])

        col5, col6, col7, col8 = st.columns(4)

        col5.metric("Fours", row["4s"])
        col6.metric("Sixes", row["6s"])
        col7.metric("50s", row["50s"])
        col8.metric("100s", row["100s"])

        st.subheader("📋 Complete Batting Statistics")

        st.dataframe(batter_result)

        st.subheader("📊 Batting Performance Graph")

        batting_graph = pd.DataFrame({

            "Statistic": [
                "Runs",
                "Strike Rate",
                "Fours",
                "Sixes"
            ],

            "Value": [
                row["Runs"],
                row["SR"],
                row["4s"],
                row["6s"]
            ]
        })

        fig = px.bar(
            batting_graph,
            x="Statistic",
            y="Value",
            color="Statistic",
            text="Value",
            title=f"{player_name} Batting Analysis"
        )

        st.plotly_chart(fig, use_container_width=True)

    # =====================================================
    # BOWLING ANALYTICS
    # =====================================================

    if not bowler_result.empty:

        st.success("🎯 Bowling Records Found")

        row2 = bowler_result.iloc[0]

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Wickets", row2["WKT"])
        col2.metric("Economy", row2["ECO"])
        col3.metric("Average", row2["AVG"])
        col4.metric("Strike Rate", row2["SR"])

        st.subheader("📋 Complete Bowling Statistics")

        st.dataframe(bowler_result)

        st.subheader("📊 Bowling Performance Graph")

        bowling_graph = pd.DataFrame({

            "Statistic": [
                "Wickets",
                "Economy",
                "Average",
                "Strike Rate"
            ],

            "Value": [
                row2["WKT"],
                row2["ECO"],
                row2["AVG"],
                row2["SR"]
            ]
        })

        fig2 = px.bar(
            bowling_graph,
            x="Statistic",
            y="Value",
            color="Statistic",
            text="Value",
            title=f"{player_name} Bowling Analysis"
        )

        st.plotly_chart(fig2, use_container_width=True)

# =========================================================
# ⚔️ PLAYER COMPARISON
# =========================================================

elif option == "⚔️ Player Comparison":

    st.title("🏏 AI Cricket Analytics")

    st.markdown(
        "## IPL 2025 Advanced Player Analytics Dashboard"
    )

    st.subheader("⚔️ Compare Two Players")

    all_players = sorted(
        batters["Player Name"].unique()
    )

    player1 = st.selectbox(
        "Select First Player",
        all_players
    )

    player2 = st.selectbox(
        "Select Second Player",
        all_players
    )

    player1_data = batters[
        batters["Player Name"] == player1
    ]

    player2_data = batters[
        batters["Player Name"] == player2
    ]

    if not player1_data.empty and not player2_data.empty:

        row1 = player1_data.iloc[0]
        row2 = player2_data.iloc[0]

        comparison_df = pd.DataFrame({

            "Statistic": [
                "Runs",
                "Average",
                "Strike Rate",
                "Fours",
                "Sixes",
                "50s",
                "100s"
            ],

            player1: [
                row1["Runs"],
                row1["AVG"],
                row1["SR"],
                row1["4s"],
                row1["6s"],
                row1["50s"],
                row1["100s"]
            ],

            player2: [
                row2["Runs"],
                row2["AVG"],
                row2["SR"],
                row2["4s"],
                row2["6s"],
                row2["50s"],
                row2["100s"]
            ]
        })

        st.dataframe(comparison_df)

        graph_df = pd.DataFrame({

            "Statistic": [
                "Runs",
                "Strike Rate",
                "Fours",
                "Sixes"
            ],

            player1: [
                row1["Runs"],
                row1["SR"],
                row1["4s"],
                row1["6s"]
            ],

            player2: [
                row2["Runs"],
                row2["SR"],
                row2["4s"],
                row2["6s"]
            ]
        })

        fig = px.bar(
            graph_df,
            x="Statistic",
            y=[player1, player2],
            barmode="group",
            title=f"{player1} vs {player2}"
        )

        st.plotly_chart(fig, use_container_width=True)

# =========================================================
# 🔥 TOP BATTERS
# =========================================================

elif option == "🔥 Top Batters":

    st.title("🏏 AI Cricket Analytics")

    st.markdown(
        "## IPL 2025 Advanced Player Analytics Dashboard"
    )

    st.subheader("🔥 Top 10 Run Scorers")

    top_runs = batters.sort_values(
        by="Runs",
        ascending=False
    ).head(10)

    fig = px.bar(
        top_runs,
        x="Player Name",
        y="Runs",
        color="Runs",
        text="Runs",
        title="Top 10 Run Scorers IPL 2025"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(top_runs)

# =========================================================
# 🎯 TOP BOWLERS
# =========================================================

elif option == "🎯 Top Bowlers":

    st.title("🏏 AI Cricket Analytics")

    st.markdown(
        "## IPL 2025 Advanced Player Analytics Dashboard"
    )

    st.subheader("🎯 Top 10 Wicket Takers")

    top_wickets = bowlers.sort_values(
        by="WKT",
        ascending=False
    ).head(10)

    fig2 = px.bar(
        top_wickets,
        x="Player Name",
        y="WKT",
        color="WKT",
        text="WKT",
        title="Top 10 Wicket Takers IPL 2025"
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.dataframe(top_wickets)

# =========================================================
# 🔴 LIVE SCORES
# =========================================================

elif option == "🔴 Live Scores":

    st.title("🏏UPCOMING INDIA MATCHES")


    # =====================================================
    # API KEY
    # =====================================================

    api_key = "079ac7d2-c7aa-4060-8a59-c7e730e303cc"

    # =====================================================
    # API URL
    # =====================================================

    url = (
        f"https://api.cricapi.com/v1/matches?"
        f"apikey={api_key}&offset=0"
    )

    # =====================================================
    # API REQUEST
    # =====================================================

    try:

        response = requests.get(
            url,
            timeout=10
        )

        data = response.json()

    except requests.exceptions.RequestException:

        st.error(
            "⚠ Unable to connect to Cricket API right now"
        )

        st.stop()

    # =====================================================
    # CHECK DATA
    # =====================================================

    if "data" in data:

        matches = data["data"]

        found = False

        for match in matches:

            match_name = match.get("name", "")

            # =================================================
            # IPL + INDIA FILTER
            # =================================================

            if (

                "India" in match_name
                or "IPL" in match_name
                or "Mumbai Indians" in match_name
                or "Chennai Super Kings" in match_name
                or "Royal Challengers Bengaluru" in match_name
                or "Kolkata Knight Riders" in match_name
                or "Sunrisers Hyderabad" in match_name
                or "Delhi Capitals" in match_name
                or "Rajasthan Royals" in match_name
                or "Pbks" in match_name
                or "Lucknow Super Giants" in match_name
                or "Gt" in match_name

            ):

                found = True

                st.markdown("---")

                st.subheader(match_name)

                st.write(
                    "🏆 Status:",
                    match.get(
                        "status",
                        "Not Available"
                    )
                )

                st.write(
                    "📍 Venue:",
                    match.get(
                        "venue",
                        "Not Available"
                    )
                )

                st.write(
                    "📅 Date:",
                    match.get(
                        "date",
                        "Not Available"
                    )
                )

                # =================================================
                # SCORE SECTION
                # =================================================

                if "score" in match:

                    for inning in match["score"]:

                        st.markdown(f"""
### 🏏 {inning['inning']}

# {inning['r']}/{inning['w']}

### Overs: {inning['o']}
""")

        # =================================================
        # NO MATCHES
        # =================================================

        if not found:

            st.warning(
                "No India or IPL matches available currently"
            )

    else:

        st.error(
            "Unable to fetch live scores"
        )







# =========================================================
# 🏆 TEAM ANALYTICS
# =========================================================

elif option == "🏆 Team Analytics":

    st.title("🏏 AI Cricket Analytics")

    st.markdown(
        "## IPL 2025 Team Analytics Dashboard"
    )

    st.subheader("🏆 Team Performance Analysis")

    # =====================================================
    # TEAM RUNS
    # =====================================================

    st.subheader("🔥 Top Batting Teams")

    team_runs = batters.groupby(
        "Team"
    )["Runs"].sum().reset_index()

    team_runs = team_runs.sort_values(
        by="Runs",
        ascending=False
    )

    fig1 = px.bar(
        team_runs,
        x="Team",
        y="Runs",
        color="Runs",
        text="Runs",
        title="Team Total Runs"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    st.dataframe(team_runs)

    # =====================================================
    # TEAM WICKETS
    # =====================================================

    st.subheader("🎯 Top Bowling Teams")

    team_wickets = bowlers.groupby(
        "Team"
    )["WKT"].sum().reset_index()

    team_wickets = team_wickets.sort_values(
        by="WKT",
        ascending=False
    )

    fig2 = px.bar(
        team_wickets,
        x="Team",
        y="WKT",
        color="WKT",
        text="WKT",
        title="Team Total Wickets"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    st.dataframe(team_wickets)






# =========================================================
# 🟠 ORANGE & 🟣 PURPLE CAP
# =========================================================

elif option == "🟠 Orange & Purple Cap":

    st.title("🏏 IPL 2025 Cap Leaders")

    st.markdown(
        "## 🟠 Orange Cap & 🟣 Purple Cap"
    )

    # =====================================================
    # ORANGE CAP
    # =====================================================

    st.subheader("🟠 Orange Cap Leader")

    orange_cap = batters.sort_values(
        by="Runs",
        ascending=False
    ).head(1)

    orange_player = orange_cap.iloc[0]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Player",
        orange_player["Player Name"]
    )

    col2.metric(
        "Runs",
        orange_player["Runs"]
    )

    col3.metric(
        "Strike Rate",
        orange_player["SR"]
    )

    st.subheader("🔥 Top 10 Run Scorers")

    top_runs = batters.sort_values(
        by="Runs",
        ascending=False
    ).head(10)

    fig1 = px.bar(
        top_runs,
        x="Player Name",
        y="Runs",
        color="Runs",
        text="Runs",
        title="Orange Cap Leaderboard"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    # =====================================================
    # PURPLE CAP
    # =====================================================

    st.subheader("🟣 Purple Cap Leader")

    purple_cap = bowlers.sort_values(
        by="WKT",
        ascending=False
    ).head(1)

    purple_player = purple_cap.iloc[0]

    col4, col5, col6 = st.columns(3)

    col4.metric(
        "Player",
        purple_player["Player Name"]
    )

    col5.metric(
        "Wickets",
        purple_player["WKT"]
    )

    col6.metric(
        "Economy",
        purple_player["ECO"]
    )

    st.subheader("🎯 Top 10 Wicket Takers")

    top_wickets = bowlers.sort_values(
        by="WKT",
        ascending=False
    ).head(10)

    fig2 = px.bar(
        top_wickets,
        x="Player Name",
        y="WKT",
        color="WKT",
        text="WKT",
        title="Purple Cap Leaderboard"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )








# =========================================================
# 🤖 MATCH PREDICTION
# =========================================================

elif option == "🤖 Match Prediction":

    st.title("🏏 AI Match Winner Prediction")

    st.markdown(
        "## 🤖 IPL 2025 Prediction System"
    )

    # =====================================================
    # TEAM LIST
    # =====================================================

    teams = sorted(
        batters["Team"].unique()
    )

    # =====================================================
    # TEAM SELECTION
    # =====================================================

    team1 = st.selectbox(
        "Select Team 1",
        teams,
        key="team1"
    )

    team2 = st.selectbox(
        "Select Team 2",
        teams,
        key="team2"
    )

    # =====================================================
    # SAME TEAM CHECK
    # =====================================================

    if team1 == team2:

        st.warning(
            "⚠ Please select two different teams"
        )

    else:

        # =================================================
        # PREDICTION BUTTON
        # =================================================

        if st.button("Predict Winner"):

            # =============================================
            # TEAM BATTING STRENGTH
            # =============================================

            team1_runs = batters[
                batters["Team"] == team1
            ]["Runs"].sum()

            team2_runs = batters[
                batters["Team"] == team2
            ]["Runs"].sum()

            # =============================================
            # TEAM BOWLING STRENGTH
            # =============================================

            team1_wickets = bowlers[
                bowlers["Team"] == team1
            ]["WKT"].sum()

            team2_wickets = bowlers[
                bowlers["Team"] == team2
            ]["WKT"].sum()

            # =============================================
            # TEAM TOTAL PERFORMANCE SCORE
            # =============================================

            team1_score = (
                team1_runs +
                (team1_wickets * 20)
            )

            team2_score = (
                team2_runs +
                (team2_wickets * 20)
            )

            # =============================================
            # WINNING PROBABILITY
            # =============================================

            total_score = (
                team1_score +
                team2_score
            )

            team1_probability = int(
                (team1_score / total_score) * 100
            )

            team2_probability = (
                100 - team1_probability
            )

            # =============================================
            # WINNER LOGIC
            # =============================================

            if team1_score > team2_score:

                winner = team1
                probability = team1_probability

            else:

                winner = team2
                probability = team2_probability

            # =============================================
            # RESULT DISPLAY
            # =============================================

            st.success(
                f"🏆 Predicted Winner: {winner}"
            )

            st.metric(
                "Winning Probability",
                f"{probability}%"
            )

            # =============================================
            # TEAM STATS
            # =============================================

            col1, col2 = st.columns(2)

            with col1:

                st.subheader(team1)

                st.write(
                    f"🔥 Total Runs: {team1_runs}"
                )

                st.write(
                    f"🎯 Total Wickets: {team1_wickets}"
                )

            with col2:

                st.subheader(team2)

                st.write(
                    f"🔥 Total Runs: {team2_runs}"
                )

                st.write(
                    f"🎯 Total Wickets: {team2_wickets}"
                )

            # =============================================
            # PIE CHART
            # =============================================

            prediction_df = pd.DataFrame({

                "Team": [
                    team1,
                    team2
                ],

                "Probability": [
                    team1_probability,
                    team2_probability
                ]
            })

            fig = px.pie(
                prediction_df,
                names="Team",
                values="Probability",
                title="Winning Chances"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            # =============================================
            # BAR CHART
            # =============================================

            compare_df = pd.DataFrame({

                "Team": [
                    team1,
                    team2
                ],

                "Performance Score": [
                    team1_score,
                    team2_score
                ]
            })

            fig2 = px.bar(
                compare_df,
                x="Team",
                y="Performance Score",
                color="Performance Score",
                text="Performance Score",
                title="Team Strength Comparison"
            )

            st.plotly_chart(
                fig2,
                use_container_width=True
            )




# =========================================================
# ⚔️ HEAD TO HEAD ANALYSIS
# =========================================================

elif option == "⚔️ Head To Head":

    st.title("🏏 IPL Head To Head Analysis")

    st.markdown(
        "## ⚔️ Team vs Team Comparison"
    )

    # =====================================================
    # TEAM LIST
    # =====================================================

    teams = sorted(
        batters["Team"].unique()
    )

    # =====================================================
    # TEAM SELECTION
    # =====================================================

    team1 = st.selectbox(
        "Select Team 1",
        teams,
        key="h2h1"
    )

    team2 = st.selectbox(
        "Select Team 2",
        teams,
        key="h2h2"
    )

    # =====================================================
    # SAME TEAM CHECK
    # =====================================================

    if team1 == team2:

        st.warning(
            "⚠ Select different teams"
        )

    else:

        # =================================================
        # TEAM STATS
        # =================================================

        team1_runs = batters[
            batters["Team"] == team1
        ]["Runs"].sum()

        team2_runs = batters[
            batters["Team"] == team2
        ]["Runs"].sum()

        team1_wickets = bowlers[
            bowlers["Team"] == team1
        ]["WKT"].sum()

        team2_wickets = bowlers[
            bowlers["Team"] == team2
        ]["WKT"].sum()

        # =================================================
        # PERFORMANCE SCORE
        # =================================================

        team1_score = (
            team1_runs +
            (team1_wickets * 20)
        )

        team2_score = (
            team2_runs +
            (team2_wickets * 20)
        )

        # =================================================
        # WIN PERCENTAGE
        # =================================================

        total = team1_score + team2_score

        team1_percent = int(
            (team1_score / total) * 100
        )

        team2_percent = (
            100 - team1_percent
        )

        # =================================================
        # TEAM METRICS
        # =================================================

        col1, col2 = st.columns(2)

        with col1:

            st.subheader(team1)

            st.metric(
                "🔥 Runs",
                team1_runs
            )

            st.metric(
                "🎯 Wickets",
                team1_wickets
            )

            st.metric(
                "🏆 Strength",
                team1_score
            )

        with col2:

            st.subheader(team2)

            st.metric(
                "🔥 Runs",
                team2_runs
            )

            st.metric(
                "🎯 Wickets",
                team2_wickets
            )

            st.metric(
                "🏆 Strength",
                team2_score
            )

        # =================================================
        # WINNER
        # =================================================

        if team1_score > team2_score:

            winner = team1

        else:

            winner = team2

        st.success(
            f"🏆 Stronger Team: {winner}"
        )

        # =================================================
        # PIE CHART
        # =================================================

        compare_df = pd.DataFrame({

            "Team": [
                team1,
                team2
            ],

            "Winning Chance": [
                team1_percent,
                team2_percent
            ]
        })

        fig = px.pie(

            compare_df,

            names="Team",

            values="Winning Chance",

            title="Head To Head Winning Chances"

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )










st.markdown("""

<style>

/* ========================================
MAIN BACKGROUND
======================================== */

.stApp {

    background: linear-gradient(
        135deg,
        #020617,
        #0F172A,
        #111827
    );

    color: white;
}

/* ========================================
SIDEBAR
======================================== */

section[data-testid="stSidebar"] {

    background: linear-gradient(
        180deg,
        #020617,
        #0F172A
    );

    min-width: 260px !important;

    max-width: 260px !important;
}

/* ========================================
HEADINGS
======================================== */

h1 {

    color: #FACC15 !important;

    font-size: 48px !important;

    font-weight: 800 !important;
}

h2 {

    color: white !important;
}

h3 {

    color: #E2E8F0 !important;
}

/* ========================================
TEXT
======================================== */

p,
label {

    color: white !important;
}

/* ========================================
SELECTBOX
======================================== */

div[data-baseweb="select"] {

    background-color: white !important;

    border-radius: 12px !important;

    border: 2px solid #2563EB !important;
}

/* SELECTED TEXT */

div[data-baseweb="select"] span {

    color: black !important;

    font-weight: bold !important;
}

/* ========================================
BUTTONS
======================================== */

.stButton button {

    background: linear-gradient(
        90deg,
        #2563EB,
        #7C3AED
    );

    color: white !important;

    border: none;

    border-radius: 12px;

    padding: 12px 20px;

    font-size: 16px;

    font-weight: bold;
}

/* ========================================
METRIC CARDS
======================================== */

div[data-testid="metric-container"] {

    background: linear-gradient(
        145deg,
        #111827,
        #1E293B
    );

    border: 1px solid #334155;

    padding: 18px;

    border-radius: 18px;

    box-shadow: 0px 4px 15px rgba(0,0,0,0.5);
}

/* METRIC LABEL */

[data-testid="stMetricLabel"] {

    color: #CBD5E1 !important;

    font-size: 15px !important;

    font-weight: 600 !important;
}

/* METRIC VALUE */

[data-testid="stMetricValue"] {

    color: white !important;

    font-size: 34px !important;

    font-weight: bold !important;
}

/* ========================================
DATAFRAME
======================================== */

[data-testid="stDataFrame"] {

    background-color: white !important;

    border-radius: 12px;
}

/* TABLE TEXT */

table {

    color: black !important;
}

/* ========================================
ALERTS
======================================== */

.stAlert {

    border-radius: 15px;
}

/* ========================================
SCROLLBAR
======================================== */

::-webkit-scrollbar {

    width: 10px;
}

::-webkit-scrollbar-thumb {

    background: #2563EB;

    border-radius: 10px;
}

/* ========================================
REMOVE STREAMLIT BRANDING
======================================== */

header {

    visibility: hidden;
}

footer {

    visibility: hidden;
}

</style>

""", unsafe_allow_html=True)

    st.dataframe(top_runs)

# =========================================================
# 🎯 TOP BOWLERS
# =========================================================

elif option == "🎯 Top Bowlers":

    st.title("🏏 AI Cricket Analytics")

    st.markdown(
        "## IPL 2025 Advanced Player Analytics Dashboard"
    )

    st.subheader("🎯 Top 10 Wicket Takers")

    top_wickets = bowlers.sort_values(
        by="WKT",
        ascending=False
    ).head(10)

    fig2 = px.bar(
        top_wickets,
        x="Player Name",
        y="WKT",
        color="WKT",
        text="WKT",
        title="Top 10 Wicket Takers IPL 2025"
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.dataframe(top_wickets)

# =========================================================
# 🔴 LIVE SCORES
# =========================================================

elif option == "🔴 Live Scores":

    st.title("🏏UPCOMING INDIA MATCHES")


    # =====================================================
    # API KEY
    # =====================================================

    api_key = "079ac7d2-c7aa-4060-8a59-c7e730e303cc"

    # =====================================================
    # API URL
    # =====================================================

    url = (
        f"https://api.cricapi.com/v1/matches?"
        f"apikey={api_key}&offset=0"
    )

    # =====================================================
    # API REQUEST
    # =====================================================

    try:

        response = requests.get(
            url,
            timeout=10
        )

        data = response.json()

    except requests.exceptions.RequestException:

        st.error(
            "⚠ Unable to connect to Cricket API right now"
        )

        st.stop()

    # =====================================================
    # CHECK DATA
    # =====================================================

    if "data" in data:

        matches = data["data"]

        found = False

        for match in matches:

            match_name = match.get("name", "")

            # =================================================
            # IPL + INDIA FILTER
            # =================================================

            if (

                "India" in match_name
                or "IPL" in match_name
                or "Mumbai Indians" in match_name
                or "Chennai Super Kings" in match_name
                or "Royal Challengers Bengaluru" in match_name
                or "Kolkata Knight Riders" in match_name
                or "Sunrisers Hyderabad" in match_name
                or "Delhi Capitals" in match_name
                or "Rajasthan Royals" in match_name
                or "Pbks" in match_name
                or "Lucknow Super Giants" in match_name
                or "Gt" in match_name

            ):

                found = True

                st.markdown("---")

                st.subheader(match_name)

                st.write(
                    "🏆 Status:",
                    match.get(
                        "status",
                        "Not Available"
                    )
                )

                st.write(
                    "📍 Venue:",
                    match.get(
                        "venue",
                        "Not Available"
                    )
                )

                st.write(
                    "📅 Date:",
                    match.get(
                        "date",
                        "Not Available"
                    )
                )

                # =================================================
                # SCORE SECTION
                # =================================================

                if "score" in match:

                    for inning in match["score"]:

                        st.markdown(f"""
### 🏏 {inning['inning']}

# {inning['r']}/{inning['w']}

### Overs: {inning['o']}
""")

        # =================================================
        # NO MATCHES
        # =================================================

        if not found:

            st.warning(
                "No India or IPL matches available currently"
            )

    else:

        st.error(
            "Unable to fetch live scores"
        )







# =========================================================
# 🏆 TEAM ANALYTICS
# =========================================================

elif option == "🏆 Team Analytics":

    st.title("🏏 AI Cricket Analytics")

    st.markdown(
        "## IPL 2025 Team Analytics Dashboard"
    )

    st.subheader("🏆 Team Performance Analysis")

    # =====================================================
    # TEAM RUNS
    # =====================================================

    st.subheader("🔥 Top Batting Teams")

    team_runs = batters.groupby(
        "Team"
    )["Runs"].sum().reset_index()

    team_runs = team_runs.sort_values(
        by="Runs",
        ascending=False
    )

    fig1 = px.bar(
        team_runs,
        x="Team",
        y="Runs",
        color="Runs",
        text="Runs",
        title="Team Total Runs"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    st.dataframe(team_runs)

    # =====================================================
    # TEAM WICKETS
    # =====================================================

    st.subheader("🎯 Top Bowling Teams")

    team_wickets = bowlers.groupby(
        "Team"
    )["WKT"].sum().reset_index()

    team_wickets = team_wickets.sort_values(
        by="WKT",
        ascending=False
    )

    fig2 = px.bar(
        team_wickets,
        x="Team",
        y="WKT",
        color="WKT",
        text="WKT",
        title="Team Total Wickets"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    st.dataframe(team_wickets)






# =========================================================
# 🟠 ORANGE & 🟣 PURPLE CAP
# =========================================================

elif option == "🟠 Orange & Purple Cap":

    st.title("🏏 IPL 2025 Cap Leaders")

    st.markdown(
        "## 🟠 Orange Cap & 🟣 Purple Cap"
    )

    # =====================================================
    # ORANGE CAP
    # =====================================================

    st.subheader("🟠 Orange Cap Leader")

    orange_cap = batters.sort_values(
        by="Runs",
        ascending=False
    ).head(1)

    orange_player = orange_cap.iloc[0]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Player",
        orange_player["Player Name"]
    )

    col2.metric(
        "Runs",
        orange_player["Runs"]
    )

    col3.metric(
        "Strike Rate",
        orange_player["SR"]
    )

    st.subheader("🔥 Top 10 Run Scorers")

    top_runs = batters.sort_values(
        by="Runs",
        ascending=False
    ).head(10)

    fig1 = px.bar(
        top_runs,
        x="Player Name",
        y="Runs",
        color="Runs",
        text="Runs",
        title="Orange Cap Leaderboard"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    # =====================================================
    # PURPLE CAP
    # =====================================================

    st.subheader("🟣 Purple Cap Leader")

    purple_cap = bowlers.sort_values(
        by="WKT",
        ascending=False
    ).head(1)

    purple_player = purple_cap.iloc[0]

    col4, col5, col6 = st.columns(3)

    col4.metric(
        "Player",
        purple_player["Player Name"]
    )

    col5.metric(
        "Wickets",
        purple_player["WKT"]
    )

    col6.metric(
        "Economy",
        purple_player["ECO"]
    )

    st.subheader("🎯 Top 10 Wicket Takers")

    top_wickets = bowlers.sort_values(
        by="WKT",
        ascending=False
    ).head(10)

    fig2 = px.bar(
        top_wickets,
        x="Player Name",
        y="WKT",
        color="WKT",
        text="WKT",
        title="Purple Cap Leaderboard"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )








# =========================================================
# 🤖 MATCH PREDICTION
# =========================================================

elif option == "🤖 Match Prediction":

    st.title("🏏 AI Match Winner Prediction")

    st.markdown(
        "## 🤖 IPL 2025 Prediction System"
    )

    # =====================================================
    # TEAM LIST
    # =====================================================

    teams = sorted(
        batters["Team"].unique()
    )

    # =====================================================
    # TEAM SELECTION
    # =====================================================

    team1 = st.selectbox(
        "Select Team 1",
        teams,
        key="team1"
    )

    team2 = st.selectbox(
        "Select Team 2",
        teams,
        key="team2"
    )

    # =====================================================
    # SAME TEAM CHECK
    # =====================================================

    if team1 == team2:

        st.warning(
            "⚠ Please select two different teams"
        )

    else:

        # =================================================
        # PREDICTION BUTTON
        # =================================================

        if st.button("Predict Winner"):

            # =============================================
            # TEAM BATTING STRENGTH
            # =============================================

            team1_runs = batters[
                batters["Team"] == team1
            ]["Runs"].sum()

            team2_runs = batters[
                batters["Team"] == team2
            ]["Runs"].sum()

            # =============================================
            # TEAM BOWLING STRENGTH
            # =============================================

            team1_wickets = bowlers[
                bowlers["Team"] == team1
            ]["WKT"].sum()

            team2_wickets = bowlers[
                bowlers["Team"] == team2
            ]["WKT"].sum()

            # =============================================
            # TEAM TOTAL PERFORMANCE SCORE
            # =============================================

            team1_score = (
                team1_runs +
                (team1_wickets * 20)
            )

            team2_score = (
                team2_runs +
                (team2_wickets * 20)
            )

            # =============================================
            # WINNING PROBABILITY
            # =============================================

            total_score = (
                team1_score +
                team2_score
            )

            team1_probability = int(
                (team1_score / total_score) * 100
            )

            team2_probability = (
                100 - team1_probability
            )

            # =============================================
            # WINNER LOGIC
            # =============================================

            if team1_score > team2_score:

                winner = team1
                probability = team1_probability

            else:

                winner = team2
                probability = team2_probability

            # =============================================
            # RESULT DISPLAY
            # =============================================

            st.success(
                f"🏆 Predicted Winner: {winner}"
            )

            st.metric(
                "Winning Probability",
                f"{probability}%"
            )

            # =============================================
            # TEAM STATS
            # =============================================

            col1, col2 = st.columns(2)

            with col1:

                st.subheader(team1)

                st.write(
                    f"🔥 Total Runs: {team1_runs}"
                )

                st.write(
                    f"🎯 Total Wickets: {team1_wickets}"
                )

            with col2:

                st.subheader(team2)

                st.write(
                    f"🔥 Total Runs: {team2_runs}"
                )

                st.write(
                    f"🎯 Total Wickets: {team2_wickets}"
                )

            # =============================================
            # PIE CHART
            # =============================================

            prediction_df = pd.DataFrame({

                "Team": [
                    team1,
                    team2
                ],

                "Probability": [
                    team1_probability,
                    team2_probability
                ]
            })

            fig = px.pie(
                prediction_df,
                names="Team",
                values="Probability",
                title="Winning Chances"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            # =============================================
            # BAR CHART
            # =============================================

            compare_df = pd.DataFrame({

                "Team": [
                    team1,
                    team2
                ],

                "Performance Score": [
                    team1_score,
                    team2_score
                ]
            })

            fig2 = px.bar(
                compare_df,
                x="Team",
                y="Performance Score",
                color="Performance Score",
                text="Performance Score",
                title="Team Strength Comparison"
            )

            st.plotly_chart(
                fig2,
                use_container_width=True
            )




# =========================================================
# ⚔️ HEAD TO HEAD ANALYSIS
# =========================================================

elif option == "⚔️ Head To Head":

    st.title("🏏 IPL Head To Head Analysis")

    st.markdown(
        "## ⚔️ Team vs Team Comparison"
    )

    # =====================================================
    # TEAM LIST
    # =====================================================

    teams = sorted(
        batters["Team"].unique()
    )

    # =====================================================
    # TEAM SELECTION
    # =====================================================

    team1 = st.selectbox(
        "Select Team 1",
        teams,
        key="h2h1"
    )

    team2 = st.selectbox(
        "Select Team 2",
        teams,
        key="h2h2"
    )

    # =====================================================
    # SAME TEAM CHECK
    # =====================================================

    if team1 == team2:

        st.warning(
            "⚠ Select different teams"
        )

    else:

        # =================================================
        # TEAM STATS
        # =================================================

        team1_runs = batters[
            batters["Team"] == team1
        ]["Runs"].sum()

        team2_runs = batters[
            batters["Team"] == team2
        ]["Runs"].sum()

        team1_wickets = bowlers[
            bowlers["Team"] == team1
        ]["WKT"].sum()

        team2_wickets = bowlers[
            bowlers["Team"] == team2
        ]["WKT"].sum()

        # =================================================
        # PERFORMANCE SCORE
        # =================================================

        team1_score = (
            team1_runs +
            (team1_wickets * 20)
        )

        team2_score = (
            team2_runs +
            (team2_wickets * 20)
        )

        # =================================================
        # WIN PERCENTAGE
        # =================================================

        total = team1_score + team2_score

        team1_percent = int(
            (team1_score / total) * 100
        )

        team2_percent = (
            100 - team1_percent
        )

        # =================================================
        # TEAM METRICS
        # =================================================

        col1, col2 = st.columns(2)

        with col1:

            st.subheader(team1)

            st.metric(
                "🔥 Runs",
                team1_runs
            )

            st.metric(
                "🎯 Wickets",
                team1_wickets
            )

            st.metric(
                "🏆 Strength",
                team1_score
            )

        with col2:

            st.subheader(team2)

            st.metric(
                "🔥 Runs",
                team2_runs
            )

            st.metric(
                "🎯 Wickets",
                team2_wickets
            )

            st.metric(
                "🏆 Strength",
                team2_score
            )

        # =================================================
        # WINNER
        # =================================================

        if team1_score > team2_score:

            winner = team1

        else:

            winner = team2

        st.success(
            f"🏆 Stronger Team: {winner}"
        )

        # =================================================
        # PIE CHART
        # =================================================

        compare_df = pd.DataFrame({

            "Team": [
                team1,
                team2
            ],

            "Winning Chance": [
                team1_percent,
                team2_percent
            ]
        })

        fig = px.pie(

            compare_df,

            names="Team",

            values="Winning Chance",

            title="Head To Head Winning Chances"

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )










st.markdown("""

<style>

/* ========================================
MAIN BACKGROUND
======================================== */

.stApp {

    background: linear-gradient(
        135deg,
        #020617,
        #0F172A,
        #111827
    );

    color: white;
}

/* ========================================
SIDEBAR
======================================== */

section[data-testid="stSidebar"] {

    background: linear-gradient(
        180deg,
        #020617,
        #0F172A
    );

    min-width: 260px !important;

    max-width: 260px !important;
}

/* ========================================
HEADINGS
======================================== */

h1 {

    color: #FACC15 !important;

    font-size: 48px !important;

    font-weight: 800 !important;
}

h2 {

    color: white !important;
}

h3 {

    color: #E2E8F0 !important;
}

/* ========================================
TEXT
======================================== */

p,
label {

    color: white !important;
}

/* ========================================
SELECTBOX
======================================== */

div[data-baseweb="select"] {

    background-color: white !important;

    border-radius: 12px !important;

    border: 2px solid #2563EB !important;
}

/* SELECTED TEXT */

div[data-baseweb="select"] span {

    color: black !important;

    font-weight: bold !important;
}

/* ========================================
BUTTONS
======================================== */

.stButton button {

    background: linear-gradient(
        90deg,
        #2563EB,
        #7C3AED
    );

    color: white !important;

    border: none;

    border-radius: 12px;

    padding: 12px 20px;

    font-size: 16px;

    font-weight: bold;
}

/* ========================================
METRIC CARDS
======================================== */

div[data-testid="metric-container"] {

    background: linear-gradient(
        145deg,
        #111827,
        #1E293B
    );

    border: 1px solid #334155;

    padding: 18px;

    border-radius: 18px;

    box-shadow: 0px 4px 15px rgba(0,0,0,0.5);
}

/* METRIC LABEL */

[data-testid="stMetricLabel"] {

    color: #CBD5E1 !important;

    font-size: 15px !important;

    font-weight: 600 !important;
}

/* METRIC VALUE */

[data-testid="stMetricValue"] {

    color: white !important;

    font-size: 34px !important;

    font-weight: bold !important;
}

/* ========================================
DATAFRAME
======================================== */

[data-testid="stDataFrame"] {

    background-color: white !important;

    border-radius: 12px;
}

/* TABLE TEXT */

table {

    color: black !important;
}

/* ========================================
ALERTS
======================================== */

.stAlert {

    border-radius: 15px;
}

/* ========================================
SCROLLBAR
======================================== */

::-webkit-scrollbar {

    width: 10px;
}

::-webkit-scrollbar-thumb {

    background: #2563EB;

    border-radius: 10px;
}

/* ========================================
REMOVE STREAMLIT BRANDING
======================================== */

header {

    visibility: hidden;
}

footer {

    visibility: hidden;
}

</style>

""", unsafe_allow_html=True)
