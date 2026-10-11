import streamlit as st
import pandas as pd
from databricks import sql

st.title("My new app - no balloons allowed")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

def get_connection():
    cfg = st.secrets["databricks"]

    return sql.connect(
        server_hostname=cfg["server_hostname"],
        http_path=cfg["http_path"],
        access_token=cfg["access_token"]
    )

def get_test_data(conn):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM workspace.magic.gold_cube_cobra LIMIT 3")
        rows=cursor.fetchall()
        columns = [col[0] for col in cursor.description]

    return pd.DataFrame(rows, columns=columns)

conn = get_connection()

try:
    df = get_test_data(conn)
    st.success("Connected to Databricks successfully!")
    st.dataframe(df, use_container_width=True)
except Exception:
    st.error(
        "The connection or query failed. "
        "Check your secrets, authentication, "
        "warehouse status and permissions."
    )

