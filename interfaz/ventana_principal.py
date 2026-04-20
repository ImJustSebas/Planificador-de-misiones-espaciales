"""
Interfaz grafica principal del planificador de misiones.

Construida con Tkinter. Permite seleccionar planetas, ejecutar la
optimizacion y visualizar los resultados desde una ventana limpia.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

from config.configuracion import (
    PLANETAS,
    PLANETA_ORIGEN_DEFAULT,
    PLANETA_DESTINO_DEFAULT,
    VENTANA_BUSQUEDA_DIAS,
)
from fisica.transferencias import calcular_transferencia_hohmann
from optimizacion.buscador_ruta import buscar_ventana_optima, evaluar_rango_ventanas
from visualizacion.graficos import (
    graficar_orbitas_y_transferencia,
    graficar_ventanas_lanzamiento,
    graficar_comparacion_ventanas,
)
from utilidades.auxiliares import formatear_delta_v, formatear_tiempo, formatear_dias


FUENTE_TITULO = ("Helvetica", 14, "bold")
FUENTE_NORMAL = ("Helvetica", 10)
FUENTE_MONO   = ("Courier", 10)


class VentanaPrincipal:
    """Ventana principal de la aplicacion."""

    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Planificador de Misiones Espaciales")
        self.raiz.resizable(False, False)

        self.resultado_actual = None

        self._construir_ui()

    def _construir_ui(self):
        """Construye todos los elementos de la interfaz."""

        # Titulo superior
        tk.Label(
            self.raiz,
            text="Planificador de Misiones Espaciales",
            font=FUENTE_TITULO,
        ).grid(row=0, column=0, columnspan=2, pady=(18, 4))

        tk.Label(
            self.raiz,
            text="Transferencias orbitales con optimizacion de ventana de lanzamiento",
            font=("Helvetica", 9),
        ).grid(row=1, column=0, columnspan=2, pady=(0, 12))

        # Panel de seleccion de mision
        panel_sel = tk.Frame(self.raiz, padx=20, pady=14, relief="sunken", bd=1)
        panel_sel.grid(row=2, column=0, columnspan=2, padx=24, pady=4, sticky="ew")

        nombres_planetas = list(PLANETAS.keys())

        tk.Label(panel_sel, text="Planeta origen:", font=FUENTE_NORMAL).grid(row=0, column=0, sticky="w", pady=5)
        self.var_origen = tk.StringVar(value=PLANETA_ORIGEN_DEFAULT)
        ttk.Combobox(
            panel_sel,
            textvariable=self.var_origen,
            values=nombres_planetas,
            state="readonly",
            width=16,
        ).grid(row=0, column=1, sticky="w", padx=12)

        tk.Label(panel_sel, text="Planeta destino:", font=FUENTE_NORMAL).grid(row=1, column=0, sticky="w", pady=5)
        self.var_destino = tk.StringVar(value=PLANETA_DESTINO_DEFAULT)
        ttk.Combobox(
            panel_sel,
            textvariable=self.var_destino,
            values=nombres_planetas,
            state="readonly",
            width=16,
        ).grid(row=1, column=1, sticky="w", padx=12)

        tk.Label(panel_sel, text="Rango de busqueda (dias):", font=FUENTE_NORMAL).grid(row=2, column=0, sticky="w", pady=5)
        self.var_rango = tk.IntVar(value=VENTANA_BUSQUEDA_DIAS)
        tk.Entry(
            panel_sel,
            textvariable=self.var_rango,
            width=8,
        ).grid(row=2, column=1, sticky="w", padx=12)

        # Fila de botones de accion
        frame_botones = tk.Frame(self.raiz)
        frame_botones.grid(row=3, column=0, columnspan=2, pady=12)

        self._boton(frame_botones, "Calcular mision",   self._ejecutar_calculo).pack(side="left", padx=6)
        self._boton(frame_botones, "Ver orbitas",        self._ver_orbitas).pack(side="left", padx=6)
        self._boton(frame_botones, "Ver ventanas",       self._ver_ventanas).pack(side="left", padx=6)
        self._boton(frame_botones, "Comparar ventanas",  self._ver_comparacion).pack(side="left", padx=6)

        # Panel de resultados
        panel_res = tk.Frame(self.raiz, padx=20, pady=12, relief="sunken", bd=1)
        panel_res.grid(row=4, column=0, columnspan=2, padx=24, pady=4, sticky="ew")

        tk.Label(
            panel_res,
            text="Resultados",
            font=("Helvetica", 11, "bold"),
        ).pack(anchor="w")

        self.texto_resultados = tk.Text(
            panel_res,
            height=12,
            width=60,
            font=FUENTE_MONO,
            relief="sunken",
            bd=1,
            state="disabled",
            wrap="word",
        )
        self.texto_resultados.pack(pady=(8, 0))

        # Barra de estado inferior
        self.var_estado = tk.StringVar(value="Listo.")
        tk.Label(
            self.raiz,
            textvariable=self.var_estado,
            font=("Helvetica", 8),
        ).grid(row=5, column=0, columnspan=2, pady=(4, 14))

    def _boton(self, padre, texto, comando):
        """Crea un boton con el estilo por defecto de tkinter."""
        return tk.Button(
            padre,
            text=texto,
            command=comando,
            font=FUENTE_NORMAL,
            padx=12,
            pady=6,
        )

    def _validar_seleccion(self):
        """Verifica que origen y destino sean validos y distintos."""
        origen  = self.var_origen.get()
        destino = self.var_destino.get()

        if origen not in PLANETAS or destino not in PLANETAS:
            messagebox.showerror("Error", "Seleccion de planeta no valida.")
            return False

        if origen == destino:
            messagebox.showwarning(
                "Seleccion invalida",
                "El planeta de origen y el de destino deben ser distintos.",
            )
            return False

        return True

    def _ejecutar_calculo(self):
        """Lanza la optimizacion y muestra los resultados en el panel de texto."""
        if not self._validar_seleccion():
            return

        origen  = self.var_origen.get()
        destino = self.var_destino.get()
        rango   = self.var_rango.get()

        self.var_estado.set("Calculando ventana optima...")
        self.raiz.update()

        try:
            resultado = buscar_ventana_optima(origen, destino, t_inicio=0, t_fin=rango)
            self.resultado_actual = resultado

            transferencia = calcular_transferencia_hohmann(
                PLANETAS[origen]["radio_orbital"],
                PLANETAS[destino]["radio_orbital"],
            )

            lineas = [
                f"Mision: {origen}  ->  {destino}",
                "-" * 46,
                f"  Delta-v total        : {formatear_delta_v(resultado['delta_v_optimo'])}",
                f"  Tiempo de vuelo      : {formatear_dias(resultado['tiempo_vuelo_dias'])}",
                f"  Salida optima        : dia {resultado['tiempo_optimo']:.1f}",
                f"  Angulo de fase ideal : {np.degrees(resultado['angulo_fase_ideal']):.2f} grados",
                f"  Angulo de fase real  : {np.degrees(resultado['angulo_fase_real']):.2f} grados",
                "",
                "Desglose del delta-v (Hohmann):",
                f"  Primer impulso       : {formatear_delta_v(transferencia['delta_v_1'])}",
                f"  Segundo impulso      : {formatear_delta_v(transferencia['delta_v_2'])}",
                "",
                "Ventanas alternativas:",
            ]

            if resultado["alternativas"]:
                for i, alt in enumerate(resultado["alternativas"]):
                    lineas.append(f"  Alt. {i + 1}: dia {alt['tiempo_dias']:.1f}  (costo {alt['costo']:.5f})")
            else:
                lineas.append("  No se encontraron alternativas en el rango dado.")

            self._mostrar_texto("\n".join(lineas))
            self.var_estado.set("Calculo completado.")

        except Exception as e:
            messagebox.showerror("Error en el calculo", str(e))
            self.var_estado.set("Error durante el calculo.")

    def _ver_orbitas(self):
        """Abre la grafica de orbitas y trayectoria de transferencia."""
        if not self._validar_seleccion():
            return
        if self.resultado_actual is None:
            messagebox.showinfo("Aviso", "Ejecuta primero el calculo de la mision.")
            return

        graficar_orbitas_y_transferencia(
            self.var_origen.get(),
            self.var_destino.get(),
            self.resultado_actual["tiempo_optimo"],
            self.resultado_actual,
        )

    def _ver_ventanas(self):
        """Abre la grafica de curva de oportunidad de lanzamiento."""
        if not self._validar_seleccion():
            return

        datos = evaluar_rango_ventanas(
            self.var_origen.get(),
            self.var_destino.get(),
            t_inicio=0,
            t_fin=self.var_rango.get(),
        )
        graficar_ventanas_lanzamiento(
            self.var_origen.get(),
            self.var_destino.get(),
            datos,
        )

    def _ver_comparacion(self):
        """Abre el grafico de comparacion de ventanas."""
        if self.resultado_actual is None:
            messagebox.showinfo("Aviso", "Ejecuta primero el calculo de la mision.")
            return
        graficar_comparacion_ventanas(self.resultado_actual)

    def _mostrar_texto(self, contenido):
        """Escribe contenido en el panel de resultados."""
        self.texto_resultados.config(state="normal")
        self.texto_resultados.delete("1.0", "end")
        self.texto_resultados.insert("end", contenido)
        self.texto_resultados.config(state="disabled")


def iniciar_interfaz():
    """Crea y lanza la ventana principal de la aplicacion."""
    raiz = tk.Tk()
    VentanaPrincipal(raiz)
    raiz.mainloop()
