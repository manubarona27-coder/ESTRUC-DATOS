import tkinter as tk
from tkinter import messagebox
import time

# --- 1. CLASE PILA OBLIGATORIA ---
class Pila:
    def __init__(self, nombre):
        self.items = []
        self.nombre = nombre
        
    def push(self, item):
        self.items.append(item)
        
    def pop(self):
        return self.items.pop() if self.items else None

# --- 2. LÓGICA DE DIBUJO (CANVAS) ---
def dibujar_estado():
    """Limpia el lienzo y redibuja los postes y discos actuales"""
    canvas.delete("all")
    
    # Dibujar la base y los 3 postes (A, B, C)
    canvas.create_rectangle(50, 350, 550, 370, fill="#8B4513") # Base
    posiciones_x = [150, 300, 450]
    for x in posiciones_x:
        canvas.create_rectangle(x - 5, 100, x + 5, 350, fill="gray") # Postes
        
    torres = [torreA, torreB, torreC]
    colores = ["#FF5733", "#33FF57", "#3357FF", "#F033FF", "#33FFF0", "#FFFF33", "#FF8C00", "#FF1493"]
    
    # Recorremos cada pila para dibujar sus discos
    for i, torre in enumerate(torres):
        for nivel, tamano_disco in enumerate(torre.items):
            ancho = tamano_disco * 15  # El disco más grande será más ancho
            x_centro = posiciones_x[i]
            y_abajo = 350 - (nivel * 20) # Apilados hacia arriba
            y_arriba = y_abajo - 20
            color = colores[tamano_disco % len(colores)]
            
            # Dibujar el rectángulo que representa el disco
            canvas.create_rectangle(x_centro - ancho, y_arriba, x_centro + ancho, y_abajo, fill=color, outline="black")
    
    # Actualizar la ventana y pausar medio segundo para crear la animación
    ventana.update()
    time.sleep(0.5)

# --- 3. ALGORITMO RECURSIVO CON PILAS ---
def mover_torre(n, origen, destino, auxiliar):
    if n > 0:
        # Mover n-1 discos al poste auxiliar
        mover_torre(n - 1, origen, auxiliar, destino)
        
        # LÓGICA DE PILA: Sacar el disco físico del origen y meterlo al destino
        disco = origen.pop()
        destino.push(disco)
        dibujar_estado() # Animamos este movimiento específico
        
        # Mover los n-1 discos del auxiliar al destino
        mover_torre(n - 1, auxiliar, destino, origen)

def iniciar_animacion():
    try:
        n_discos = int(entrada_discos.get())
        if n_discos < 1 or n_discos > 8: 
            raise ValueError
    except:
        messagebox.showerror("Error", "Por favor ingresa un número del 1 al 8.")
        return

    # Limpiar las pilas antes de empezar
    torreA.items.clear()
    torreB.items.clear()
    torreC.items.clear()
    
    # Llenar la Torre A con los discos de mayor a menor
    for i in range(n_discos, 0, -1):
        torreA.push(i)
        
    dibujar_estado()
    
    # Bloquear el botón mientras se anima
    btn_iniciar.config(state=tk.DISABLED)
    mover_torre(n_discos, torreA, torreC, torreB)
    btn_iniciar.config(state=tk.NORMAL)
    messagebox.showinfo("Completado", "¡Resolución de Hanoi terminada!")

# --- 4. INTERFAZ GRÁFICA ---
ventana = tk.Tk()
ventana.title("Torres de Hanoi - Resolución Animada")
ventana.geometry("600x450")

# Instanciamos nuestras 3 pilas requeridas
torreA = Pila("A")
torreB = Pila("B")
torreC = Pila("C")

# Panel superior de controles
frame_controles = tk.Frame(ventana)
frame_controles.pack(pady=10)

tk.Label(frame_controles, text="Número de discos (1-8):", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
entrada_discos = tk.Entry(frame_controles, width=5, justify="center")
entrada_discos.insert(0, "3") # Valor por defecto de 3 o más discos
entrada_discos.pack(side=tk.LEFT, padx=5)

btn_iniciar = tk.Button(frame_controles, text="Resolver y Animar", command=iniciar_animacion, bg="lightgreen", font=("Arial", 10, "bold"))
btn_iniciar.pack(side=tk.LEFT, padx=10)

# Lienzo (Canvas) donde se dibujarán las torres
canvas = tk.Canvas(ventana, width=600, height=400, bg="#E8F6F3")
canvas.pack()

# Dibujar el escenario vacío al abrir
dibujar_estado()

ventana.mainloop()