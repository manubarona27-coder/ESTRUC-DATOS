"""
ADA2 - Colas
Sistema de turnos para una compañía de seguros (Python + Tkinter).

Comandos (se escriben en el cuadro de texto o se usan los botones):
    C <letra>            -> Llega un cliente al servicio indicado. Ej: C P
    A <letra><número>    -> Atiende a ese cliente.            Ej: A P1
"""

import re
import tkinter as tk
from tkinter import ttk, messagebox


# ----------------------------------------------------------------------
# Clase Cola (FIFO)
# ----------------------------------------------------------------------
class Cola:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("La cola está vacía")
        return self.items.pop(0)

    def front(self):
        if self.is_empty():
            return None
        return self.items[0]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def to_list(self):
        return list(self.items)


# ----------------------------------------------------------------------
# Servicios de la aseguradora: letra clave -> nombre
# ----------------------------------------------------------------------
SERVICIOS = {
    "P": "Pólizas nuevas",
    "S": "Siniestros",
    "G": "Pagos",
    "R": "Renovaciones",
    "Q": "Quejas y aclaraciones",
}


# ----------------------------------------------------------------------
# Lógica del sistema (independiente de la interfaz)
# ----------------------------------------------------------------------
class SistemaTurnos:
    def __init__(self):
        self.colas = {letra: Cola() for letra in SERVICIOS}
        self.contadores = {letra: 0 for letra in SERVICIOS}

    def nuevo_cliente(self, letra):
        """Genera un turno y lo guarda solo en la cola de ese servicio."""
        self.contadores[letra] += 1
        numero = self.contadores[letra]
        self.colas[letra].enqueue(numero)
        return f"{letra}{numero}"

    def atender(self, letra, numero):
        """Atiende al cliente indicado. Debe ser el primero de la cola."""
        cola = self.colas[letra]
        if cola.is_empty():
            raise ValueError(f"No hay clientes en espera en {SERVICIOS[letra]}.")
        if cola.front() != numero:
            raise ValueError(
                f"El turno {letra}{numero} no es el siguiente. "
                f"Le toca a {letra}{cola.front()}."
            )
        return f"{letra}{cola.dequeue()}"

    def atender_siguiente(self, letra):
        cola = self.colas[letra]
        if cola.is_empty():
            raise ValueError(f"No hay clientes en espera en {SERVICIOS[letra]}.")
        return f"{letra}{cola.dequeue()}"


