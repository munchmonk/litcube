import streamlit as st

from db import fetch
from tournament_utils import generate_random_teams, TWO_TEAMS

st.title("Continue an existing tournament")

running_tournament_query = """
    SELECT 
        T.tournament_id, 
        T.tournament_date, 
        T.num_rounds, 
        DT.draft_type_name, 
        TT.team_type_name, 
        DL.draft_location_name, 
        collect_list(P.player_id) AS player_ids,
        collect_list(P.player_name) AS player_names
    FROM workspace.litcube.tournament T
    INNER JOIN workspace.litcube.dim_draft_type DT ON DT.draft_type_id = T.draft_type_id
    INNER JOIN workspace.litcube.dim_team_type TT ON TT.team_type_id = T.team_type_id
    INNER JOIN workspace.litcube.dim_draft_location DL ON DL.draft_location_id = T.draft_location_id
    INNER JOIN workspace.litcube.dim_player P ON array_contains(T.player_ids, P.player_id)
    WHERE T.is_still_running
    GROUP BY T.tournament_id, T.tournament_date, T.num_rounds, DT.draft_type_name, TT.team_type_name, DL.draft_location_name
"""
df_running_tournaments = fetch(st.session_state["conn"], running_tournament_query)

if not df_running_tournaments.empty:
    st.selectbox(
        "Choose a running tournament:", 
        df_running_tournaments["tournament_id"],
        index=None, 
        key="running_tournament_picker", 
        persist_state="page"
    )
else:
    st.header("No running tournaments. Create a new one first!")

if "running_tournament_picker" in st.session_state and st.session_state["running_tournament_picker"]:
    team_1_query = f"""
        SELECT collect_list(player_name) AS players
        FROM workspace.litcube.tournament T 
        INNER JOIN workspace.litcube.dim_player P ON array_contains(T.team_1, P.player_id)
        WHERE tournament_id = {st.session_state["running_tournament_picker"]}
    """
    df_team_1 = fetch(st.session_state["conn"], team_1_query)

    team_2_query = f"""
        SELECT collect_list(player_name) AS players
        FROM workspace.litcube.tournament T 
        INNER JOIN workspace.litcube.dim_player P ON array_contains(T.team_2, P.player_id)
        WHERE tournament_id = {st.session_state["running_tournament_picker"]}
    """
    df_team_2 = fetch(st.session_state["conn"], team_2_query)

    tournament = df_running_tournaments[df_running_tournaments["tournament_id"] == st.session_state["running_tournament_picker"]]
    st.write(f"Tournament date: {tournament["tournament_date"].iloc[0]}")
    st.write(f"Players: {str(tournament["player_names"].iloc[0]).replace("[", "").replace("]", "").replace("'", "")}")
    st.write(f"Team 1: {str(df_team_1.iloc[0, 0]).replace("[", "").replace("]", "").replace("'", "")}")
    st.write(f"Team 2: {str(df_team_2.iloc[0, 0]).replace("[", "").replace("]", "").replace("'", "")}")
    st.write(f"Draft type: {tournament["draft_type_name"].iloc[0]}")
    st.write(f"Team type: {tournament["team_type_name"].iloc[0]}")
    st.write(f"Number of rounds: {tournament["num_rounds"].iloc[0]}")
    st.write(f"Location: {tournament["draft_location_name"].iloc[0]}")

    # To be amended to account for three teams
    if tournament["team_type_name"].iloc[0] == TWO_TEAMS:
        st.button(
            "Generate random teams",
            key="random_teams_button",
            on_click=generate_random_teams,
            args=[st.session_state["running_tournament_picker"], tournament["team_type_name"].iloc[0], tournament["player_ids"].iloc[0]]
        )

        if st.session_state["random_teams_button"]:
            st.success("Teams generated!")

