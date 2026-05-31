# Sistema de Gestión de Incidencias Técnicas

## ¿Qué es esto?
Herramienta desarrollada para registrar, gestionar y visualizar incidencias técnicas de hardware y equipos en entornos reales de soporte e implantación.

Surge de una necesidad real: en mi trabajo diario como técnico de telecomunicaciones, las incidencias se gestionan por email y llamadas sin un sistema centralizado. Este proyecto es una primera solución funcional a ese problema.

## ¿Qué hace?
- Registrar incidencias con título, tipo, prioridad, responsable y descripción
- Consultar el listado de incidencias activas y cerradas
- Cerrar incidencias y actualizar su estado
- Visualizar métricas en un dashboard web interactivo

## Dashboard
El panel de visualización muestra:
- Total de incidencias, abiertas y cerradas
- Distribución por prioridad
- Distribución por tipo
- Listado completo filtrable

## Tecnologías usadas
- Python 3
- CSV (almacenamiento de datos)
- Streamlit (dashboard web)
- Pandas (tratamiento de datos)
- GitHub (control de versiones)

## Cómo ejecutarlo

### Gestor de incidencias
```bash
python app.py
```

### Dashboard
```bash
streamlit run dashboard.py
```

## Próximos pasos
- Migración de CSV a base de datos SQLite
- Filtros avanzados en el dashboard
- Sistema de alertas por prioridad
- Exportación de informes

## Autor
Diego Andreu — Ingeniero de Telecomunicaciones
https://www.linkedin.com/in/diego-andreu-cantador-001102385
