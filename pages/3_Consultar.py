#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 31 23:43:29 2026

@author: diegoandreu
"""

import streamlit as st
import pandas as pd
from database import inicializar_db, obtener_incidencias

inicializar_db()

st.title("🔍 Consultar Incidencias")
st.markdown("---")

datos = obtener_incidencias()

if not datos:
    st.info("No hay incidencias registradas todavía.")
else:
    df = pd.DataFrame(datos)

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

    st.subheader(f"Resultados ({len(df_filtrado)} incidencias)")
    st.dataframe(df_filtrado, use_container_width=True)