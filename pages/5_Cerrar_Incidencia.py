#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 31 23:44:42 2026

@author: diegoandreu
"""

import streamlit as st
from database import inicializar_db, obtener_incidencias, cerrar_incidencia

inicializar_db()

st.title("🔒 Cerrar Incidencia")
st.markdown("---")

datos = obtener_incidencias()
abiertas = [i for i in datos if i["estado"] == "abierta"]

if not abiertas:
    st.info("No hay incidencias abiertas.")
else:
    opciones = {f"[{i['id']}] {i['titulo']} — {i['prioridad']}": i['id'] for i in abiertas}
    seleccion = st.selectbox("Selecciona la incidencia a cerrar", list(opciones.keys()))

    if st.button("Cerrar incidencia"):
        cerrar_incidencia(opciones[seleccion])
        st.success("✅ Incidencia cerrada correctamente.")
        st.rerun()