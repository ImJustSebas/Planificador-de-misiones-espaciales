"""
Busqueda de la ventana optima de lanzamiento entre dos planetas.

La estrategia consiste en evaluar el desfase angular entre los planetas
a lo largo del tiempo y minimizar la diferencia con el angulo de fase
ideal para una transferencia de Hohmann.

Se usa muestreo grueso para localizar el minimo global aproximado,
seguido de una minimizacion local precisa con scipy.optimize.
"""

import numpy as np
from scipy.optimize import minimize_scalar

from config.configuracion import PLANETAS
from fisica.transferencias import (
    calcular_transferencia_hohmann,
    calcular_angulo_fase_requerido,
    angulo_fase_actual,
)


def funcion_costo_ventana(tiempo_dias, nombre_origen, nombre_destino):
    """
    Funcion de costo para la busqueda de ventana de lanzamiento.

    Evalua cuanto se aleja el angulo de fase actual del angulo ideal.
    Un valor cercano a cero indica una buena ventana.

    Parametros
    ----------
    tiempo_dias    : float - Tiempo de salida en dias desde la epoca de referencia
    nombre_origen  : str
    nombre_destino : str

    Retorna
    -------
    float - Diferencia cuadratica entre angulo actual e ideal (radianes^2)
    """
    radio_origen  = PLANETAS[nombre_origen]["radio_orbital"]
    radio_destino = PLANETAS[nombre_destino]["radio_orbital"]

    angulo_ideal  = calcular_angulo_fase_requerido(radio_origen, radio_destino)
    angulo_actual = angulo_fase_actual(nombre_origen, nombre_destino, tiempo_dias)

    diferencia = (angulo_actual - angulo_ideal + np.pi) % (2 * np.pi) - np.pi

    return diferencia ** 2


def buscar_ventana_optima(nombre_origen, nombre_destino, t_inicio=0, t_fin=730, n_semillas=12):
    """
    Busca la ventana de lanzamiento optima en el intervalo [t_inicio, t_fin] dias.

    Parametros
    ----------
    nombre_origen  : str   - Planeta de origen
    nombre_destino : str   - Planeta de destino
    t_inicio       : float - Inicio del intervalo de busqueda en dias
    t_fin          : float - Fin del intervalo de busqueda en dias
    n_semillas     : int   - Numero de puntos de muestreo inicial

    Retorna
    -------
    dict con claves:
      'tiempo_optimo'      : tiempo de lanzamiento optimo en dias
      'delta_v_optimo'     : delta-v de la transferencia de Hohmann en m/s
      'angulo_fase_ideal'  : angulo de fase requerido en radianes
      'angulo_fase_real'   : angulo de fase en el tiempo optimo en radianes
      'costo_minimo'       : valor de la funcion de costo en el optimo
      'tiempo_vuelo_dias'  : duracion del viaje en dias
      'alternativas'       : lista de otras ventanas encontradas (hasta 3)
    """
    if nombre_origen not in PLANETAS or nombre_destino not in PLANETAS:
        raise ValueError("Nombres de planetas no validos.")

    radio_origen  = PLANETAS[nombre_origen]["radio_orbital"]
    radio_destino = PLANETAS[nombre_destino]["radio_orbital"]

    # Muestreo inicial sobre todo el rango
    tiempos_muestra = np.linspace(t_inicio, t_fin, 500)
    costos_muestra  = np.array([
        funcion_costo_ventana(t, nombre_origen, nombre_destino)
        for t in tiempos_muestra
    ])

    # Los n_semillas mejores puntos de arranque
    indices_ordenados = np.argsort(costos_muestra)
    semillas          = tiempos_muestra[indices_ordenados[:n_semillas]]

    mejores = []
    margen  = (t_fin - t_inicio) / 20.0

    for semilla in semillas:
        lim_inf = max(t_inicio, semilla - margen)
        lim_sup = min(t_fin,    semilla + margen)

        res = minimize_scalar(
            funcion_costo_ventana,
            bounds=(lim_inf, lim_sup),
            method="bounded",
            args=(nombre_origen, nombre_destino),
        )

        # Aceptamos solo resultados razonablemente buenos
        if res.fun < 1.0:
            mejores.append({"tiempo": res.x, "costo": res.fun})

    mejores.sort(key=lambda r: r["costo"])

    # Eliminar duplicados: ventanas separadas por menos de 5 dias se consideran la misma
    ventanas_unicas = []
    for res in mejores:
        es_duplicado = any(
            abs(res["tiempo"] - v["tiempo"]) < 5.0
            for v in ventanas_unicas
        )
        if not es_duplicado:
            ventanas_unicas.append(res)

    if not ventanas_unicas:
        raise RuntimeError("No se encontro ninguna ventana de lanzamiento en el rango dado.")

    mejor = ventanas_unicas[0]

    transferencia   = calcular_transferencia_hohmann(radio_origen, radio_destino)
    angulo_ideal    = calcular_angulo_fase_requerido(radio_origen, radio_destino)
    angulo_real     = angulo_fase_actual(nombre_origen, nombre_destino, mejor["tiempo"])

    alternativas = [
        {"tiempo_dias": round(v["tiempo"], 2), "costo": round(v["costo"], 6)}
        for v in ventanas_unicas[1:4]
    ]

    return {
        "tiempo_optimo":     round(mejor["tiempo"], 2),
        "delta_v_optimo":    transferencia["delta_v_total"],
        "angulo_fase_ideal": angulo_ideal,
        "angulo_fase_real":  angulo_real,
        "costo_minimo":      mejor["costo"],
        "tiempo_vuelo_dias": transferencia["tiempo_vuelo_dias"],
        "alternativas":      alternativas,
    }


def evaluar_rango_ventanas(nombre_origen, nombre_destino, t_inicio=0, t_fin=730, n_puntos=300):
    """
    Evalua la funcion de costo en todo el rango de busqueda.

    Util para graficar la curva de oportunidad de lanzamiento a lo largo del tiempo
    y visualizar donde se encuentran los minimos (ventanas favorables).

    Retorna
    -------
    dict con claves 'tiempos' y 'costos' (arrays numpy)
    """
    tiempos = np.linspace(t_inicio, t_fin, n_puntos)
    costos  = np.array([
        funcion_costo_ventana(t, nombre_origen, nombre_destino)
        for t in tiempos
    ])
    return {"tiempos": tiempos, "costos": costos}