# ----------------------------------------------------------------------
# Interfaz gráfica
# ----------------------------------------------------------------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aseguradora - Sistema de turnos")
        self.geometry("1000x640")
        self.minsize(900, 560)
        self.configure(bg="#f4f6fa")

        self.sistema = SistemaTurnos()
        self.listas = {}
        self.etiquetas_total = {}

        self._crear_estilos()
        self._crear_widgets()

    # ---------- estilos ----------
    def _crear_estilos(self):
        estilo = ttk.Style(self)
        estilo.theme_use("clam")
        estilo.configure("TFrame", background="#f4f6fa")
        estilo.configure("Card.TLabelframe", background="#ffffff")
        estilo.configure("Card.TLabelframe.Label", background="#ffffff",
                         font=("Segoe UI", 11, "bold"), foreground="#1f3a5f")
        estilo.configure("Accent.TButton", font=("Segoe UI", 10, "bold"),
                         padding=6)

    # ---------- widgets ----------
    def _crear_widgets(self):
        # Título
        tk.Label(self, text="Sistema de turnos - Compañía de seguros",
                 font=("Segoe UI", 18, "bold"), bg="#1f3a5f", fg="white",
                 pady=10).pack(fill="x")

        cuerpo = ttk.Frame(self, padding=10)
        cuerpo.pack(fill="both", expand=True)
        cuerpo.columnconfigure(0, weight=3)
        cuerpo.columnconfigure(1, weight=2)
        cuerpo.rowconfigure(0, weight=1)

        # ----- Columna izquierda: colas por servicio -----
        izq = ttk.Frame(cuerpo)
        izq.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        izq.rowconfigure(0, weight=1)
        for i in range(len(SERVICIOS)):
            izq.columnconfigure(i, weight=1)

        for col, (letra, nombre) in enumerate(SERVICIOS.items()):
            marco = ttk.LabelFrame(izq, text=f"{letra} · {nombre}",
                                   style="Card.TLabelframe", padding=6)
            marco.grid(row=0, column=col, sticky="nsew", padx=3)
            marco.rowconfigure(0, weight=1)
            marco.columnconfigure(0, weight=1)

            lista = tk.Listbox(marco, font=("Consolas", 12), height=12,
                               width=8, activestyle="none",
                               selectbackground="#dbe7f7",
                               selectforeground="black", relief="flat",
                               highlightthickness=1,
                               highlightbackground="#cfd8e6")
            lista.grid(row=0, column=0, sticky="nsew")
            self.listas[letra] = lista

            total = tk.Label(marco, text="En espera: 0", bg="#ffffff",
                             fg="#555", font=("Segoe UI", 9))
            total.grid(row=1, column=0, pady=(4, 2))
            self.etiquetas_total[letra] = total

            ttk.Button(marco, text="Nuevo cliente", style="Accent.TButton",
                       command=lambda l=letra: self.nuevo_cliente(l)
                       ).grid(row=2, column=0, sticky="ew", pady=2)
            ttk.Button(marco, text="Llamar siguiente",
                       command=lambda l=letra: self.llamar_siguiente(l)
                       ).grid(row=3, column=0, sticky="ew", pady=2)

        # ----- Columna derecha: consola de comandos -----
        der = ttk.Frame(cuerpo)
        der.grid(row=0, column=1, sticky="nsew")
        der.columnconfigure(0, weight=1)
        der.rowconfigure(3, weight=1)

        # Pantalla "llamando"
        pantalla = tk.Frame(der, bg="#1f3a5f", padx=10, pady=10)
        pantalla.grid(row=0, column=0, sticky="ew")
        tk.Label(pantalla, text="LLAMANDO AL TURNO", bg="#1f3a5f",
                 fg="#9fb8d9", font=("Segoe UI", 10, "bold")).pack()
        self.lbl_llamando = tk.Label(pantalla, text="—", bg="#1f3a5f",
                                     fg="white", font=("Segoe UI", 40, "bold"))
        self.lbl_llamando.pack()
        self.lbl_servicio = tk.Label(pantalla, text="", bg="#1f3a5f",
                                     fg="#9fb8d9", font=("Segoe UI", 10))
        self.lbl_servicio.pack()

        # Entrada de comandos
        cmd = ttk.LabelFrame(der, text="Comando", style="Card.TLabelframe",
                             padding=8)
        cmd.grid(row=1, column=0, sticky="ew", pady=10)
        cmd.columnconfigure(0, weight=1)
        self.entrada = ttk.Entry(cmd, font=("Consolas", 13))
        self.entrada.grid(row=0, column=0, sticky="ew", padx=(0, 6))
        self.entrada.bind("<Return>", lambda e: self.ejecutar_comando())
        self.entrada.focus()
        ttk.Button(cmd, text="Enviar", style="Accent.TButton",
                   command=self.ejecutar_comando).grid(row=0, column=1)

        ayuda = ("C P  → llega un cliente a Pólizas\n"
                 "A P1 → atender al turno P1")
        tk.Label(cmd, text=ayuda, justify="left", bg="#ffffff", fg="#555",
                 font=("Consolas", 9)).grid(row=1, column=0, columnspan=2,
                                            sticky="w", pady=(6, 0))

        # Leyenda de servicios
        leyenda = "  ".join(f"{l}={n}" for l, n in SERVICIOS.items())
        tk.Label(der, text=leyenda, wraplength=380, justify="left",
                 bg="#f4f6fa", fg="#555", font=("Segoe UI", 9)
                 ).grid(row=2, column=0, sticky="w")

        # Bitácora
        bit = ttk.LabelFrame(der, text="Bitácora", style="Card.TLabelframe",
                             padding=6)
        bit.grid(row=3, column=0, sticky="nsew", pady=(10, 0))
        bit.rowconfigure(0, weight=1)
        bit.columnconfigure(0, weight=1)
        self.log = tk.Text(bit, height=8, font=("Consolas", 10),
                           state="disabled", relief="flat", bg="#fafbfd")
        self.log.grid(row=0, column=0, sticky="nsew")

    # ---------- acciones ----------
    def nuevo_cliente(self, letra):
        turno = self.sistema.nuevo_cliente(letra)
        self.escribir_log(f"Cliente nuevo en {SERVICIOS[letra]} → turno {turno}")
        self.actualizar_colas()
        messagebox.showinfo("Turno asignado",
                            f"Su turno es: {turno}\nServicio: {SERVICIOS[letra]}")

    def llamar_siguiente(self, letra):
        try:
            turno = self.sistema.atender_siguiente(letra)
        except ValueError as e:
            messagebox.showwarning("Sin clientes", str(e))
            return
        self.mostrar_llamado(letra, turno)

    def ejecutar_comando(self):
        texto = self.entrada.get().strip().upper()
        self.entrada.delete(0, "end")
        if not texto:
            return

        # C <letra>  -> nuevo cliente
        m = re.fullmatch(r"C\s*([A-Z])", texto)
        if m:
            letra = m.group(1)
            if letra not in SERVICIOS:
                return self.error(f"El servicio '{letra}' no existe.")
            return self.nuevo_cliente(letra)

        # A <letra><número>  -> atender
        m = re.fullmatch(r"A\s*([A-Z])\s*(\d+)", texto)
        if m:
            letra, numero = m.group(1), int(m.group(2))
            if letra not in SERVICIOS:
                return self.error(f"El servicio '{letra}' no existe.")
            try:
                turno = self.sistema.atender(letra, numero)
            except ValueError as e:
                return self.error(str(e))
            return self.mostrar_llamado(letra, turno)

        self.error("Comando no válido. Usa 'C P' para llegada o 'A P1' para atender.")

    def mostrar_llamado(self, letra, turno):
        self.lbl_llamando.config(text=turno)
        self.lbl_servicio.config(text=SERVICIOS[letra])
        self.escribir_log(f"Llamando al turno {turno} ({SERVICIOS[letra]})")
        self.actualizar_colas()

    def error(self, mensaje):
        self.escribir_log(f"⚠ {mensaje}")
        messagebox.showwarning("Aviso", mensaje)

    # ---------- refresco de la interfaz ----------
    def actualizar_colas(self):
        for letra, cola in self.sistema.colas.items():
            lista = self.listas[letra]
            lista.delete(0, "end")
            for n in cola.to_list():
                lista.insert("end", f"{letra}{n}")
            self.etiquetas_total[letra].config(
                text=f"En espera: {cola.size()}")

    def escribir_log(self, texto):
        self.log.config(state="normal")
        self.log.insert("end", texto + "\n")
        self.log.see("end")
        self.log.config(state="disabled")


if __name__ == "__main__":
    App().mainloop()