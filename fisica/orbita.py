"""
Funciones de mecanica orbital basica.

Cubre posiciones en orbitas circulares y elipticas, velocidades orbitales
y calculos geometricos derivados de las leyes de Kepler.
"""

import numpy as np
from config.configuracion import MU_SOL


def velocidad_circular(radio_m):
    """
    Calcula la velocidad circular en una orbita de radio dado alrededor del Sol.

    v = sqrt(mu / r)

    Parametros
    ----------
    radio_m : float - Radio orbital en metros

    Retorna
    -------
    float - Velocidad en m/s
    """
    if radio_m <= 0:
        raise ValueError("El radio orbital debe ser positivo.")
    return np.sqrt(MU_SOL / radio_m)


def periodo_orbital(radio_m):
    """
    Calcula el periodo orbital kepleriano para una orbita circular.

    T = 2 * pi * sqrt(r^3 / mu)

    Parametros
    ----------
    radio_m : float - Radio orbital en metros

    Retorna
    -------
    float - Periodo en segundos
    """
    if radio_m <= 0:
        raise ValueError("El radio orbital debe ser positivo.")
    return 2 * np.pi * np.sqrt(radio_m**3 / MU_SOL)


def posicion_circular_2d(radio_m, angulo_rad):
    """
    Devuelve la posicion (x, y) en una orbita circular dado un angulo.

    Parametros
    ----------
    radio_m    : float - Radio de la orbita en metros
    angulo_rad : float - Angulo en radianes desde el eje x positivo

    Retorna
    -------
    tuple (x, y) en metros
    """
    return (radio_m * np.cos(angulo_rad), radio_m * np.sin(angulo_rad))


def puntos_orbita_circular(radio_m, n_puntos=300):
    """
    Genera arrays de puntos (x, y) que describen una orbita circular completa.
    Util para graficar.

    Retorna
    -------
    tuple (array_x, array_y) en metros
    """
    angulos = np.linspace(0, 2 * np.pi, n_puntos)
    return (radio_m * np.cos(angulos), radio_m * np.sin(angulos))


def semieje_mayor_elipse(radio_perihelio, radio_afelio):
    """
    Calcula el semieje mayor de una elipse dadas las distancias extremas al foco.

    a = (r_perihelio + r_afelio) / 2
    """
    return (radio_perihelio + radio_afelio) / 2.0


def velocidad_en_punto_eliptico(radio_m, semieje_mayor_m):
    """
    Velocidad en un punto de una orbita eliptica usando la ecuacion vis-viva.

    v^2 = mu * (2/r - 1/a)

    Parametros
    ----------
    radio_m         : float - Distancia actual al foco (Sol) en metros
    semieje_mayor_m : float - Semieje mayor de la elipse en metros

    Retorna
    -------
    float - Velocidad en m/s
    """
    v_cuadrado = MU_SOL * (2.0 / radio_m - 1.0 / semieje_mayor_m)
    if v_cuadrado < 0:
        raise ValueError("Configuracion orbital invalida: v^2 negativo (check radios y semieje).")
    return np.sqrt(v_cuadrado)


def puntos_orbita_transferencia(radio_origen_m, radio_destino_m, n_puntos=150):
    """
    Genera los puntos de la semi-elipse de transferencia de Hohmann entre
    dos orbitas circulares.

    El perihelio de la elipse coincide con la orbita de origen y el afelio
    con la de destino (o viceversa si el viaje es hacia adentro).

    Retorna
    -------
    tuple (array_x, array_y) en metros
    """
    a = semieje_mayor_elipse(
        min(radio_origen_m, radio_destino_m),
        max(radio_origen_m, radio_destino_m)
    )
    # Distancia focal: c = a - r_perihelio
    c = a - min(radio_origen_m, radio_destino_m)

    angulos  = np.linspace(0, np.pi, n_puntos)
    x_elipse = a * np.cos(angulos)
    y_elipse = np.sqrt(a**2 - c**2) * np.sin(angulos)

    # Desplazamos para que el Sol quede en el foco
    x = x_elipse - c
    y = y_elipse

    # Si el destino es exterior, reflejamos para que el perihelio este a la derecha
    if radio_destino_m > radio_origen_m:
        x = -x

    return (x, y)
