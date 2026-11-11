import tkinter as tk
from tkinter import messagebox

# ==========================================
# ESTRUCTURAS DE DATOS
# ==========================================

class NodoIngrediente:
    def __init__(self, nombre):
        self.nombre = nombre
        self.siguiente = None  # Puntero al siguiente (NIL por defecto)

class ListaEnlazadaIngredientes:
    def __init__(self):
        self.cabeza = None

    def agregar(self, nombre):
        nuevo_nodo = NodoIngrediente(nombre)
        if not self.cabeza:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo

    def eliminar(self, nombre):
        actual = self.cabeza
        previo = None
        
        # Buscar el nodo
        while actual and actual.nombre.lower() != nombre.lower():
            previo = actual
            actual = actual.siguiente
            
        if not actual:
            return False # No se encontró el ingrediente
            
        # Desconectar el nodo
        if not previo: # Era el primer nodo (cabeza)
            self.cabeza = actual.siguiente
        else:
            previo.siguiente = actual.siguiente
        return True

    def obtener_todos(self):
        ingredientes = []
        actual = self.cabeza
        while actual:
            ingredientes.append(actual.nombre)
            actual = actual.siguiente
        return ingredientes

    def eliminar_duplicados(self):
        # Ejercicio 2: Limpieza de repetidos en la lista enlazada
        if not self.cabeza:
            return 0
            
        vistos = set([self.cabeza.nombre.lower()])
        actual = self.cabeza
        eliminados = 0
        
        while actual.siguiente:
            if actual.siguiente.nombre.lower() in vistos:
                # Saltarse el nodo duplicado (eliminar)
                actual.siguiente = actual.siguiente.siguiente
                eliminados += 1
            else:
                vistos.add(actual.siguiente.nombre.lower())
                actual = actual.siguiente
        return eliminados

class Postre:
    def __init__(self, nombre):
        self.nombre = nombre
        self.ingredientes = ListaEnlazadaIngredientes()

# ==========================================
# INTERFAZ GRÁFICA (GUI)
# ==========================================

