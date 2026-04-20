"""
Funciones de apoyo reutilizables en todo el proyecto.

Incluye formateo de unidades, conversiones y validaciones basicas.
"""

from config.configuracion import PLANETAS, SEGUNDOS_POR_DIA, UA


def formatear_delta_v(delta_v_ms):
    """
    Convierte un delta-v en m/s a km/s y lo devuelve como cadena.

    Ejemplo: 2940.0 -> "2.940 km/s"
    """
    return f"{delta_v_ms / 1000.0:.3f} km/s"


def formatear_tiempo(segundos):
    """
    Convierte un tiempo en segundos a una representacion legible en dias y horas.

    Ejemplo: 22291200 -> "258 dias, 4 h"
    """
    dias  = int(segundos // SEGUNDOS_POR_DIA)
    horas = int((segundos % SEGUNDOS_POR_DIA) // 3600)
    return f"{dias} dias, {horas} h"


def formatear_dias(dias_float):
    """
    Devuelve un numero de dias formateado con un decimal.

    Ejemplo: 258.7 -> "258.7 dias"
    """
    return f"{dias_float:.1f} dias"


def validar_par_planetas(nombre_origen, nombre_destino):
    """
    Verifica que ambos planetas existan en la configuracion y sean distintos.

    Lanza ValueError con un mensaje claro si alguna condicion falla.
    """
    if nombre_origen not in PLANETAS:
        raise ValueError(f"Planeta de origen no reconocido: '{nombre_origen}'")
    if nombre_destino not in PLANETAS:
        raise ValueError(f"Planeta de destino no reconocido: '{nombre_destino}'")
    if nombre_origen == nombre_destino:
        raise ValueError("El origen y el destino no pueden ser el mismo planeta.")


def metros_a_ua(metros):
    """Convierte metros a Unidades Astronomicas."""
    return metros / UA


def ua_a_metros(ua):
    """Convierte Unidades Astronomicas a metros."""
    return ua * UA


def ms_a_kms(velocidad_ms):
    """Convierte m/s a km/s."""
    return velocidad_ms / 1000.0


def segundos_a_dias(segundos):
    """Convierte segundos a dias."""
    return segundos / SEGUNDOS_POR_DIA


def dias_a_segundos(dias):
    """Convierte dias a segundos."""
    return dias * SEGUNDOS_POR_DIA
