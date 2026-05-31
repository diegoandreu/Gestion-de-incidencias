#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 31 14:31:23 2026

@author: diegoandreu
"""

import csv
import os
from datetime import datetime

ARCHIVO = "incidencias.csv"
CAMPOS = ["id", "titulo", "tipo", "prioridad", "estado", "responsable", "fecha_apertura", "descripcion"]

def inicializar_archivo():
    if not os.path.exists(ARCHIVO):
        with open(ARCHIVO, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(CAMPOS)

def obtener_siguiente_id():
    with open(ARCHIVO, "r", encoding="utf-8") as f:
        filas = list(csv.reader(f))
    return len(filas)  # encabezado cuenta como fila 1, así ID empieza en 1

def registrar_incidencia():
    print("\n--- NUEVA INCIDENCIA ---")
    titulo = input("Título breve: ")
    tipo = input("Tipo (hardware/red/software/otro): ")
    prioridad = input("Prioridad (alta/media/baja): ")
    responsable = input("Responsable: ")
    descripcion = input("Descripción: ")

    nueva = [
        obtener_siguiente_id(),
        titulo,
        tipo,
        prioridad,
        "abierta",
        responsable,
        datetime.now().strftime("%Y-%m-%d %H:%M"),
        descripcion
    ]

    with open(ARCHIVO, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(nueva)

    print(f"\nIncidencia #{nueva[0]} registrada correctamente.")

inicializar_archivo()
registrar_incidencia()

