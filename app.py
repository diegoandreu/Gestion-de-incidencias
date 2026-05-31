import streamlit as st
import pandas as pd
from database import inicializar_db, insertar_incidencia, obtener_incidencias, cerrar_incidencia, obtener_incidencia_por_id

st.set_page_config(page_title="Gestor de Incidencias", page_icon="🔧", layout="wide")

inicializar_db()

# --- NAVEGACIÓN ---
seccion = st.sidebar.selectbox("Menú principal", ["📋 Dashboard", "🗂 Incidencias"])

# --- NAVEGACIÓN ---
st.sidebar.title("🔧 Gestor de Incidencias")
st.sidebar.markdown("---")

st.sidebar.markdown("### 📊 General")
if st.sidebar.button("📋 Dashboard", use_container_width=True):
    st.session_state["menu"] = "📋 Dashboard"

st.sidebar.markdown("---")
st.sidebar.markdown("### 🗂 Incidencias")
if st.sidebar.button("🔍 Consultar", use_container_width=True):
    st.session_state["menu"] = "🔍 Consultar"
if st.sidebar.button("➕ Nueva Incidencia", use_container_width=True):
    st.session_state["menu"] = "➕ Nueva Incidencia"
if st.sidebar.button("🔒 Cerrar Incidencia", use_container_width=True):
    st.session_state["menu"] = "🔒 Cerrar Incidencia"

if "menu" not in st.session_state:
    st.session_state["menu"] = "📋 Dashboard"

menu = st.session_state["menu"]

# ==========================================
# DASHBOARD
# ==========================================
if menu == "📋 Dashboard":
    st.title("🔧 Panel de Gestión de Incidencias")
    st.markdown("---")

    datos = obtener_incidencias()

    if not datos:
        st.info("No hay incidencias registradas todavía.")
    else:
        df = pd.DataFrame(datos)

        # Métricas
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("📋 Total", len(df))
        col2.metric("🔴 Abiertas", len(df[df["estado"] == "abierta"]))
        col3.metric("✅ Cerradas", len(df[df["estado"] == "cerrada"]))
        col4.metric("⚠️ Alta prioridad", len(df[df["prioridad"] == "alta"]))

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
            st.bar_chart(df_filtrado["prioridad"].value_counts())
        with col_g2:
            st.subheader("Por tipo")
            st.bar_chart(df_filtrado["tipo"].value_counts())

        st.markdown("---")

        # Tabla
        st.subheader(f"Incidencias ({len(df_filtrado)} resultados)")
        st.dataframe(df_filtrado, use_container_width=True)

# ==========================================
# CONSULTAR INCIDENCIAS
# ==========================================
elif menu == "🔍 Consultar":
    st.title("🔍 Consultar Incidencias")
    st.markdown("---")

    datos = obtener_incidencias()

    if not datos:
        st.info("No hay incidencias registradas todavía.")
    else:
        df = pd.DataFrame(datos)

        filtro_estado = st.selectbox("Filtrar por estado", ["Todos", "abierta", "cerrada"])
        df_filtrado = df if filtro_estado == "Todos" else df[df["estado"] == filtro_estado]

        st.dataframe(df_filtrado, use_container_width=True)

# ==========================================
# NUEVA INCIDENCIA
# ==========================================
elif menu == "➕ Nueva Incidencia":
    st.title("➕ Registrar Nueva Incidencia")
    st.markdown("---")

    if st.session_state.get("incidencia_registrada"):
        st.success("✅ Incidencia registrada correctamente.")
        st.session_state["incidencia_registrada"] = False

    with st.form("formulario_incidencia", clear_on_submit=True):
        titulo = st.text_input("Título breve")
        tipo = st.selectbox("Tipo", ["hardware", "red", "software", "otro"])
        prioridad = st.selectbox("Prioridad", ["alta", "media", "baja"])
        responsable = st.text_input("Responsable")
        descripcion = st.text_area("Descripción")
        enviado = st.form_submit_button("Registrar incidencia")

    if enviado:
        if titulo and responsable:
            insertar_incidencia(titulo, tipo, prioridad, responsable, descripcion)
            st.session_state["incidencia_registrada"] = True
            st.rerun()
        else:
            st.error("❌ El título y el responsable son obligatorios.")

# ==========================================
# CERRAR INCIDENCIA
# ==========================================
elif menu == "🔒 Cerrar Incidencia":
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