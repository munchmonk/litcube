import streamlit as st

from db import get_connection


if "conn" not in st.session_state:
    conn = get_connection()
    st.session_state["conn"] = conn

pages = [
    st.Page("homepage.py", title="Home"),
    st.Page("new_tournament.py", title="New tournament"),
    st.Page("running_tournament.py", title="Running tournaments")
]

pages = st.navigation(pages)
pages.run()
