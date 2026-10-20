import streamlit as st
import random

from db import execute

# dim_team_type
TWO_TEAMS = "Two teams"

def generate_random_teams(tournament_id, team_type, player_ids):
    """
        Generate two random teams and updates the tournament table to reflect it. Only supports two teams for now; to be expanded to include three teams.
    """
    if team_type == TWO_TEAMS:
        team_1 = []
        team_2 = [int(player) for player in player_ids]
        random.shuffle(team_2)

        while len(team_1) < len(team_2):
            team_1.append(team_2.pop())
        
        team_1.sort()
        team_2.sort()

        execute(
            st.session_state["conn"],
            """
            UPDATE workspace.litcube.tournament
            SET team_1 = split(:team_1, ",")
            WHERE tournament_id = :tournament_id
            """,
            parameters = {
                "tournament_id": tournament_id,
                "team_1": str(team_1)[1:-1]
            }
        )

        execute(
            st.session_state["conn"],
            """
            UPDATE workspace.litcube.tournament
            SET team_1 = split(:team_1, ","), team_2 = split(:team_2, ",")
            WHERE tournament_id = :tournament_id
            """,
            parameters = {
                "tournament_id": tournament_id,
                "team_1": str(team_1)[1:-1],
                "team_2": str(team_2)[1:-1]
            }
        )