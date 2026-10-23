import tkinter as tk
from tkinter import messagebox

def evaluar_expresion():
    expresion = entrada.get().split()
    es_prefija = (tipo_notacion.get() == "prefija")
    pila = []
    
    # Si la notación es prefija, el truco es leer la lista de derecha a izquierda
    if es_prefija:
        expresion.reverse()
        
    try:
        for token in expresion:
            # Si es número, a la pila
            if token.replace('.','',1).isdigit() or (token.startswith('-') and token[1:].isdigit()):
                pila.append(float(token))
                
            # Si es operador, sacamos los últimos dos y operamos
            elif token in ['+', '-', '*', '/']:
                # El orden en que asignamos 'a' y 'b' cambia dependiendo de la notación
                if es_prefija:
                    a = pila.pop()
                    b = pila.pop()
                else: # Posfija
                    b = pila.pop()
                    a = pila.pop()
                    
                if token == '+': pila.append(a + b)
                elif token == '-': pila.append(a - b)
                elif token == '*': pila.append(a * b)
                elif token == '/': pila.append(a / b)
            else:
                raise ValueError("Carácter no válido")
                
        # Mostrar el resultado final
        resultado = pila.pop()
        lbl_resultado.config(text=f"Resultado: {resultado}")
        
    except Exception as e:
        messagebox.showerror("Error", "Expresión inválida. Asegúrate de separar con espacios.")

# --- INTERFAZ GRÁFICA ---
ventana = tk.Tk()
ventana.title("Evaluador Posfijo / Prefijo")
ventana.geometry("350x250")

tk.Label(ventana, text="Introduce la expresión\n(separada por espacios):").pack(pady=5)
entrada = tk.Entry(ventana, width=30, justify="center")
entrada.pack(pady=5)

# Variables y botones para elegir tipo de notación
tipo_notacion = tk.StringVar(value="posfija")
tk.Radiobutton(ventana, text="Posfija (Ej: 3 4 +)", variable=tipo_notacion, value="posfija").pack()
tk.Radiobutton(ventana, text="Prefija (Ej: + 3 4)", variable=tipo_notacion, value="prefija").pack()

tk.Button(ventana, text="Evaluar", command=evaluar_expresion, bg="lightblue").pack(pady=10)

lbl_resultado = tk.Label(ventana, text="Resultado: ", font=("Arial", 12, "bold"))
lbl_resultado.pack()

ventana.mainloop()