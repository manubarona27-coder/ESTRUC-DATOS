import sys
import time

# --- 1. CLASE STACK (PILA) EXPLÍCITA ---
class Stack:
    def __init__(self, nombre):
        self.nombre = nombre
        self.items = []

    def push(self, item):
        """Agrega un elemento a la cima de la pila"""
        self.items.append(item)

    def pop(self):
        """Saca y devuelve el elemento de la cima"""
        if not self.is_empty():
            return self.items.pop()
        return None

    def peek(self):
        """Mira el elemento de la cima sin sacarlo"""
        if not self.is_empty():
            return self.items[-1]
        return None

    def is_empty(self):
        """Verifica si la pila está vacía"""
        return len(self.items) == 0

    def size(self):
        """Devuelve el número de elementos en la pila"""
        return len(self.items)


# --- 2. INTERFAZ GRÁFICA Y SIMULACIÓN CON STACKS ---
try:
    import tkinter as tk
    from tkinter import messagebox, ttk
except ImportError:
    print("Error: Se requiere la librería tkinter.")
    sys.exit(1)

class TorresDeHanoiGrafica:
    def __init__(self, root):
        self.root = root
        self.root.title("Torres de Hanói con Clases Stack - Modo Gráfico")
        self.root.geometry("750x600")
        self.root.config(bg="#f4f6f7")

        # Configuración de los Postes usando la clase Stack
        self.poste_A = Stack("Origen")
        self.poste_B = Stack("Auxiliar")
        self.poste_C = Stack("Destino")

        self.animando = False
        self.movimientos_lista = []

        self.crear_interfaz()

    def crear_interfaz(self):
        # Título
        titulo = tk.Label(self.root, text="Torres de Hanói (Estructura de Datos: PILA / STACK)", font=("Arial", 14, "bold"), bg="#f4f6f7", fg="#2c3e50")
        titulo.pack(pady=10)

        # Controles superiores
        marco_controles = tk.Frame(self.root, bg="#f4f6f7")
        marco_controles.pack(pady=5)

        tk.Label(marco_controles, text="Número de Discos (3 a 64):", font=("Arial", 10, "bold"), bg="#f4f6f7").pack(side=tk.LEFT, padx=5)
        
        # Permitimos elegir hasta 64 discos en el spinbox
        self.spin_discos = ttk.Spinbox(marco_controles, from_=3, to=64, width=5, font=("Arial", 10))
        self.spin_discos.set(4) # Por defecto 4 discos para animar
        self.spin_discos.pack(side=tk.LEFT, padx=5)

        self.btn_iniciar = tk.Button(marco_controles, text="Iniciar Simulación", command=self.iniciar_simulacion, bg="#27ae60", fg="white", font=("Arial", 10, "bold"))
        self.btn_iniciar.pack(side=tk.LEFT, padx=10)

        self.btn_reiniciar = tk.Button(marco_controles, text="Reiniciar", command=self.reiniciar_juego, bg="#c0392b", fg="white", font=("Arial", 10, "bold"))
        self.btn_reiniciar.pack(side=tk.LEFT, padx=5)

        # Contador de movimientos / Mensajes
        self.lbl_contador = tk.Label(self.root, text="Movimientos: 0", font=("Arial", 11, "bold"), bg="#f4f6f7", fg="#34495e")
        self.lbl_contador.pack(pady=5)

        # Lienzo (Canvas) para dibujar los postes y discos
        self.canvas_width = 700
        self.canvas_height = 380
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="white", highlightthickness=2, highlightbackground="#bdc3c7")
        self.canvas.pack(pady=10)

        self.reiniciar_juego()

    def reiniciar_juego(self):
        if self.animando:
            return

        # Vaciar los Stacks
        self.poste_A.items.clear()
        self.poste_B.items.clear()
        self.poste_C.items.clear()

        # Obtener número de discos seleccionado
        try:
            self.num_discos = int(self.spin_discos.get())
        except ValueError:
            self.num_discos = 4

        # Validación si excede el límite visual de animación
        if self.num_discos > 10:
            self.lbl_contador.config(text=f"Modo Teórico Activado para {self.num_discos} discos.")
            self.actualizar_dibujo_vacio()
            return

        # Llenar el poste de Origen (Stack A) con los discos
        for i in range(self.num_discos, 0, -1):
            self.poste_A.push(i)

        self.contador_movs = 0
        self.lbl_contador.config(text="Movimientos: 0")
        self.actualizar_dibujo()

    def actualizar_dibujo_vacio(self):
        self.canvas.delete("all")
        postes_x = {"A": 150, "B": 375, "C": 600}
        self.canvas.create_rectangle(50, 340, 650, 355, fill="#7f8c8d")
        for x in postes_x.values():
            self.canvas.create_rectangle(x - 6, 120, x + 6, 340, fill="#95a5a6")
        self.canvas.create_text(150, 365, text="Poste A (Origen)", font=("Arial", 10, "bold"), fill="#2c3e50")
        self.canvas.create_text(375, 365, text="Poste B (Auxiliar)", font=("Arial", 10, "bold"), fill="#2c3e50")
        self.canvas.create_text(600, 365, text="Poste C (Destino)", font=("Arial", 10, "bold"), fill="#2c3e50")
        
        # Mensaje en el canvas
        self.canvas.create_text(350, 200, text=f"⚠️ Demasiados discos ({self.num_discos}) para animación gráfica.\nUsa el botón de simulación para ver el cálculo teórico.", font=("Arial", 12, "bold"), fill="#c0392b", justify="center")

    def actualizar_dibujo(self):
        self.canvas.delete("all")

        postes_x = {"A": 150, "B": 375, "C": 600}

        self.canvas.create_rectangle(50, 340, 650, 355, fill="#7f8c8d")
        for x in postes_x.values():
            self.canvas.create_rectangle(x - 6, 120, x + 6, 340, fill="#95a5a6")

        self.canvas.create_text(150, 365, text="Poste A (Origen)", font=("Arial", 10, "bold"), fill="#2c3e50")
        self.canvas.create_text(375, 365, text="Poste B (Auxiliar)", font=("Arial", 10, "bold"), fill="#2c3e50")
        self.canvas.create_text(600, 365, text="Poste C (Destino)", font=("Arial", 10, "bold"), fill="#2c3e50")

        colores = ["#e74c3c", "#e67e22", "#f1c40f", "#2ecc71", "#3498db", "#9b59b6", "#1abc9c"]
        mapping = [("A", self.poste_A), ("B", self.poste_B), ("C", self.poste_C)]

        for nombre_poste, stack in mapping:
            x_centro = postes_x[nombre_poste]
            for index, tamano_disco in enumerate(stack.items):
                ancho = max(15, 30 + (tamano_disco * 15))
                alto = 20
                y_pos = 335 - (index * (alto + 2))
                x1 = x_centro - (ancho / 2)
                x2 = x_centro + (ancho / 2)
                y1 = y_pos - alto
                y2 = y_pos

                color = colores[(tamano_disco - 1) % len(colores)]
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#2c3e50", width=2)
                if self.num_discos <= 7:
                    self.canvas.create_text(x_centro, y1 + (alto / 2), text=str(tamano_disco), font=("Arial", 8, "bold"), fill="white")

    def iniciar_simulacion(self):
        if self.animando:
            return

        try:
            self.num_discos = int(self.spin_discos.get())
        except ValueError:
            self.num_discos = 4

        # VALIDACIÓN PARA 64 DISCOS (O NÚMEROS GRANDES)
        if self.num_discos > 64:
            movimientos_teoricos = (2**self.num_discos) - 1
            mensaje = (
                f"⚠️ ¡Imposible realizar la animación física con {self.num_discos} discos!\n\n"
                f"• Movimientos teóricos necesarios: {movimientos_teoricos:,}\n"
                f"• Tiempo estimado de simulación: Físicamente imposible.\n\n"
                f"A una velocidad de 1 movimiento por segundo, tardaría más de "
                f"584 mil millones de años en completarse."
            )
            messagebox.showwarning("Límite Físico Superado", mensaje)
            return

        self.reiniciar_juego()
        self.animando = True
        self.spin_discos.config(state="disabled")
        self.btn_iniciar.config(state="disabled")
        self.btn_reiniciar.config(state="disabled")

        self.movimientos_lista = []
        self.hanoi_generar_movimientos(self.num_discos, self.poste_A, self.poste_C, self.poste_B)
        self.ejecutar_siguiente_movimiento()

    def hanoi_generar_movimientos(self, n, origen, destino, auxiliar):
        if n == 1:
            self.movimientos_lista.append((origen, destino))
            return
        
        self.hanoi_generar_movimientos(n - 1, origen, auxiliar, destino)
        self.movimientos_lista.append((origen, destino))
        self.hanoi_generar_movimientos(n - 1, auxiliar, destino, origen)

    def ejecutar_siguiente_movimiento(self):
        if self.movimientos_lista:
            origen, destino = self.movimientos_lista.pop(0)
            
            # Operación con la clase Stack
            disco = origen.pop()
            if disco is not None:
                destino.push(disco)
            
            self.contador_movs += 1
            self.lbl_contador.config(text=f"Movimientos: {self.contador_movs}")
            
            self.actualizar_dibujo()
            self.root.after(400, self.ejecutar_siguiente_movimiento)
        else:
            self.animando = False
            self.spin_discos.config(state="normal")
            self.btn_iniciar.config(state="normal")
            self.btn_reiniciar.config(state="normal")
            messagebox.showinfo("¡Completado!", f"¡Torre de Hanói resuelta con éxito en {self.contador_movs} movimientos usando Stacks!")


if __name__ == "__main__":
    root = tk.Tk()
    app = TorresDeHanoiGrafica(root)
    root.mainloop()