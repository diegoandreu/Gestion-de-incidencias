import sqlite3
from datetime import datetime

DB = "incidencias.db"

def conectar():
    return sqlite3.connect(DB)

def inicializar_db():
    with conectar() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS incidencias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                tipo TEXT NOT NULL,
                prioridad TEXT NOT NULL,
                estado TEXT NOT NULL DEFAULT 'abierta',
                responsable TEXT NOT NULL,
                fecha_apertura TEXT NOT NULL,
                descripcion TEXT
            )
        """)
        conn.commit()

def insertar_incidencia(titulo, tipo, prioridad, responsable, descripcion):
    with conectar() as conn:
        conn.execute("""
            INSERT INTO incidencias (titulo, tipo, prioridad, estado, responsable, fecha_apertura, descripcion)
            VALUES (?, ?, ?, 'abierta', ?, ?, ?)
        """, (titulo, tipo, prioridad, responsable, datetime.now().strftime("%Y-%m-%d %H:%M"), descripcion))
        conn.commit()

def obtener_incidencias():
    with conectar() as conn:
        cursor = conn.execute("SELECT * FROM incidencias ORDER BY id DESC")
        columnas = [col[0] for col in cursor.description]
        return [dict(zip(columnas, fila)) for fila in cursor.fetchall()]

def cerrar_incidencia(id):
    with conectar() as conn:
        conn.execute("UPDATE incidencias SET estado = 'cerrada' WHERE id = ?", (id,))
        conn.commit()

def obtener_incidencia_por_id(id):
    with conectar() as conn:
        cursor = conn.execute("SELECT * FROM incidencias WHERE id = ?", (id,))
        columnas = [col[0] for col in cursor.description]
        fila = cursor.fetchone()
        return dict(zip(columnas, fila)) if fila else None
