# python
import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Titanic Dashboard", layout="wide", page_icon="🚢")

# --- load data ---
conn = sqlite3.connect("data/titanic.db")
df = pd.read_sql("SELECT * FROM passengers", conn)
conn.close()

# basic cleaning / types
df['age'] = pd.to_numeric(df['age'], errors='coerce')
df['fare'] = pd.to_numeric(df['fare'], errors='coerce')
df['survived'] = df['survived'].astype(int)

# --- sidebar filters ---
st.sidebar.header("Filtros")
sex_options = ["Todos"] + sorted(df['sex'].dropna().unique().tolist())
pclass_options = ["Todos"] + sorted(df['pclass'].dropna().unique().tolist())
sex = st.sidebar.selectbox("Sexo", sex_options)
pclass = st.sidebar.selectbox("Classe (pclass)", pclass_options)
age_min, age_max = int(df['age'].min(skipna=True)), int(df['age'].max(skipna=True))
age_range = st.sidebar.slider("Faixa etária", age_min, age_max, (age_min, age_max))

# apply filters
filtered = df.copy()
if sex != "Todos":
    filtered = filtered[filtered['sex'] == sex]
if pclass != "Todos":
    filtered = filtered[filtered['pclass'] == pclass]
filtered = filtered[(filtered['age'] >= age_range[0]) & (filtered['age'] <= age_range[1])]

# --- style (small card-like CSS) ---
st.markdown(
    """
    <style>
    .card {background: #f8f9fb; padding: 12px; border-radius: 8px; margin-bottom: 10px;}
    .stMetric {padding: 6px 10px;}
    </style>
    """,
    unsafe_allow_html=True,
)

# --- header ---
st.title("Titanic Dashboard")
st.markdown("Visualização interativa com filtros. Selecione opções na barra lateral.")

# --- KPIs ---
survival_rate = filtered['survived'].mean() * 100 if not filtered.empty else 0
avg_age = filtered['age'].mean() if not filtered.empty else None
avg_fare = filtered['fare'].mean() if not filtered.empty else None

k1, k2, k3 = st.columns(3)
k1.metric("Taxa de sobrevivência", f"{survival_rate:.1f} %")
k2.metric("Idade média", f"{avg_age:.1f}" if avg_age is not None else "N/A")
k3.metric("Tarifa média (fare)", f"${avg_fare:.2f}" if avg_fare is not None else "N/A")

# --- charts ---
c1, c2 = st.columns((1, 1))

with c1:
    st.markdown('<div class="card">### Sobrevivência por sexo</div>', unsafe_allow_html=True)
    if not filtered.empty:
        fig_sex = px.bar(
            filtered.groupby("sex", dropna=False)["survived"].mean().reset_index().assign(pct=lambda d: d['survived']*100),
            x="sex", y="pct", labels={"pct":"Taxa (%)","sex":"Sexo"},
            color="sex", text="pct"
        )
        fig_sex.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig_sex.update_layout(yaxis=dict(range=[0,100]), showlegend=False, margin=dict(t=30))
        st.plotly_chart(fig_sex, use_container_width=True)
    else:
        st.info("Sem dados para os filtros selecionados.")

with c2:
    st.markdown('<div class="card">### Sobrevivência por classe</div>', unsafe_allow_html=True)
    if not filtered.empty:
        fig_class = px.bar(
            filtered.groupby("pclass", dropna=False)["survived"].mean().reset_index().assign(pct=lambda d: d['survived']*100),
            x="pclass", y="pct", labels={"pct":"Taxa (%)","pclass":"Classe"},
            color="pclass", text="pct"
        )
        fig_class.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig_class.update_layout(yaxis=dict(range=[0,100]), showlegend=False, margin=dict(t=30))
        st.plotly_chart(fig_class, use_container_width=True)
    else:
        st.info("Sem dados para os filtros selecionados.")

st.markdown("### Distribuição de idade")
if not filtered.empty:
    fig_age = px.histogram(filtered, x="age", nbins=30, color="survived", barmode="overlay",
                           labels={"age":"Idade","survived":"Sobreviveu"}, opacity=0.7)
    st.plotly_chart(fig_age, use_container_width=True)
else:
    st.info("Sem dados para os filtros selecionados.")

# --- tabela e download ---
st.markdown("### Dados (filtrados)")
st.dataframe(filtered.reset_index(drop=True).drop(columns=[col for col in filtered.columns if col.startswith("Unnamed")], errors='ignore'))

csv = filtered.to_csv(index=False).encode('utf-8')
st.download_button("Download CSV (filtrado)", csv, "titanic_filtered.csv", "text/csv")