#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 31 23:44:12 2026

@author: diegoandreu
"""

import streamlit as st
from database import inicializar_db, insertar_incidencia

inicializar_db()

st.title("➕ Registrar Nueva Incidencia")
st.markdown("---")

if st.session_state.get("incidencia_registrada"):
    st.success("✅ Incidencia registrada correctamente.")
    st.session_state["incidencia_registrada"] = False

with st.form("formulario_incidencia", clear_on_submit=True):
    titulo = st.text_input("Título breve")
    tipo = st.selectbox("Tipo", ["hardware", "red", "software", "otro"])
    prioridad = st.selectbox("Prioridad", ["alta", "media", "baja"])
    respons