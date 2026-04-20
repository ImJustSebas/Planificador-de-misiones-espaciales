"""
Generacion de graficas para el planificador de misiones.

Incluye visualizacion de orbitas, trayectoria de transferencia
y curva de ventanas de lanzamiento. Las graficas se abren en
ventanas independientes de Matplotlib.
"""

import numpy as np
import matplotlib.pyplot as plt

from config.configuracion import PLANETAS, UA
from fisica.orbita import puntos_orbita_circular, puntos_orbita_transferencia
from datos.efemerides_simuladas import obtener_posicion_planeta

FONDO       = "white"
COLOR_TEXTO = "black"
COLOR_EJES  = "black"
COLOR_GRID  = "lightgray"
COLOR_BORDE = "gray"


def _aplicar_estilo_oscuro(ax):
    """Aplica el tema oscuro comun a todos los ejes."""
    ax.set_facecolor(FONDO)
    ax.tick_params(colors=COLOR_EJES)
    for spine in ax.spines.values():
        spine.set_edgecolor(COLOR_BORDE)
    ax.grid(True, color=COLOR_GRID, linewidth=0.5)


def graficar_orbitas_y_transferencia(nombre_origen, nombre_destino, tiempo_salida_dias, resultado_busqueda):
    """
    Dibuja el sistema solar simplificado con las orbitas de los planetas
    involucrados y la trayectoria de transferencia de Hohmann.

    Parametros
    ----------
    nombre_origen         : str
    nombre_destino        : str
    tiempo_salida_dias    : float - Tiempo de salida en dias
    resultado_busqueda    : dict  - Resultado de buscar_ventana_optima
    """
    fig, ax = plt.subplots(figsize=(8, 8), facecolor=FONDO)
    ax.set_aspect("equal")
    ax.set_title("Transferencia orbital", color=COLOR_TEXTO, fontsize=13, pad=14)
    _aplicar_estilo_oscuro(ax)

    # Sol en el centro
    ax.plot(0, 0, "o", color="gold", markersize=14, zorder=5, label="Sol")

    for nombre in [nombre_origen, nombre_destino]:
        datos  = PLANETAS[nombre]
        radio  = datos["radio_orbital"]
        color  = datos["color"]

        ox, oy = puntos_orbita_circular(radio)
        ax.plot(ox / UA, oy / UA, "-", color=color, alpha=0.3, linewidth=0.9)

        px, py = obtener_posicion_planeta(nombre, tiempo_salida_dias)
        ax.plot(px / UA, py / UA, "o", color=color, markersize=8, zorder=4)
        ax.annotate(
            nombre,
            (px / UA, py / UA),
            textcoords="offset points",
            xytext=(8, 5),
            color=COLOR_TEXTO,
            fontsize=9,
        )

    # Trayectoria de transferencia
    radio_origen  = PLANETAS[nombre_origen]["radio_orbital"]
    radio_destino = PLANETAS[nombre_destino]["radio_orbital"]
    tx, ty = puntos_orbita_transferencia(radio_origen, radio_destino)
    ax.plot(tx / UA, ty / UA, "--", color="blue", linewidth=1.4, label="Transferencia Hohmann")

    # Posicion del destino al momento de llegada
    tiempo_llegada = tiempo_salida_dias + resultado_busqueda["tiempo_vuelo_dias"]
    dx, dy = obtener_posicion_planeta(nombre_destino, tiempo_llegada)
    ax.plot(
        dx / UA, dy / UA, "s",
        color=PLANETAS[nombre_destino]["color"],
        markersize=9, zorder=4,
        label=f"{nombre_destino} (llegada)",
    )
    ax.annotate(
        "llegada",
        (dx / UA, dy / UA),
        textcoords="offset points",
        xytext=(8, -12),
        color=COLOR_TEXTO,
        fontsize=8,
        fontstyle="italic",
    )

    ax.set_xlabel("x [UA]", color=COLOR_EJES)
    ax.set_ylabel("y [UA]", color=COLOR_EJES)
    ax.legend(facecolor="white", edgecolor=COLOR_BORDE, labelcolor=COLOR_TEXTO, fontsize=8)
    plt.tight_layout()
    plt.show()


def graficar_ventanas_lanzamiento(nombre_origen, nombre_destino, datos_rango):
    """
    Grafica la curva de costo de la ventana de lanzamiento a lo largo del tiempo.

    Los minimos de la curva corresponden a las mejores ventanas de salida.

    Parametros
    ----------
    nombre_origen  : str
    nombre_destino : str
    datos_rango    : dict con 'tiempos' y 'costos' (arrays numpy)
    """
    tiempos = datos_rango["tiempos"]
    costos  = datos_rango["costos"]

    fig, ax = plt.subplots(figsize=(9, 4), facecolor=FONDO)
    _aplicar_estilo_oscuro(ax)

    ax.plot(tiempos, costos, color="blue", linewidth=1.3)
    ax.set_title(
        f"Curva de oportunidad de lanzamiento: {nombre_origen} -> {nombre_destino}",
        color=COLOR_TEXTO, fontsize=11,
    )
    ax.set_xlabel("Tiempo desde epoca de referencia (dias)", color=COLOR_EJES)
    ax.set_ylabel("Costo (diferencia de fase cuadratica)", color=COLOR_EJES)

    # Marcamos el minimo mas visible
    idx_min = np.argmin(costos)
    ax.axvline(
        x=tiempos[idx_min],
        color="red",
        linestyle="--",
        linewidth=0.9,
        label=f"Minimo aprox. en dia {tiempos[idx_min]:.0f}",
    )
    ax.legend(facecolor="white", edgecolor=COLOR_BORDE, labelcolor=COLOR_TEXTO, fontsize=8)
    plt.tight_layout()
    plt.show()


def graficar_comparacion_ventanas(resultado_busqueda):
    """
    Muestra un grafico de barras comparando la ventana optima con las alternativas.

    Parametros
    ----------
    resultado_busqueda : dict - Resultado de buscar_ventana_optima
    """
    optima       = {"tiempo_dias": resultado_busqueda["tiempo_optimo"],
                    "costo":       resultado_busqueda["costo_minimo"]}
    alternativas = resultado_busqueda.get("alternativas", [])

    etiquetas = [f"Optima\n({optima['tiempo_dias']:.0f} d)"]
    costos    = [optima["costo"]]
    colores   = ["lightblue"]

    for i, alt in enumerate(alternativas):
        etiquetas.append(f"Alt. {i + 1}\n({alt['tiempo_dias']:.0f} d)")
        costos.append(alt["costo"])
        colores.append("lightgray")

    fig, ax = plt.subplots(figsize=(6, 4), facecolor=FONDO)
    _aplicar_estilo_oscuro(ax)

    barras = ax.bar(etiquetas, costos, color=colores, width=0.5, edgecolor=COLOR_BORDE)
    ax.set_title("Comparacion de ventanas de lanzamiento", color=COLOR_TEXTO, fontsize=11)
    ax.set_ylabel("Costo (diferencia de fase cuadratica)", color=COLOR_EJES)

    for barra, costo in zip(barras, costos):
        ax.text(
            barra.get_x() + barra.get_width() / 2,
            barra.get_height() + max(costos) * 0.01,
            f"{costo:.4f}",
            ha="center", va="bottom",
            color=COLOR_TEXTO, fontsize=8,
        )

    plt.tight_layout()
    plt.show()
