import streamlit as st
import pandas as pd

ARCHIVO = "incidencias.csv"

st.set_page_config(page_title="Gestor de Incidencias", page_icon="🔧", layout="wide")

st.title("🔧 Panel de Gestión de Incidencias")
st.markdown("---")

df = pd.read_csv(ARCHIVO)

# --- FILTROS ENCADENADOS ---
st.subheader("Filtros")
col_f1, col_f2, col_f3 = st.columns(3)

with col_f1:
    filtro_estado = st.selectbox("Estado", ["Todos"] + sorted(df["estado"].unique().tolist()))

df_paso1 = df.copy()
if filtro_estado != "Todos":
    df_paso1 = df_paso1[df_paso1["estado"] == filtro_estado]

with col_f2:
    filtro_prioridad = st.selectbox("Prioridad", ["Todos"] + sorted(df_paso1["prioridad"].unique().tolist()))

df_paso2 = df_paso1.copy()
if filtro_prioridad != "Todos":
    df_paso2 = df_paso2[df_paso2["prioridad"] == filtro_prioridad]

with col_f3:
    filtro_tipo = st.selectbox("Tipo", ["Todos"] + sorted(df_paso2["tipo"].unique().tolist()))

df_filtrado = df_paso2.copy()
if filtro_tipo != "Todos":
    df_filtrado = df_filtrado[df_filtrado["tipo"] == filtro_tipo]

st.markdown("---")

# --- MÉTRICAS sobre datos filtrados ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("📋 Total", len(df_filtrado))
col2.metric("🔴 Abiertas", len(df_filtrado[df_filtrado["estado"] == "abierta"]))
col3.metric("✅ Cerradas", len(df_filtrado[df_filtrado["estado"] == "cerrada"]))
col4.metric("⚠️ Alta prioridad", len(df_filtrado[df_filtrado["prioridad"] == "alta"]))

st.markdown("---")

# --- GRÁFICAS sobre datos filtrados ---
col_g1, col_g2 = st.columns(2)

with col_g1:
    st.subheader("Por prioridad")
    if not df_filtrado.empty:
        st.bar_chart(df_filtrado["prioridad"].value_counts())
    else:
        st.info("Sin datos para mostrar")

with col_g2:
    st.subheader("Por tipo")
    if not df_filtrado.empty:
        st.bar_chart(df_filtrado["tipo"].value_counts())
    else:
        st.info("Sin datos para mostrar")

st.markdown("---")

# --- TABLA ---
st.subheader(f"Incidencias ({len(df_filtrado)} resultados)")
st.dataframe(df_filtrado, use_container_width=True)