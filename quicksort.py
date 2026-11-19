import tkinter as tk
from tkinter import simpledialog


class QuickSortApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ordenamiento Gráfico - Quicksort")
        self.root.geometry("760x480")
        self.root.configure(bg="#0f172a")

        self.datos = []
        self.ordenando = False

        tk.Label(
            root, text="QUICKSORT - VISUALIZACIÓN INTERACTIVA",
            font=("Segoe UI", 14, "bold"), bg="#0f172a", fg="#f8fafc"
        ).pack(pady=(12, 4))

        self.lbl_estado = tk.Label(
            root, text="Presiona 'Ingresar Números' para comenzar",
            font=("Segoe UI", 10), bg="#0f172a", fg="#94a3b8"
        )
        self.lbl_estado.pack(pady=(0, 8))

        self.canvas = tk.Canvas(root, width=700, height=310, bg="#1e293b", highlightthickness=0)
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

        w, h = 700, 310
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
        self.root.after(600, self.ejecutar_quicksort)

    def particionar(self, inicio, fin):
        pivote = self.datos[fin]
        i = inicio - 1
        for j in range(inicio, fin):
            colores = ["#38bdf8"] * len(self.datos)
            for k in range(inicio, fin + 1):
                colores[k] = "#6366f1"
            colores[fin] = "#a855f7"  # Pivote en morado
            colores[j] = "#facc15"    # Elemento evaluado en amarillo
            self.lbl_estado.config(text=f"Rango [{inicio}..{fin}] | Pivote = {pivote} | Evaluando {self.datos[j]}")
            self.dibujar_barras(colores)
            self.root.after(400)

            if self.datos[j] <= pivote:
                i += 1
                if i != j:
                    self.datos[i], self.datos[j] = self.datos[j], self.datos[i]
                    colores[i] = "#f43f5e"
                    colores[j] = "#f43f5e"
                    self.dibujar_barras(colores)
                    self.root.after(400)

        self.datos[i + 1], self.datos[fin] = self.datos[fin], self.datos[i + 1]
        colores = ["#38bdf8"] * len(self.datos)
        colores[i + 1] = "#22c55e"
        self.lbl_estado.config(text=f"Pivote {pivote} fijado en índice [{i + 1}]")
        self.dibujar_barras(colores)
        self.root.after(450)
        return i + 1

    def _quicksort_rec(self, inicio, fin):
        if inicio < fin:
            p = self.particionar(inicio, fin)
            self._quicksort_rec(inicio, p - 1)
            self._quicksort_rec(p + 1, fin)

    def ejecutar_quicksort(self):
        self._quicksort_rec(0, len(self.datos) - 1)
        self.dibujar_barras(["#22c55e"] * len(self.datos))
        self.lbl_estado.config(text=f"¡Ordenado con Quicksort!: {self.datos}")
        self.ordenando = False
        self.btn_ingresar.config(state="normal")


if __name__ == "__main__":
    root = tk.Tk()
    app = QuickSortApp(root)
    root.mainloop()