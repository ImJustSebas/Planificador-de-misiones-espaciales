# Planificador de Misiones Espaciales

Sistema desarrollado en Python para simular y optimizar trayectorias orbitales entre planetas, con enfoque en eficiencia energética (delta-v) y análisis de ventanas de lanzamiento.

Este proyecto busca modelar, de forma simplificada pero estructurada, uno de los problemas fundamentales en la ingeniería aeroespacial: la planificación de transferencias orbitales entre cuerpos celestes.

---

## Descripción

El sistema permite calcular trayectorias de transferencia entre planetas utilizando modelos físicos simplificados, además de optimizar el momento de lanzamiento para reducir el consumo de combustible.

Incluye simulación orbital, cálculo de transferencias tipo Hohmann, optimización numérica y visualización de resultados.

El diseño es modular y está pensado para poder adaptarse fácilmente a datos reales (efemérides) en el futuro.

---

## Características principales

- Simulación de órbitas planetarias en 2D
- Cálculo de transferencias orbitales tipo Hohmann
- Estimación de delta-v total
- Optimización de ventanas de lanzamiento
- Visualización de órbitas y trayectorias
- Interfaz gráfica simple con Tkinter
- Ejecución desde consola (CLI)
- Arquitectura modular y extensible

---

## Estructura del proyecto


mission_planner/
├── main.py
├── requirements.txt
├── config/
│ └── configuracion.py
├── datos/
│ ├── generador_datos.py
│ └── efemerides_simuladas.py
├── fisica/
│ ├── orbita.py
│ └── transferencias.py
├── optimizacion/
│ └── buscador_ruta.py
├── visualizacion/
│ └── graficos.py
├── interfaz/
│ └── ventana_principal.py
└── utilidades/
└── auxiliares.py


---

## Instalación

Clonar el repositorio:


git clone https://github.com/ImJustSebas/Planificador-de-misiones-espaciales.git

cd Planificador-de-misiones-espaciales


Crear entorno virtual (opcional pero recomendado):


python -m venv entorno
source entorno/bin/activate # Linux / macOS
entorno\Scripts\activate # Windows


Instalar dependencias:


pip install -r requirements.txt


---

## Uso

### Interfaz gráfica


python main.py


Permite:
- Seleccionar planeta origen
- Seleccionar planeta destino
- Ejecutar simulación
- Visualizar resultados

---

### Modo consola


python main.py --modo cli --origen tierra --destino marte


Salida esperada:
- Delta-v estimado
- Tiempo de vuelo
- Mejor ventana de lanzamiento
- Gráfica de la trayectoria

---

## Conceptos implementados

Este proyecto incluye conceptos reales de mecánica orbital:

- Órbitas circulares simplificadas
- Transferencias de Hohmann
- Parámetro gravitacional
- Optimización numérica de trayectorias
- Simulación de posiciones planetarias

---

## Tecnologías utilizadas

- Python
- NumPy
- SciPy
- Matplotlib
- Tkinter

---

## Posibles mejoras

- Uso de efemérides reales (JPL / NASA)
- Implementación del problema de Lambert
- Órbitas elípticas en lugar de circulares
- Simulación en 3D
- Interfaz web (FastAPI + frontend)
- Soporte para múltiples transferencias (asistencias gravitacionales)
- Sistema en tiempo real con datos externos

---

## Objetivo del proyecto

El objetivo principal es demostrar la capacidad de:

- Aplicar matemáticas y física a problemas reales
- Diseñar sistemas modulares y escalables
- Implementar optimización numérica
- Desarrollar software técnico con enfoque científico

---

## Estado del proyecto

En desarrollo. La versión actual utiliza modelos simplificados, pero la arquitectura está preparada para evolucionar hacia simulaciones más realistas.

---

## Autor

Sebastian porras solano

Repositorio:
https://github.com/ImJustSebas/Planificador-de-misiones-espaciales
