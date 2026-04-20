"""
Generador de datos simulados para pruebas del sistema.

Produce series temporales de posiciones orbitales en 2D para uno o mas planetas,
con soporte para semilla determinista. Util para validar la logica sin depender
de efemerides reales.
"""

import numpy as np
from config.configuracion import PLANETAS, SEGUNDOS_POR_DIA


def generar_serie_posiciones(nombre_planeta, t_inicio_dias, t_fin_dias, n_puntos=200, semilla=None):
    """
    Genera una serie de posiciones (x, y) en metros para un planeta dado,
    asumiendo orbita circular en el plano ecliptico.

    Parametros
    ----------
    nombre_planeta  : str   - Clave del planeta en PLANETAS
    t_inicio_dias   : float - Tiempo inicial en dias
    t_fin_dias      : float - Tiempo final en dias
    n_puntos        : int   - Numero de puntos en la serie
    semilla         : int   - Semilla opcional para reproducibilidad

    Retorna
    -------
    dict con claves 'tiempos_dias', 'x', 'y' (todos arrays numpy)
    """
    if nombre_planeta not in PLANETAS:
        raise ValueError(f"Planeta '{nombre_planeta}' no reconocido.")

    if semilla is not None:
        np.random.seed(semilla)

    datos   = PLANETAS[nombre_planeta]
    radio   = datos["radio_orbital"]
    periodo = datos["periodo_orbital"]

    tiempos_dias = np.linspace(t_inicio_dias, t_fin_dias, n_puntos)
    tiempos_s    = tiempos_dias * SEGUNDOS_POR_DIA
    angulo       = 2 * np.pi * tiempos_s / periodo

    return {
        "tiempos_dias": tiempos_dias,
        "x":            radio * np.cos(angulo),
        "y":            radio * np.sin(angulo),
    }


def generar_datos_multiples(nombres_planetas, t_inicio_dias=0, t_fin_dias=730, n_puntos=300):
    """
    Genera series de posicion para una lista de planetas de forma simultanea.

    Retorna un diccionario indexado por nombre de planeta, donde cada valor
    es el dict producido por generar_serie_posiciones.
    """
    return {
        nombre: generar_serie_posiciones(nombre, t_inicio_dias, t_fin_dias, n_puntos)
        for nombre in nombres_planetas
    }
