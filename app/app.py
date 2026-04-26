import streamlit as st
import sqlite3
import pandas as pd

conn = sqlite3.connect("data/titanic.db")

df = pd.read_sql("SELECT * FROM passengers", conn)

st.title("Titanic Dashboard")

st.write("### Sobrevivência por sexo")
st.bar_chart(df.groupby("sex")["survived"].mean())

st.write("### Idade média por classe")
st.bar_chart(df.groupby("pclass")["age"].mean())