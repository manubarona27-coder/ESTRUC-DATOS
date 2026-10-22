import tkinter as tk
from tkinter import messagebox

# --- 1. VARIABLES DE LA PILA ---
pila = []              # Lista que simulará nuestra pila
MAX_CAPACIDAD = 8      # Límite máximo según el ejercicio

# --- 2. FUNCIONES LÓGICAS ---
def actualizar_pantalla():
    """Actualiza los textos en la ventana para mostrar la pila actual y el TOPE"""
    # Invertimos la lista para que el último elemento se vea arriba
    texto_pila = "\n".join(reversed(pila)) if pila else "Pila vacía"
    lbl_pila.config(text=texto_pila)
    
    # Actualizamos el número del TOPE
    lbl_tope.config(text=f"TOPE = {len(pila)}")

def insertar():
    """Función para meter un elemento a la pila (Push)"""
    # Revisamos si hay DESBORDAMIENTO
    if len(pila) >= MAX_CAPACIDAD:
        messagebox.showerror("Error", "¡Desbordamiento! La pila ya tiene 8 elementos.")
    else:
        # Obtenemos la letra de la caja de texto (ej. X, Y, V)
        elemento = entrada.get()
        if elemento != "":
            pila.append(elemento)   # Metemos el elemento a la lista
            entrada.delete(0, tk.END) # Limpiamos la caja de texto
            actualizar_pantalla()

def eliminar():
    """Función para sacar un elemento de la pila (Pop)"""
    # Revisamos si hay SUBDESBORDAMIENTO
    if len(pila) == 0:
        messagebox.showerror("Error", "¡Subdesbordamiento! La pila está vacía.")
    else:
        # Sacamos el elemento que está en la cima (al final de la lista)
        elemento_sacado = pila.pop()
        messagebox.showinfo("Eliminado", f"Se sacó el elemento: {elemento_sacado}")
        actualizar_pantalla()

# --- 3. INTERFAZ GRÁFICA (VENTANA) ---
ventana = tk.Tk()
ventana.title("Simulador de Pila")
ventana.geometry("300x450")

# Controles de entrada e inserción
tk.Label(ventana, text="Letra a insertar (X, Y, V...):").pack(pady=5)
entrada = tk.Entry(ventana, justify="center")
entrada.pack()

tk.Button(ventana, text="Insertar (Push)", bg="lightgreen", command=insertar).pack(pady=10)
tk.Button(ventana, text="Eliminar (Pop)", bg="salmon", command=eliminar).pack(pady=5)

# Etiqueta para mostrar el valor del TOPE
lbl_tope = tk.Label(ventana, text="TOPE = 0", font=("Arial", 14, "bold"))
lbl_tope.pack(pady=10)

# Cuadro visual donde se dibujarán los elementos de la pila
marco = tk.Frame(ventana, bg="white", relief="sunken", bd=2)
marco.pack(fill="both", expand=True, padx=50, pady=10)

lbl_pila = tk.Label(marco, text="Pila vacía", bg="white", font=("Arial", 16, "bold"))
lbl_pila.pack(pady=10)

# Arrancar el programa
ventana.mainloop()