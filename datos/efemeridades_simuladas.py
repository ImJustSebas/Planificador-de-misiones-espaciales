"""
Efemerides simplificadas basadas en orbitas circulares kepleranas.

Este modulo actua como capa de abstraccion: puede reemplazarse en el futuro
por un proveedor de datos reales (JPL Horizons, SPICE, etc.) sin necesidad
de modificar el resto del codigo, siempre que se respeten las mismas firmas.
"""

import numpy as np
from config.configuracion import PLANETAS, SEGUNDOS_POR_DIA


def obtener_posicion_planeta(nombre_planeta, tiempo_dias):
    """
    Devuelve la posicion (x, y) de un planeta en metros en el plano ecliptico,
    calculada mediante orbita circular con el periodo kepleriano del planeta.

    Parametros
    ----------
    nombre_planeta : str   - Nombre del planeta (clave en PLANETAS)
    tiempo_dias    : float - Tiempo desde la epoca de referencia en dias

    Retorna
    -------
    tuple (x, y) en metros
    """
    if nombre_planeta not in PLANETAS:
        raise ValueError(f"Planeta '{nombre_planeta}' no encontrado en la configuracion.")

    datos    = PLANETAS[nombre_planeta]
    radio    = datos["radio_orbital"]
    periodo  = datos["periodo_orbital"]
    tiempo_s = tiempo_dias * SEGUNDOS_POR_DIA
    angulo   = 2 * np.pi * tiempo_s / periodo

    return (radio * np.cos(angulo), radio * np.sin(angulo))


def obtener_velocidad_orbital(nombre_planeta):
    """
    Devuelve la velocidad orbital circular de un planeta en m/s.

    Se calcula como v = 2 * pi * r / T, que es la velocidad tangencial
    en la orbita circular aproximada.
    """
    if nombre_planeta not in PLANETAS:
        raise ValueError(f"Planeta '{nombre_planeta}' no encontrado.")

    datos = PLANETAS[nombre_planeta]
    return 2 * np.pi * datos["radio_orbital"] / datos["periodo_orbital"]


def obtener_angulo_orbital(nombre_planeta, tiempo_dias):
    """
    Retorna el angulo orbital en radianes de un planeta en un tiempo dado,
    normalizado al rango [0, 2*pi].

    Util para calcular la geometria relativa entre planetas sin necesidad
    de sus posiciones cartesianas completas.
    """
    datos    = PLANETAS[nombre_planeta]
    periodo  = datos["periodo_orbital"]
    tiempo_s = tiempo_dias * SEGUNDOS_POR_DIA

    return (2 * np.pi * tiempo_s / periodo) % (2 * np.pi)
