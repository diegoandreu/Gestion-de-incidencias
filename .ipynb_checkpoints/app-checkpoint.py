import streamlit as st
from database import inicializar_db

st.set_page_config(page_title="Gestor de Incidencias", page_icon="🔧", layout="wide")

inicializar_db()

st.title("🔧 Gestor de Incidencias Técnicas")
st.markdown("---")
st.markdown("""
Bienvenido al sistema de gestión de incidencias técnicas.

Usa el menú lateral para navegar entre las secciones:

- 📋 **Dashboard** — visión general y métricas
- 📈 **Estadísticas** — KPIs y análisis detallado
- 🔍 **Consultar** — listado y filtrado de incidencias
- ➕ **Nueva Incidencia** — registrar una nueva
- 🔒 **Cerrar Incidencia** — cerrar incidencias abiertas
""")