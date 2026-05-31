import streamlit as st
import pandas as pd

ARCHIVO = "incidencias.csv"

st.set_page_config(page_title="Gestor de Incidencias", page_icon="🔧", layout="wide")

st.title("🔧 Panel de Gestión de Incidencias")
st.markdown("---")

df = pd.read_csv(ARCHIVO)

# --- MÉTRICAS ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("📋 Total", len(df))
col2.metric("🔴 Abiertas", len(df[df["estado"] == "abierta"]))
col3.metric("✅ Cerradas", len(df[df["estado"] == "cerrada"]))
col4.metric("⚠️ Alta prioridad", len(df[df["prioridad"] == "alta"]))

st.markdown("---")

# --- FILTROS ---
st.subheader("Filtros")
col_f1, col_f2, col_f3 = st.columns(3)

with col_f1:
    filtro_estado = st.selectbox("Estado", ["Todos", "abierta", "cerrada"])
with col_f2:
    filtro_prioridad = st.selectbox("Prioridad", ["Todos", "alta", "media", "baja"])
with col_f3:
    filtro_tipo = st.selectbox("Tipo", ["Todos"] + sorted(df["tipo"].unique().tolist()))

df_filtrado = df.copy()
if filtro_estado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["estado"] == filtro_estado]
if filtro_prioridad != "Todos":
    df_filtrado = df_filtrado[df_filtrado["prioridad"] == filtro_prioridad]
if filtro_tipo != "Todos":
    df_filtrado = df_filtrado[df_filtrado["tipo"] == filtro_tipo]

st.markdown("---")

# --- GRÁFICAS ---
col_g1, col_g2 = st.columns(2)

with col_g1:
    st.subheader("Por prioridad")
    st.bar_chart(df["prioridad"].value_counts())

with col_g2:
    st.subheader("Por tipo")
    st.bar_chart(df["tipo"].value_counts())

st.markdown("---")

# --- TABLA ---
st.subheader(f"Incidencias ({len(df_filtrado)} resultados)")
st.dataframe(df_filtrado, use_container_width=True)