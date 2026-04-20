"""
Constantes fisicas, parametros orbitales y configuracion general del proyecto.

Todos los valores estan en el Sistema Internacional (SI) salvo indicacion contraria.
Los radios orbitales estan en metros y los periodos en segundos.
"""

# Constante gravitacional universal (m^3 / kg / s^2)
G = 6.674e-11

# Masa del Sol en kilogramos
MASA_SOL = 1.989e30

# Parametro gravitacional estandar del Sol: mu = G * M
MU_SOL = G * MASA_SOL

# Unidad Astronomica en metros
UA = 1.496e11

# Segundos por dia
SEGUNDOS_POR_DIA = 86400

# Segundos por anio (365.25 dias)
SEGUNDOS_POR_ANIO = 365.25 * SEGUNDOS_POR_DIA

# Datos orbitales simplificados de los planetas.
# Se asumen orbitas circulares en el plano ecliptico.
# radio_orbital en metros, periodo_orbital en segundos, color para graficas.
PLANETAS = {
    "Mercurio": {
        "radio_orbital":   0.387 * UA,
        "periodo_orbital": 87.97 * SEGUNDOS_POR_DIA,
        "color":           "gray",
    },
    "Venus": {
        "radio_orbital":   0.723 * UA,
        "periodo_orbital": 224.70 * SEGUNDOS_POR_DIA,
        "color":           "orange",
    },
    "Tierra": {
        "radio_orbital":   1.000 * UA,
        "periodo_orbital": 365.25 * SEGUNDOS_POR_DIA,
        "color":           "blue",
    },
    "Marte": {
        "radio_orbital":   1.524 * UA,
        "periodo_orbital": 686.97 * SEGUNDOS_POR_DIA,
        "color":           "red",
    },
    "Jupiter": {
        "radio_orbital":   5.203 * UA,
        "periodo_orbital": 4332.59 * SEGUNDOS_POR_DIA,
        "color":           "brown",
    },
    "Saturno": {
        "radio_orbital":   9.537 * UA,
        "periodo_orbital": 10759.22 * SEGUNDOS_POR_DIA,
        "color":           "yellow",
    },
}

# Planeta origen y destino por defecto al abrir la aplicacion
PLANETA_ORIGEN_DEFAULT  = "Tierra"
PLANETA_DESTINO_DEFAULT = "Marte"

# Rango de busqueda de ventana de lanzamiento en dias
VENTANA_BUSQUEDA_DIAS = 730

# Parametros fisicos como diccionario para pasar entre modulos si se necesita
PARAMETROS_FISICOS = {
    "mu_sol":            MU_SOL,
    "ua":                UA,
    "segundos_por_dia":  SEGUNDOS_POR_DIA,
}
