import tkinter as tk
from tkinter import simpledialog


class RadixSortApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ordenamiento Gráfico - Radix Sort")
        self.root.geometry("780x500")
        self.root.configure(bg="#0f172a")

        self.datos = []
        self.ordenando = False

        tk.Label(
            root, text="RADIX SORT - VISUALIZACIÓN POR DÍGITOS Y CUBETAS",
            font=("Segoe UI", 14, "bold"), bg="#0f172a", fg="#f8fafc"
        ).pack(pady=(12, 4))

        self.lbl_estado = tk.Label(
            root, text="Presiona 'Ingresar Números' para comenzar",
            font=("Segoe UI", 10), bg="#0f172a", fg="#94a3b8"
        )
        self.lbl_estado.pack(pady=(0, 8))

        self.canvas = tk.Canvas(root, width=720, height=330, bg="#1e293b", highlightthickness=0)
        self.canvas.pack(pady=6)

        frame_botones = tk.Frame(root, bg="#0f172a")
        frame_botones.pack(pady=12)

        self.btn_ingresar = tk.Button(
            frame_botones, text="1. Ingresar Números y Ordenar",
            font=("Segoe UI", 10, "bold"), bg="#2563eb", fg="white",
            activebackground="#1d4ed8", activeforeground="white",
            padx=16, pady=8, relief="flat", cursor="hand2",
            command=self.iniciar_proceso
        )
        self.btn_ingresar.grid(row=0, column=0, padx=10)

        self.btn_salir = tk.Button(
            frame_botones, text="2. Salir",
            font=("Segoe UI", 10, "bold"), bg="#dc2626", fg="white",
            activebackground="#b91c1c", activeforeground="white",
            padx=16, pady=8, relief="flat", cursor="hand2",
            command=self.root.destroy
        )
        self.btn_salir.grid(row=0, column=1, padx=10)

    def dibujar_barras(self, colores=None):
        self.canvas.delete("all")
        if not self.datos:
            return
        if colores is None:
            colores = ["#38bdf8"] * len(self.datos)

        w, h = 720, 330
        n = len(self.datos)
        margen_x = 30
        ancho_disponible = w - 2 * margen_x
        ancho_barra = max(8, (ancho_disponible / n) - 6)

        min_val = min(self.datos)
        desplazamiento = abs(min_val) + 1 if min_val <= 0 else 0
        max_ajustado = max(x + desplazamiento for x in self.datos)

        for i, val in enumerate(self.datos):
            altura = max(20, ((val + desplazamiento) / max_ajustado) * (h - 60))
            x0 = margen_x + i * (ancho_disponible / n)
            y0 = h - 30 - altura
            x1 = x0 + ancho_barra
            y1 = h - 30

            self.canvas.create_rectangle(x0, y0, x1, y1, fill=colores[i], outline="")
            self.canvas.create_text(
                (x0 + x1) / 2, y0 - 10, text=str(val),
                fill="#f8fafc", font=("Consolas", 9, "bold")
            )
            self.canvas.create_text(
                (x0 + x1) / 2, y1 + 12, text=f"[{i}]",
                fill="#94a3b8", font=("Consolas", 8)
            )
        self.root.update()

    def iniciar_proceso(self):
        if self.ordenando:
            return

        cantidad = simpledialog.askinteger(
            "Cantidad", "¿Cuántos números deseas ordenar?",
            parent=self.root, minvalue=1, maxvalue=30
        )
        if cantidad is None:
            return

        numeros = []
        for i in range(cantidad):
            num = simpledialog.askinteger(
                "Captura de datos", f"Ingresa el número {i + 1} de {cantidad}:",
                parent=self.root
            )
            if num is None:
                return
            numeros.append(num)

        self.datos = numeros
        self.ordenando = True
        self.btn_ingresar.config(state="disabled")
        self.lbl_estado.config(text=f"Lista original: {self.datos}")
        self.dibujar_barras()
        self.root.after(600, self.ejecutar_radixsort)

    def ordenar_grupo_radix(self, grupo, signo):
        if not grupo:
            return []
        lista = grupo.copy()
        max_num = max(lista)
        exp = 1
        paleta = ["#f43f5e", "#f97316", "#facc15", "#4ade80", "#2dd4bf",
                  "#38bdf8", "#818cf8", "#c084fc", "#f472b6", "#fb7185"]

        while max_num // exp > 0:
            cubetas = [[] for _ in range(10)]
            for num in lista:
                digito = (num // exp) % 10
                cubetas[digito].append(num)

            lista = [num for cubeta in cubetas for num in cubeta]
            # Actualizar vista parcial
            if signo == "Negativos":
                actual = [-x for x in reversed(lista)] + [x for x in self.datos if x >= 0]
            else:
                actual = [x for x in self.datos if x < 0] + lista
            self.datos = actual

            colores = [paleta[(abs(val) // exp) % 10] for val in self.datos]
            self.lbl_estado.config(text=f"Radix ({signo}) | Agrupando por dígito posición 10^{len(str(exp))-1} (divisor={exp})")
            self.dibujar_barras(colores)
            self.root.after(700)
            exp *= 10

        return lista

    def ejecutar_radixsort(self):
        negativos = [-x for x in self.datos if x < 0]
        positivos = [x for x in self.datos if x >= 0]

        neg_ord = [-x for x in reversed(self.ordenar_grupo_radix(negativos, "Negativos"))] if negativos else []
        pos_ord = self.ordenar_grupo_radix(positivos, "Positivos") if positivos else []

        self.datos = neg_ord + pos_ord
        self.dibujar_barras(["#22c55e"] * len(self.datos))
        self.lbl_estado.config(text=f"¡Ordenado con Radix Sort!: {self.datos}")
        self.ordenando = False
        self.btn_ingresar.config(state="normal")


if __name__ == "__main__":
    root = tk.Tk()
    app = RadixSortApp(root)
    root.mainloop()