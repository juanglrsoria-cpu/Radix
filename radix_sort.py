
import tkinter as tk
from tkinter import messagebox

# Paleta visual
FONDO = "#101827"
PANEL = "#1c2940"
TEXTO = "#f4f7ff"
SECUNDARIO = "#aab8d0"
ACCENT = "#35d39a"
VERDE = "#35d39a"
NARANJA = "#ffad5c"
ROJO = "#ff647c"

class AplicacionOrdenamiento:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("VISUAL SORT | RADIX SORT")
        self.raiz.geometry("1000x720")
        self.raiz.minsize(850, 650)
        self.raiz.configure(bg=FONDO)

        self.frames = []
        self.paso = 0
        self.after_id = None
        self.crear_interfaz()

    def crear_interfaz(self):
        encabezado = tk.Frame(self.raiz, bg=FONDO)
        encabezado.pack(fill="x", padx=28, pady=(22, 10))

        tk.Label(encabezado, text="ALGORITMOS DE ORDENAMIENTO",
                 bg=FONDO, fg=ACCENT, font=("Segoe UI", 10, "bold")).pack(anchor="w")
        tk.Label(encabezado, text="RADIX SORT",
                 bg=FONDO, fg=TEXTO, font=("Segoe UI", 25, "bold")).pack(anchor="w", pady=(4, 0))
        tk.Label(encabezado, text="Explora cómo se mueven los datos paso a paso.",
                 bg=FONDO, fg=SECUNDARIO, font=("Segoe UI", 11)).pack(anchor="w", pady=(2, 0))

        controles = tk.Frame(self.raiz, bg=PANEL, highlightbackground="#344765",
                             highlightthickness=1)
        controles.pack(fill="x", padx=28, pady=12)

        tk.Label(controles, text="CANTIDAD DE NÚMEROS",
                 bg=PANEL, fg=SECUNDARIO, font=("Segoe UI", 9, "bold")).grid(
                     row=0, column=0, sticky="w", padx=(16, 8), pady=(13, 4))
        self.cantidad = tk.Entry(controles, width=12, font=("Segoe UI", 12),
                                 bg="#263752", fg=TEXTO, insertbackground=TEXTO,
                                 relief="flat")
        self.cantidad.insert(0, "8")
        self.cantidad.grid(row=1, column=0, padx=(16, 8), pady=(0, 14), ipady=7)

        tk.Label(controles, text="NÚMEROS (separados por comas)",
                 bg=PANEL, fg=SECUNDARIO, font=("Segoe UI", 9, "bold")).grid(
                     row=0, column=1, sticky="w", padx=8, pady=(13, 4))
        self.entrada = tk.Entry(controles, width=48, font=("Segoe UI", 12),
                                bg="#263752", fg=TEXTO, insertbackground=TEXTO,
                                relief="flat")
        self.entrada.insert(0, "38, 12, 65, 7, 42, 19, 81, 25")
        self.entrada.grid(row=1, column=1, padx=8, pady=(0, 14), ipady=7)

        botones = tk.Frame(controles, bg=PANEL)
        botones.grid(row=1, column=2, padx=12, pady=(0, 14))
        tk.Button(botones, text="▶  ORDENAR", command=self.iniciar,
                  bg=ACCENT, fg="#101827", activebackground=ACCENT,
                  font=("Segoe UI", 10, "bold"), relief="flat",
                  padx=15, pady=9, cursor="hand2").pack(side="left", padx=4)
        tk.Button(botones, text="↻  REINICIAR", command=self.reiniciar,
                  bg="#344765", fg=TEXTO, activebackground="#405779",
                  font=("Segoe UI", 10, "bold"), relief="flat",
                  padx=12, pady=9, cursor="hand2").pack(side="left", padx=4)

        visual = tk.Frame(self.raiz, bg=PANEL, highlightbackground="#344765",
                          highlightthickness=1)
        visual.pack(fill="both", expand=True, padx=28, pady=(2, 10))

        top = tk.Frame(visual, bg=PANEL)
        top.pack(fill="x", padx=18, pady=(14, 4))
        self.estado = tk.Label(top, text="LISTO PARA COMENZAR",
                               bg=PANEL, fg=ACCENT,
                               font=("Segoe UI", 11, "bold"))
        self.estado.pack(side="left")
        self.contador = tk.Label(top, text="PASO 0",
                                 bg=PANEL, fg=SECUNDARIO,
                                 font=("Segoe UI", 9, "bold"))
        self.contador.pack(side="right")

        self.canvas = tk.Canvas(visual, bg="#152238", height=350,
                                highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=16, pady=12)

        leyenda = tk.Frame(visual, bg=PANEL)
        leyenda.pack(fill="x", padx=18, pady=(0, 12))
        for color, texto in [(ACCENT, "Elemento activo"), (NARANJA, "Comparación"),
                             (VERDE, "Posición definitiva")]:
            item = tk.Frame(leyenda, bg=PANEL)
            item.pack(side="left", padx=(0, 22))
            tk.Label(item, text="●", fg=color, bg=PANEL,
                     font=("Segoe UI", 12)).pack(side="left")
            tk.Label(item, text=texto, fg=SECUNDARIO, bg=PANEL,
                     font=("Segoe UI", 9)).pack(side="left", padx=5)

        pie = tk.Frame(self.raiz, bg=FONDO)
        pie.pack(fill="x", padx=30, pady=(0, 15))
        self.detalle = tk.Label(pie, text="Ingresa los datos y presiona ORDENAR.",
                                bg=FONDO, fg=SECUNDARIO,
                                font=("Segoe UI", 10), anchor="w")
        self.detalle.pack(fill="x")

        self.raiz.bind("<Configure>", lambda e: self.dibujar_actual())

    def crear_pasos(self, datos):
        raise NotImplementedError

    def iniciar(self):
        self.detener_animacion()
        try:
            cantidad = int(self.cantidad.get())
            valores = [int(x.strip()) for x in self.entrada.get().split(",") if x.strip()]
            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor que cero.")
            if len(valores) != cantidad:
                raise ValueError(f"Indicaste {cantidad} números, pero escribiste {len(valores)}.")
            if len(valores) > 30:
                raise ValueError("Para una visualización clara, utiliza máximo 30 números.")
        except ValueError as error:
            messagebox.showerror("Revisa los datos", str(error))
            return

        self.frames = self.crear_pasos(valores)
        self.paso = 0
        self.animar()

    def animar(self):
        self.dibujar_actual()
        if self.paso < len(self.frames) - 1:
            self.paso += 1
            self.after_id = self.raiz.after(420, self.animar)

    def dibujar_actual(self):
        if not hasattr(self, "frames") or not self.frames:
            return
        if self.paso >= len(self.frames):
            return
        valores, activos, comparados, fijos, mensaje = self.frames[self.paso]
        self.canvas.delete("all")
        ancho = max(self.canvas.winfo_width(), 500)
        alto = max(self.canvas.winfo_height(), 250)
        margen_x = 35
        espacio = 7
        bw = max(12, (ancho - 2*margen_x - espacio*(len(valores)-1)) / len(valores))
        maximo = max([abs(v) for v in valores] + [1])
        base_y = alto - 45
        area_h = alto - 105

        # Línea base y guía
        self.canvas.create_line(margen_x-10, base_y, ancho-margen_x+10, base_y,
                                fill="#50617c", width=2)
        for i, valor in enumerate(valores):
            x1 = margen_x + i*(bw+espacio)
            x2 = x1 + bw
            barra_h = max(7, area_h * abs(valor) / maximo)
            y1 = base_y - barra_h
            if i in fijos:
                color = VERDE
            elif i in activos:
                color = ACCENT
            elif i in comparados:
                color = NARANJA
            else:
                color = "#49617f"
            self.canvas.create_rectangle(x1, y1, x2, base_y,
                                         fill=color, outline="")
            self.canvas.create_text((x1+x2)/2, y1-15, text=str(valor),
                                    fill=TEXTO, font=("Segoe UI", 10, "bold"))
            self.canvas.create_text((x1+x2)/2, base_y+17, text=str(i+1),
                                    fill=SECUNDARIO, font=("Segoe UI", 8))
        self.estado.config(text=mensaje.upper())
        self.contador.config(text=f"PASO {self.paso+1} / {len(self.frames)}")
        self.detalle.config(text="Azul: elemento activo   |   Naranja: comparación   |   Verde: posición definitiva")

    def detener_animacion(self):
        if self.after_id is not None:
            self.raiz.after_cancel(self.after_id)
            self.after_id = None

    def reiniciar(self):
        self.detener_animacion()
        self.frames = []
        self.paso = 0
        self.canvas.delete("all")
        self.estado.config(text="LISTO PARA COMENZAR")
        self.contador.config(text="PASO 0")
        self.detalle.config(text="Ingresa los datos y presiona ORDENAR.")


    def crear_pasos(self, datos):
        # Radix sort visual admite enteros positivos y negativos.
        a = datos.copy()
        pasos = [(a.copy(), [], [], [], "Lista original")]

        def radix_positivo(valores, etiqueta):
            if not valores:
                return []
            exp = 1
            maximo = max(valores)
            while maximo // exp > 0:
                cubetas = [[] for _ in range(10)]
                for v in valores:
                    digito = (v // exp) % 10
                    cubetas[digito].append(v)
                    pasos.append((a.copy(), [], [], [], f"{etiqueta}: distribuyendo por dígito {digito}"))
                valores = [v for cubeta in cubetas for v in cubeta]
                pasos.append((a.copy(), [], [], [], f"{etiqueta}: reuniendo por posición {exp}"))
                exp *= 10
            return valores

        negativos = [-v for v in datos if v < 0]
        positivos = [v for v in datos if v >= 0]
        neg_ord = radix_positivo(negativos, "Negativos")
        pos_ord = radix_positivo(positivos, "Positivos")
        resultado = [-v for v in reversed(neg_ord)] + pos_ord
        pasos.append((resultado.copy(), [], [], list(range(len(resultado))), "¡Radix Sort terminado!"))
        return pasos


if __name__ == "__main__":
    ventana = tk.Tk()
    app = AplicacionOrdenamiento(ventana)
    ventana.mainloop()
