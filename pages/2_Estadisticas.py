#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 31 23:42:20 2026

@author: diegoandreu
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from database import inicializar_db, obtener_incidencias

inicializar_db()

st.title("📈 Estadísticas")
st.markdown("---")

datos = obtener_incidencias()

if not datos:
    st.info("No hay datos suficientes para mostrar estadísticas.")
else:
    df = pd.DataFrame(datos)
    df["fecha_apertura"] = pd.to_datetime(df["fecha_apertura"])

    cerradas = df[df["estado"] == "cerrada"].copy()
    if not cerradas.empty and "fecha_cierre" in cerradas.columns:
        cerradas["fecha_cierre"] = pd.to_datetime(cerradas["fecha_cierre"])
        cerradas["horas_resolucion"] = (cerradas["fecha_cierre"] - cerradas["fecha_apertura"]).dt.total_seconds() / 3600
        tiempo_medio = round(cerradas["horas_resolucion"].mean(), 1)
        max_resolucion = round(cerradas["horas_resolucion"].max(), 1)
        min_resolucion = round(cerradas["horas_resolucion"].min(), 1)
    else:
        tiempo_medio = max_resolucion = min_resolucion = None

    pct_resueltas = round(len(cerradas) / len(df) * 100, 1) if len(df) > 0 else 0
    abiertas_mas_24h = df[
        (df["estado"] == "abierta") &
        ((pd.Timestamp.now() - df["fecha_apertura"]).dt.total_seconds() / 3600 > 24)
    ]

    # KPIs
    st.subheader("KPIs principales")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("⏱ Tiempo medio resolución", f"{tiempo_medio}h" if tiempo_medio else "Sin datos")
    col2.metric("✅ % Incidencias resueltas", f"{pct_resueltas}%")
    col3.metric("🐢 Resolución más lenta", f"{max_resolucion}h" if max_resolucion else "Sin datos")
    col4.metric("⚡ Resolución más rápida", f"{min_resolucion}h" if min_resolucion else "Sin datos")

    if len(abiertas_mas_24h) > 0:
        st.warning(f"⚠️ {len(abiertas_mas_24h)} incidencia(s) llevan más de 24h abiertas sin resolver.")

    st.markdown("---")

    # Evolución temporal
    st.subheader("Evolución de incidencias por día")
    df["dia"] = df["fecha_apertura"].dt.date
    por_dia = df.groupby("dia").size().reset_index(name="incidencias")
    fig_linea = px.line(
        por_dia, x="dia", y="incidencias",
        markers=True,
        labels={"dia": "Fecha", "incidencias": "Incidencias registradas"}
    )
    st.plotly_chart(fig_linea, use_container_width=True)

    st.markdown("---")

    # Distribución por tipo y prioridad
    col_g1, col_g2 = st.columns(2)

    with col_g1:
        st.subheader("Distribución por tipo")
        fig_tipo = px.bar(
            df["tipo"].value_counts().reset_index(),
            x="tipo", y="count",
            color="tipo",
            labels={"tipo": "Tipo", "count": "Cantidad"}
        )
        st.plotly_chart(fig_tipo, use_container_width=True)

    with col_g2:
        st.subheader("Distribución por prioridad")
        fig_prior = px.pie(
            df, names="prioridad",
            color="prioridad",
            color_discrete_map={"alta": "#ef4444", "media": "#f97316", "baja": "#22c55e"}
        )
        st.plotly_chart(fig_prior, use_container_width=True)

    st.markdown("---")

    # Tiempo de resolución por tipo
    if not cerradas.empty:
        st.subheader("Tiempo medio de resolución por tipo (horas)")
        tiempo_por_tipo = cerradas.groupby("tipo")["horas_resolucion"].mean().round(1).reset_index()
        tiempo_por_tipo.columns = ["tipo", "horas_media"]
        fig_tiempo = px.bar(
            tiempo_por_tipo, x="tipo", y="horas_media",
            color="tipo",
            labels={"tipo": "Tipo", "horas_media": "Horas media"}
        )
        st.plotly_chart(fig_tiempo, use_container_width=True)