#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 31 14:40:40 2026

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
    return len(filas)

def registrar_incidencia():
    print("\n--- NUEVA INCIDENCIA ---")
    titulo = input("Título breve: ")
    tipo = input("Tipo (hardware/red/software/otro): ")
    prioridad = input("Prioridad (alta/media/baja): ")
    responsable = input("Responsable: ")
    descripcion = input("Descripción: ")

    nueva = [
        obtener_siguiente_id(),
        titulo, tipo, prioridad,
        "abierta", responsable,
        datetime.now().strftime("%Y-%m-%d %H:%M"),
        descripcion
    ]

    with open(ARCHIVO, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(nueva)

    print(f"\nIncidencia #{nueva[0]} registrada correctamente.")

def listar_incidencias():
    print("\n--- INCIDENCIAS REGISTRADAS ---")
    with open(ARCHIVO, "r", encoding="utf-8") as f:
        filas = list(csv.DictReader(f))

    if not filas:
        print("No hay incidencias registradas.")
        return

    for fila in filas:
        print(f"[{fila['id']}] {fila['titulo']} | {fila['tipo']} | {fila['prioridad']} | {fila['estado']} | {fila['responsable']}")

def cerrar_incidencia():
    listar_incidencias()
    id_cerrar = input("\nID de la incidencia a cerrar: ")

    filas = []
    with open(ARCHIVO, "r", encoding="utf-8") as f:
        filas = list(csv.DictReader(f))

    encontrada = False
    for fila in filas:
        if fila["id"] == id_cerrar:
            fila["estado"] = "cerrada"
            encontrada = True

    if not encontrada:
        print("ID no encontrado.")
        return

    with open(ARCHIVO, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CAMPOS)
        writer.writeheader()
        writer.writerows(filas)

    print(f"Incidencia #{id_cerrar} cerrada.")

def menu():
    inicializar_archivo()
    while True:
        print("\n=== GESTOR DE INCIDENCIAS ===")
        print("1. Registrar incidencia")
        print("2. Ver incidencias")
        print("3. Cerrar incidencia")
        print("4. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            registrar_incidencia()
        elif opcion == "2":
            listar_incidencias()
        elif opcion == "3":
            cerrar_incidencia()
        elif opcion == "4":
            print("Saliendo...")
            break
        else:
            print("Opción no válida.")

menu()