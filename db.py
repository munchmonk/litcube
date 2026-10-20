import streamlit as st
import pandas as pd
from databricks import sql


def get_connection():
    cfg = st.secrets["databricks"]

    return sql.connect(
        server_hostname=cfg["server_hostname"],
        http_path=cfg["http_path"],
        access_token=cfg["access_token"]
    )


def fetch(conn, query):
    with conn.cursor() as cursor:
        cursor.execute(query)
        rows=cursor.fetchall()
        columns = [col[0] for col in cursor.description]

    return pd.DataFrame(rows, columns=columns)


def execute(conn, query, parameters={}):
    with conn.cursor() as cursor:
        cursor.execute(query, parameters=parameters)
        rows=cursor.fetchall()
        columns = [col[0] for col in cursor.description]

    return pd.DataFrame(rows, columns=columns)
