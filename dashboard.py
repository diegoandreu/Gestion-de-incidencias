#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 31 14:49:44 2026

@author: diegoandreu
"""

import streamlit as st
import pandas as pd

ARCHIVO = "incidencias.csv"

df = pd.read_csv(ARCHIVO)

st.title("Panel de Incidencias")

# Métricas principales
col1, col2, col3 = st.columns(3)
col1.metric("Total incidencias", len(df))
col2.metric("Abiertas", len(df[df["estado"] == "abierta"]))
col3.metric("Cerradas", len(df[df["estado"] == "cerrada"]))

# Gráfica por prioridad
st.subheader("Incidencias por prioridad")
st.bar_chart(df["prioridad"].value_counts())

# Gráfica por tipo
st.subheader("Incidencias por tipo")
st.bar_chart(df["tipo"].value_counts())

# Tabla completa
st.subheader("Listado completo")
st.dataframe(df)