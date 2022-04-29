import mysql.connector
import streamlit as st


@st.experimental_singleton
def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])

conn = init_connection()


@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

rows = run_query("SELECT * from tweets;")


for row in rows:
    st.write(f"{row[0]} has a :{row[1]}:")
