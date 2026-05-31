import streamlit as st
import pandas as pd
import plotly.express as px
from database import inicializar_db, obtener_incidencias

inicializar_db()

st.title("📋 Dashboard")
st.markdown("---")

datos = obtener_incidencias()

if not datos:
    st.info("No hay incidencias registradas todavía.")
else:
    df = pd.DataFrame(datos)

    # Calcular tiempo medio de resolución
    cerradas = df[df["estado"] == "cerrada"].copy()
    if not cerradas.empty and "fecha_cierre" in cerradas.columns:
        cerradas["fecha_apertura"] = pd.to_datetime(cerradas["fecha_apertura"])
        cerradas["fecha_cierre"] = pd.to_datetime(cerradas["fecha_cierre"])
        cerradas["horas_resolucion"] = (cerradas["fecha_cierre"] - cerradas["fecha_apertura"]).dt.total_seconds() / 3600
        tiempo_medio = round(cerradas["horas_resolucion"].mean(), 1)
        tiempo_medio_str = f"{tiempo_medio}h"
    else:
        tiempo_medio_str = "Sin datos"

    # Métricas
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("📋 Total", len(df))
    col2.metric("🔴 Abiertas", len(df[df["estado"] == "abierta"]))
    col3.metric("✅ Cerradas", len(df[df["estado"] == "cerrada"]))
    col4.metric("⚠️ Alta prioridad", len(df[df["prioridad"] == "alta"]))
    col5.metric("⏱ Tiempo medio resolución", tiempo_medio_str)

    st.markdown("---")

    # Filtros encadenados
    st.subheader("Filtros")
    col_f1, col_f2, col_f3 = st.columns(3)

    with col_f1:
        filtro_estado = st.selectbox("Estado", ["Todos"] + sorted(df["estado"].unique().tolist()))
    df_paso1 = df if filtro_estado == "Todos" else df[df["estado"] == filtro_estado]

    with col_f2:
        filtro_prioridad = st.selectbox("Prioridad", ["Todos"] + sorted(df_paso1["prioridad"].unique().tolist()))
    df_paso2 = df_paso1 if filtro_prioridad == "Todos" else df_paso1[df_paso1["prioridad"] == filtro_prioridad]

    with col_f3:
        filtro_tipo = st.selectbox("Tipo", ["Todos"] + sorted(df_paso2["tipo"].unique().tolist()))
    df_filtrado = df_paso2 if filtro_tipo == "Todos" else df_paso2[df_paso2["tipo"] == filtro_tipo]

    st.markdown("---")

    # Gráficas
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.subheader("Por prioridad")
        fig = px.bar(
            df_filtrado["prioridad"].value_counts().reset_index(),
            x="prioridad", y="count",
            color="prioridad",
            color_discrete_map={"alta": "#ef4444", "media": "#f97316", "baja": "#22c55e"},
            labels={"prioridad": "Prioridad", "count": "Cantidad"}
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_g2:
        st.subheader("Por tipo")
        fig2 = px.pie(
            df_filtrado,
            names="tipo",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # Tabla
    st.subheader(f"Incidencias ({len(df_filtrado)} resultados)")
    st.dataframe(df_filtrado, use_container_width=True)
