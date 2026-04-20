"""
Punto de entrada del planificador de misiones espaciales.

Modos de uso:
  python main.py            -> Lanza la interfaz grafica
  python main.py --consola  -> Ejecuta una simulacion de prueba en terminal
"""

import sys
import argparse


def modo_consola():
    from config.configuracion import PLANETAS
    from fisica.transferencias import calcular_transferencia_hohmann
    from optimizacion.buscador_ruta import buscar_ventana_optima
    from utilidades.auxiliares import formatear_delta_v, formatear_tiempo

    print("=== Planificador de Misiones Espaciales ===")
    print()

    origen  = "Tierra"
    destino = "Marte"

    print(f"Origen  : {origen}")
    print(f"Destino : {destino}")
    print()

    radio_origen  = PLANETAS[origen]["radio_orbital"]
    radio_destino = PLANETAS[destino]["radio_orbital"]

    transferencia = calcular_transferencia_hohmann(radio_origen, radio_destino)

    print("Transferencia de Hohmann:")
    print(f"  Delta-v total  : {formatear_delta_v(transferencia['delta_v_total'])}")
    print(f"  Tiempo de vuelo: {formatear_tiempo(transferencia['tiempo_vuelo_s'])}")
    print()

    resultado = buscar_ventana_optima(origen, destino, t_inicio=0, t_fin=700)

    print("Ventana optima de lanzamiento:")
    print(f"  Tiempo de salida (dias): {resultado['tiempo_optimo']:.2f}")
    print(f"  Delta-v estimado       : {formatear_delta_v(resultado['delta_v_optimo'])}")

    if resultado["alternativas"]:
        print()
        print("Ventanas alternativas:")
        for i, alt in enumerate(resultado["alternativas"]):
            print(f"  Alt. {i+1}: dia {alt['tiempo_dias']:.1f}")


def modo_interfaz():
    from interfaz.ventana_principal import iniciar_interfaz
    iniciar_interfaz()


def main():
    parser = argparse.ArgumentParser(
        description="Planificador de misiones espaciales con optimizacion de trayectorias."
    )
    parser.add_argument(
        "--consola",
        action="store_true",
        help="Ejecuta una simulacion rapida en modo consola."
    )
    args = parser.parse_args()

    if args.consola:
        modo_consola()
    else:
        modo_interfaz()


if __name__ == "__main__":
    main()
