import streamlit as st

from db import fetch, execute

MIN_ROUNDS = 1
MAX_ROUNDS = 4

st.title("Create a new tournament")

# Tournament date
st.date_input(
    "Select the tournament date:", 
    key="tournament_date_picker", 
    persist_state="page"
)

# Draft type
draft_type_query = "SELECT * FROM workspace.litcube.dim_draft_type"
df_draft_type = fetch(st.session_state["conn"], draft_type_query)
st.selectbox(
    "Select the draft type:", 
    df_draft_type["draft_type_id"],
    format_func=lambda x: df_draft_type[df_draft_type["draft_type_id"] == x]["draft_type_name"].iloc[0],
    index=None, 
    key="draft_type_picker", 
    persist_state="page"
)

# Team type
team_type_query = "SELECT * FROM workspace.litcube.dim_team_type"
df_team_type = fetch(st.session_state["conn"], team_type_query)
st.selectbox(
    "Select the draft type:", 
    df_team_type["team_type_id"],
    format_func=lambda x: df_team_type[df_team_type["team_type_id"] == x]["team_type_name"].iloc[0],
    index=None, 
    key="team_type_picker", 
    persist_state="page"
)

# Num rounds
st.selectbox(
    "Select the number of rounds:", 
    range(MIN_ROUNDS, MAX_ROUNDS + 1),
    index=None, 
    key="num_rounds_picker", 
    persist_state="page"
)

# Draft location
draft_location_query = "SELECT * FROM workspace.litcube.dim_draft_location"
df_draft_location = fetch(st.session_state["conn"], draft_location_query)
st.selectbox(
    "Select the draft location:", 
    df_draft_location["draft_location_id"],
    format_func=lambda x: df_draft_location[df_draft_location["draft_location_id"] == x]["draft_location_name"].iloc[0],
    index=None, 
    key="draft_location_picker", 
    persist_state="page"
)

# Players
players_query = "SELECT * FROM workspace.litcube.dim_player"
df_players = fetch(st.session_state["conn"], players_query)
st.multiselect(
    "Choose all participants:",
    df_players["player_id"],
    format_func=lambda x: df_players[df_players["player_id"] == x]["player_name"].iloc[0],
    select_all=False,
    key="players_picker", 
    persist_state="page"
)

if st.session_state["tournament_date_picker"] is not None and \
    st.session_state["draft_type_picker"] is not None and \
    st.session_state["team_type_picker"] is not None and \
    st.session_state["num_rounds_picker"] is not None and \
    st.session_state["draft_location_picker"] is not None and \
    len(st.session_state["players_picker"]) > 1:

    st.button("Create new tournament!", key="new_tournament_button")

    if st.session_state["new_tournament_button"]:
        new_tournament_id = int(fetch(st.session_state["conn"], "SELECT coalesce(max(tournament_id) + 1, 1) FROM workspace.litcube.tournament").iloc[0, 0])

        execute(
            st.session_state["conn"],
            """
            INSERT INTO workspace.litcube.tournament
            VALUES (
                :tournament_id, :tournament_date, :draft_type_id, :team_type_id, 
                :num_rounds, :draft_location_id, split(:player_ids, ","), NULL, NULL, NULL, :rounds, :is_still_running
            )
            """,
            parameters = {
                "tournament_id": new_tournament_id,
                "tournament_date": st.session_state["tournament_date_picker"],
                "draft_type_id": st.session_state["draft_type_picker"],
                "team_type_id": st.session_state["team_type_picker"],
                "num_rounds": st.session_state["num_rounds_picker"],
                "draft_location_id": st.session_state["draft_location_picker"],
                "player_ids": str(st.session_state["players_picker"])[1:-1],
                "rounds": None,
                "is_still_running": True
            }
        )

        st.success(f"New tournament created successfully! Tournament ID: {new_tournament_id}")