class AppRecetario:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Postres e Ingredientes")
        self.root.geometry("600x450")
        
        self.arreglo_postres = [] # Arreglo principal
        self.postre_seleccionado = None

        self.crear_interfaz()

    def crear_interfaz(self):
        # Paneles
        panel_izq = tk.Frame(self.root, padx=10, pady=10)
        panel_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        panel_der = tk.Frame(self.root, padx=10, pady=10)
        panel_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # --- SECCIÓN POSTRES (Arreglo) ---
        tk.Label(panel_izq, text="Arreglo de POSTRES", font=("Arial", 10, "bold")).pack()
        self.listbox_postres = tk.Listbox(panel_izq, height=10)
        self.listbox_postres.pack(fill=tk.BOTH, expand=True, pady=5)
        self.listbox_postres.bind('<<ListboxSelect>>', self.seleccionar_postre)

        self.entry_postre = tk.Entry(panel_izq)
        self.entry_postre.pack(fill=tk.X, pady=2)

        tk.Button(panel_izq, text="d) Alta Postre", command=self.alta_postre).pack(fill=tk.X, pady=2)
        tk.Button(panel_izq, text="e) Baja Postre", command=self.baja_postre).pack(fill=tk.X, pady=2)
        tk.Button(panel_izq, text="2) Limpiar Duplicados Globales", command=self.limpiar_duplicados_global).pack(fill=tk.X, pady=10)

        # --- SECCIÓN INGREDIENTES (Lista Enlazada) ---
        tk.Label(panel_der, text="Lista de INGREDIENTES", font=("Arial", 10, "bold")).pack()
        self.lbl_postre_actual = tk.Label(panel_der, text="Seleccione un postre...", fg="blue")
        self.lbl_postre_actual.pack()
        
        self.listbox_ingredientes = tk.Listbox(panel_der, height=10)
        self.listbox_ingredientes.pack(fill=tk.BOTH, expand=True, pady=5)

        self.entry_ingrediente = tk.Entry(panel_der)
        self.entry_ingrediente.pack(fill=tk.X, pady=2)

        tk.Button(panel_der, text="b) Insertar Ingrediente", command=self.insertar_ingrediente).pack(fill=tk.X, pady=2)
        tk.Button(panel_der, text="c) Eliminar Ingrediente", command=self.eliminar_ingrediente).pack(fill=tk.X, pady=2)

    # --- LÓGICA DE OPERACIONES ---

    def buscar_postre(self, nombre):
        for p in self.arreglo_postres:
            if p.nombre.lower() == nombre.lower():
                return p
        return None

    def actualizar_lista_postres(self):
        # Garantizar orden alfabético del arreglo antes de mostrar
        self.arreglo_postres.sort(key=lambda x: x.nombre.lower())
        self.listbox_postres.delete(0, tk.END)
        for p in self.arreglo_postres:
            self.listbox_postres.insert(tk.END, p.nombre)

    def seleccionar_postre(self, event):
        seleccion = self.listbox_postres.curselection()
        if seleccion:
            nombre_postre = self.listbox_postres.get(seleccion[0])
            self.postre_seleccionado = self.buscar_postre(nombre_postre)
            self.lbl_postre_actual.config(text=f"Ingredientes de: {self.postre_seleccionado.nombre}")
            self.mostrar_ingredientes() # a) Imprimir ingredientes

    def mostrar_ingredientes(self):
        # a) Dado un postre, imprimir lista de ingredientes
        self.listbox_ingredientes.delete(0, tk.END)
        if self.postre_seleccionado:
            ingredientes = self.postre_seleccionado.ingredientes.obtener_todos()
            for ing in ingredientes:
                self.listbox_ingredientes.insert(tk.END, ing)

    def alta_postre(self):
        # d) Alta de un postre
        nombre = self.entry_postre.get().strip()
        if not nombre:
            messagebox.showwarning("Error", "Ingrese un nombre de postre.")
            return
        if self.buscar_postre(nombre):
            messagebox.showwarning("Error", "Este postre ya existe.")
            return
        
        nuevo_postre = Postre(nombre)
        self.arreglo_postres.append(nuevo_postre)
        self.entry_postre.delete(0, tk.END)
        self.actualizar_lista_postres()
        messagebox.showinfo("Éxito", f"Postre '{nombre}' dado de alta y ordenado.")

    def baja_postre(self):
        # e) Baja de un postre
        seleccion = self.listbox_postres.curselection()
        if not seleccion:
            messagebox.showwarning("Error", "Seleccione un postre de la lista para dar de baja.")
            return
            
        nombre = self.listbox_postres.get(seleccion[0])
        postre = self.buscar_postre(nombre)
        
        # Eliminar del arreglo
        self.arreglo_postres.remove(postre)
        # (En Python, la memoria de la lista enlazada interna se libera automáticamente)
        
        self.postre_seleccionado = None
        self.lbl_postre_actual.config(text="Seleccione un postre...")
        self.listbox_ingredientes.delete(0, tk.END)
        self.actualizar_lista_postres()
        messagebox.showinfo("Éxito", f"Postre '{nombre}' y sus ingredientes eliminados.")

    def insertar_ingrediente(self):
        # b) Insertar nuevos ingredientes
        if not self.postre_seleccionado:
            messagebox.showwarning("Error", "Seleccione un postre primero.")
            return
            
        ingrediente = self.entry_ingrediente.get().strip()
        if not ingrediente:
            messagebox.showwarning("Error", "Ingrese un nombre de ingrediente.")
            return
            
        self.postre_seleccionado.ingredientes.agregar(ingrediente)
        self.entry_ingrediente.delete(0, tk.END)
        self.mostrar_ingredientes()

    def eliminar_ingrediente(self):
        # c) Eliminar ingrediente
        if not self.postre_seleccionado:
            messagebox.showwarning("Error", "Seleccione un postre primero.")
            return
            
        ingrediente = self.entry_ingrediente.get().strip()
        if not ingrediente:
            # Si no escribió nada, intentar tomar el seleccionado de la lista
            seleccion = self.listbox_ingredientes.curselection()
            if seleccion:
                ingrediente = self.listbox_ingredientes.get(seleccion[0])
            else:
                messagebox.showwarning("Error", "Escriba o seleccione un ingrediente para eliminar.")
                return

        exito = self.postre_seleccionado.ingredientes.eliminar(ingrediente)
        if exito:
            self.entry_ingrediente.delete(0, tk.END)
            self.mostrar_ingredientes()
        else:
            messagebox.showerror("Error", f"El ingrediente '{ingrediente}' no se encontró en este postre.")

    def limpiar_duplicados_global(self):
        # 2. Subprograma que elimina repetidos de la estructura POSTRES
        total_eliminados = 0
        for postre in self.arreglo_postres:
            eliminados_aqui = postre.ingredientes.eliminar_duplicados()
            total_eliminados += eliminados_aqui
            
        self.mostrar_ingredientes() # Refrescar la vista actual por si acaso
        messagebox.showinfo("Limpieza Completada", f"Se eliminaron {total_eliminados} ingredientes repetidos en todo el recetario.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppRecetario(root)
    root.mainloop()