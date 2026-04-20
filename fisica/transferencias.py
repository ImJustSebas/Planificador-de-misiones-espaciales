"""
Calculo de transferencias orbitales interplanetarias.

Implementa la transferencia de Hohmann como caso base: es la maniobra
de dos impulsos que minimiza el delta-v total entre dos orbitas circulares
coplanares, segun la mecanica orbital clasica.
"""

import numpy as np

from fisica.orbita import (
    velocidad_circular,
    velocidad_en_punto_eliptico,
    semieje_mayor_elipse,
    periodo_orbital,
)
from config.configuracion import PLANETAS, SEGUNDOS_POR_DIA, MU_SOL


def calcular_transferencia_hohmann(radio_origen_m, radio_destino_m):
    """
    Calcula los parametros de una transferencia de Hohmann entre dos
    orbitas circulares alrededor del Sol.

    La maniobra consiste en dos impulsos:
      1. En la orbita de origen, para entrar a la elipse de transferencia.
      2. En la orbita de destino, para circularizar.

    Parametros
    ----------
    radio_origen_m  : float - Radio de la orbita de origen en metros
    radio_destino_m : float - Radio de la orbita de destino en metros

    Retorna
    -------
    dict con claves:
      'delta_v_1'        : primer impulso en m/s
      'delta_v_2'        : segundo impulso en m/s
      'delta_v_total'    : suma de magnitudes en m/s
      'tiempo_vuelo_s'   : duracion del viaje en segundos
      'tiempo_vuelo_dias': duracion del viaje en dias
      'semieje_mayor_m'  : semieje mayor de la elipse de transferencia en metros
    """
    if radio_origen_m <= 0 or radio_destino_m <= 0:
        raise ValueError("Los radios orbitales deben ser positivos.")

    if radio_origen_m == radio_destino_m:
        return {
            "delta_v_1":         0.0,
            "delta_v_2":         0.0,
            "delta_v_total":     0.0,
            "tiempo_vuelo_s":    0.0,
            "tiempo_vuelo_dias": 0.0,
            "semieje_mayor_m":   radio_origen_m,
        }

    v_origen  = velocidad_circular(radio_origen_m)
    v_destino = velocidad_circular(radio_destino_m)

    r_peri = min(radio_origen_m, radio_destino_m)
    r_afe  = max(radio_origen_m, radio_destino_m)
    a      = semieje_mayor_elipse(r_peri, r_afe)

    v_trans_peri = velocidad_en_punto_eliptico(r_peri, a)
    v_trans_afe  = velocidad_en_punto_eliptico(r_afe,  a)

    if radio_destino_m > radio_origen_m:
        # Viaje hacia una orbita exterior: se acelera dos veces
        dv1 = v_trans_peri - v_origen
        dv2 = v_destino    - v_trans_afe
    else:
        # Viaje hacia una orbita interior: se frena dos veces
        dv1 = v_origen     - v_trans_afe
        dv2 = v_trans_peri - v_destino

    tiempo_vuelo_s = periodo_orbital(a) / 2.0

    return {
        "delta_v_1":         dv1,
        "delta_v_2":         dv2,
        "delta_v_total":     abs(dv1) + abs(dv2),
        "tiempo_vuelo_s":    tiempo_vuelo_s,
        "tiempo_vuelo_dias": tiempo_vuelo_s / SEGUNDOS_POR_DIA,
        "semieje_mayor_m":   a,
    }


def calcular_angulo_fase_requerido(radio_origen_m, radio_destino_m):
    """
    Calcula el angulo de fase que debe tener el planeta destino por delante
    del planeta origen en el momento del lanzamiento.

    Esta es la condicion geometrica para que la nave llegue al punto correcto
    de la orbita de destino tras completar la semi-elipse de Hohmann.

    Retorna el angulo en radianes (puede ser negativo si el destino debe
    estar por detras del origen).
    """
    r_peri = min(radio_origen_m, radio_destino_m)
    r_afe  = max(radio_origen_m, radio_destino_m)
    a      = semieje_mayor_elipse(r_peri, r_afe)

    tiempo_vuelo      = periodo_orbital(a) / 2.0
    vel_ang_destino   = np.sqrt(MU_SOL / radio_destino_m**3)
    angulo_fase       = np.pi - vel_ang_destino * tiempo_vuelo

    return angulo_fase


def angulo_fase_actual(nombre_origen, nombre_destino, tiempo_dias):
    """
    Calcula el angulo de fase actual del planeta destino relativo al origen.

    Retorna el angulo en radianes, normalizado al rango [-pi, pi].
    Un valor positivo significa que el destino va por delante del origen.
    """
    from datos.efemerides_simuladas import obtener_angulo_orbital

    angulo_origen  = obtener_angulo_orbital(nombre_origen,  tiempo_dias)
    angulo_destino = obtener_angulo_orbital(nombre_destino, tiempo_dias)

    diferencia = (angulo_destino - angulo_origen) % (2 * np.pi)

    # Normalizar a [-pi, pi]
    if diferencia > np.pi:
        diferencia -= 2 * np.pi

    return diferencia
