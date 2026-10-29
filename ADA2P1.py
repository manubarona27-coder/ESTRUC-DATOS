"""
ADA2 - Colas | Problema 1
Suma de dos colas elemento por elemento.
Acepta: positivos, negativos, ceros, decimales y números muy grandes.
No acepta letras ni símbolos raros.
"""

import re
from decimal import Decimal, getcontext

# Precisión muy alta para que los números enormes se sumen sin perder dígitos
getcontext().prec = 10000

# Formato válido: signo opcional, dígitos, y parte decimal opcional (. o ,)
PATRON_NUMERO = re.compile(r"[+-]?(\d+([.,]\d+)?|[.,]\d+)")


class Cola:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        return self.items.pop(0)

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def to_list(self):
        return list(self.items)


def sumar_colas(cola_a, cola_b):
    """Recibe 2 colas de números y devuelve una nueva cola con los
    elementos sumados uno a uno. Si una cola es más corta, se toma 0."""
    resultado = Cola()
    while not cola_a.is_empty() or not cola_b.is_empty():
        a = cola_a.dequeue() if not cola_a.is_empty() else Decimal(0)
        b = cola_b.dequeue() if not cola_b.is_empty() else Decimal(0)
        resultado.enqueue(a + b)
    return resultado


def formatear(numero):
    """Convierte un Decimal a texto normal (sin notación científica)."""
    if numero == 0:
        return "0"
    return format(numero.normalize(), "f")


def pedir_numero(mensaje):
    """Pide un dato hasta que sea un número válido (entero o decimal,
    positivo o negativo). Acepta coma o punto como separador decimal."""
    while True:
        texto = input(mensaje).strip()
        if PATRON_NUMERO.fullmatch(texto):
            return Decimal(texto.replace(",", "."))
        print("  ❌ Solo se aceptan números (ej: 5, -3, 0, 2.75, -0.5). "
              "Intenta de nuevo.")


def pedir_cantidad(mensaje):
    """Pide un entero positivo para el tamaño de las colas."""
    while True:
        texto = input(mensaje).strip()
        if texto.isdigit() and int(texto) > 0:
            return int(texto)
        print("  ❌ Escribe un entero mayor que 0.")


def llenar_cola(nombre, cantidad):
    cola = Cola()
    for i in range(1, cantidad + 1):
        cola.enqueue(pedir_numero(f"  {nombre} - elemento {i}: "))
    return cola


def main():
    print("=== SUMA DE COLAS ===")
    cantidad = pedir_cantidad("¿Cuántos elementos tendrá cada cola? ")

    print("\nCola A:")
    cola_a = llenar_cola("Cola A", cantidad)
    print("\nCola B:")
    cola_b = llenar_cola("Cola B", cantidad)

    # Copias para mostrarlas, porque sumar_colas vacía las originales
    lista_a = [formatear(x) for x in cola_a.to_list()]
    lista_b = [formatear(x) for x in cola_b.to_list()]

    resultado = sumar_colas(cola_a, cola_b)
    lista_r = [formatear(x) for x in resultado.to_list()]

    # Ancho de columnas según el número más largo
    w_a = max(len("Cola A"), *(len(x) for x in lista_a)) + 3
    w_b = max(len("Cola B"), *(len(x) for x in lista_b)) + 3

    print("\n" + "Cola A".ljust(w_a) + "Cola B".ljust(w_b) + "Cola Resultado")
    for a, b, r in zip(lista_a, lista_b, lista_r):
        print(a.ljust(w_a) + b.ljust(w_b) + r)


if __name__ == "__main__":
    main()