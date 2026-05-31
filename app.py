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

def pedir_opcion(mensaje, opciones):
    opciones_lower = [o.lower() for o in opciones]
    while True:
        valor = input(f"{mensaje} ({'/'.join(opciones)}): ").strip().lower()
        if valor in opciones_lower:
            return valor
        print(f"  ❌ Opción no válida. Por favor elige entre: {', '.join(opciones)}\n")

def registrar_incidencia():
    print("\n--- NUEVA INCIDENCIA ---")
    titulo = input("Título breve: ").strip()
    tipo = pedir_opcion("Tipo", ["hardware", "red", "software", "otro"])
    prioridad = pedir_opcion("Prioridad", ["alta", "media", "baja"])
    responsable = input("Responsable: ").strip()
    descripcion = input("Descripción: ").strip()

    nueva = [
        obtener_siguiente_id(),
        titulo, tipo, prioridad,
        "abierta", responsable,
        datetime.now().strftime("%Y-%m-%d %H:%M"),
        descripcion
    ]

    with open(ARCHIVO, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(nueva)

    print(f"\n✅ Incidencia #{nueva[0]} registrada correctamente.")

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
    id_cerrar = input("\nID de la incidencia a cerrar: ").strip()

    filas = []
    with open(ARCHIVO, "r", encoding="utf-8") as f:
        filas = list(csv.DictReader(f))

    encontrada = False
    for fila in filas:
        if fila["id"] == id_cerrar:
            if fila["estado"] == "cerrada":
                print("⚠️ Esta incidencia ya está cerrada.")
                return
            fila["estado"] = "cerrada"
            encontrada = True

    if not encontrada:
        print("❌ ID no encontrado.")
        return

    with open(ARCHIVO, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CAMPOS)
        writer.writeheader()
        writer.writerows(filas)

    print(f"✅ Incidencia #{id_cerrar} cerrada correctamente.")

def menu():
    inicializar_archivo()
    while True:
        print("\n=== GESTOR DE INCIDENCIAS ===")
        print("1. Registrar incidencia")
        print("2. Ver incidencias")
        print("3. Cerrar incidencia")
        print("4. Salir")
        opcion = input("Selecciona una opción: ").strip()

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
            print("❌ Opción no válida. Elige entre 1 y 4.")

menu()

