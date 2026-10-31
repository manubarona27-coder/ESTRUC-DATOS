import tkinter as tk
from tkinter import messagebox


# 1. CLASE QUE REPRESENTA UN PEDIDO (Igual que Order.java de la guía)
class Order:

  def __init__(self, customer, qtty):
    self.customer = customer
    self.qtty = qtty

  def __str__(self):
    return f"Cliente: {self.customer} | Cantidad: {self.qtty}"


# 2. CLASE QUE REPRESENTA CADA NODO DE LA LISTA ENLAZADA
class Node:

  def __init__(self, info, next_node=None):
    self.info = info  # Guarda el objeto Order
    self.next = next_node  # Apunta al siguiente nodo


# 3. CLASE QUE IMPLEMENTA LA COLA CON LISTA ENLAZADA
class LinkedQueue:

  def __init__(self):
    self.top = None  # Apunta al inicio de la cola (para extraer)
    self.tail = None  # Apunta al final de la cola (para insertar)
    self._size = 0

  def is_empty(self):
    return self.top is None

  def size(self):
    return self._size

  # Enqueue: Añade un elemento al final de la cola
  def enqueue(self, order):
    new_node = Node(order)
    if self.is_empty():
      self.top = new_node
      self.tail = new_node
    else:
      self.tail.next = new_node
      self.tail = new_node
    self._size += 1

  # Dequeue: Extrae el primer elemento de la cola
  def dequeue(self):
    if self.is_empty():
      return None
    info = self.top.info
    self.top = self.top.next
    if self.top is None:
      self.tail = None  # Si la cola se quedó vacía, tail también se limpia
    self._size -= 1
    return info

  # Front: Devuelve el primer elemento sin sacarlo
  def front(self):
    if self.is_empty():
      return None
    return self.top.info

  # Método para recorrer la cola y mostrar todos los elementos (como printInfo)
  def get_elements(self):
    elements = []
    current = self.top
    while current:
      elements.append(current.info)
      current = current.next
    return elements


# 4. INTERFAZ GRÁFICA (GUI) CON TKINTER
class QueueApp:

  def __init__(self, root):
    self.root = root
    self.root.title("Simulador de Cola de Pedidos (UC3M)")
    self.root.geometry("480x460")
    self.root.config(bg="#f4f6f9")

    self.queue = LinkedQueue()

    # Título
    title_label = tk.Label(
        root,
        text="Gestión de Pedidos - Cola Enlazada",
        font=("Arial", 14, "bold"),
        bg="#f4f6f9",
        fg="#333",
    )
    title_label.pack(pady=10)

    # Marco de formulario
    form_frame = tk.LabelFrame(
        root, text=" Nuevo Pedido ", font=("Arial", 10, "bold"), bg="#f4f6f9"
    )
    form_frame.pack(fill="x", padx=20, pady=5)

    tk.Label(form_frame, text="Nombre del Cliente:", bg="#f4f6f9").grid(
        row=0, column=0, sticky="w", padx=5, pady=5
    )
    self.cust_entry = tk.Entry(form_frame, width=22)
    self.cust_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Cantidad de producto:", bg="#f4f6f9").grid(
        row=1, column=0, sticky="w", padx=5, pady=5
    )
    self.qtty_entry = tk.Entry(form_frame, width=22)
    self.qtty_entry.grid(row=1, column=1, padx=5, pady=5)

    btn_enqueue = tk.Button(
        form_frame,
        text="Añadir a la Cola (Enqueue)",
        bg="#4CAF50",
        fg="white",
        font=("Arial", 9, "bold"),
        command=self.add_order,
    )
    btn_enqueue.grid(row=2, column=0, columnspan=2, pady=10, sticky="we")

    # Marco de botones de control
    action_frame = tk.Frame(root, bg="#f4f6f9")
    action_frame.pack(fill="x", padx=20, pady=5)

    btn_dequeue = tk.Button(
        action_frame,
        text="Atender Siguiente (Dequeue)",
        bg="#f44336",
        fg="white",
        font=("Arial", 9, "bold"),
        command=self.remove_order,
    )
    btn_dequeue.pack(side="left", expand=True, fill="x", padx=2)

    btn_front = tk.Button(
        action_frame,
        text="Ver Siguiente (Front)",
        bg="#2196F3",
        fg="white",
        font=("Arial", 9, "bold"),
        command=self.show_front,
    )
    btn_front.pack(side="left", expand=True, fill="x", padx=2)

    # Visualizador de la Cola en pantalla
    list_frame = tk.LabelFrame(
        root,
        text=" Estado Actual de la Cola (FIFO) ",
        font=("Arial", 10, "bold"),
        bg="#f4f6f9",
    )
    list_frame.pack(fill="both", expand=True, padx=20, pady=10)

    self.listbox = tk.Listbox(list_frame, font=("Courier", 10), bg="white")
    self.listbox.pack(side="left", fill="both", expand=True, padx=5, pady=5)

    scrollbar = tk.Scrollbar(list_frame, orient="vertical")
    scrollbar.config(command=self.listbox.yview)
    scrollbar.pack(side="right", fill="y")
    self.listbox.config(yscrollcommand=scrollbar.set)

    self.update_display()

  def add_order(self):
    customer = self.cust_entry.get().strip()
    qtty_str = self.qtty_entry.get().strip()

    if not customer or not qtty_str:
      messagebox.showerror("Error", "Por favor completa todos los campos.")
      return

    try:
      qtty = int(qtty_str)
    except ValueError:
      messagebox.showerror("Error", "La cantidad debe ser un número entero.")
      return

    order = Order(customer, qtty)
    self.queue.enqueue(order)
    self.cust_entry.delete(0, tk.END)
    self.qtty_entry.delete(0, tk.END)
    self.update_display()

  def remove_order(self):
    order = self.queue.dequeue()
    if order is None:
      messagebox.showinfo("Cola Vacía", "No hay pedidos pendientes en la cola.")
    else:
      messagebox.showinfo(
          "Pedido Atendido (Dequeue)", f"Se ha procesado el pedido:\n{order}"
      )
      self.update_display()

  def show_front(self):
    order = self.queue.front()
    if order is None:
      messagebox.showinfo("Cola Vacía", "La cola está vacía.")
    else:
      messagebox.showinfo(
          "Siguiente en la Cola (Front)",
          f"El próximo cliente a atender es:\n{order}",
      )

  def update_display(self):
    self.listbox.delete(0, tk.END)
    elements = self.queue.get_elements()
    if not elements:
      self.listbox.insert(tk.END, "[ La cola está vacía actualmente ]")
    else:
      for i, el in enumerate(elements, 1):
        prefix = "-> [TOP] " if i == 1 else f"   [Node {i}] "
        self.listbox.insert(tk.END, f"{prefix} {el}")


if __name__ == "__main__":
  root = tk.Tk()
  app = QueueApp(root)
  root.mainloop()