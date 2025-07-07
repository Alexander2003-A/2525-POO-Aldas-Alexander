# Programa que calcula el área de un círculo
# Autor: Alexander Aldas
# Fecha: 28-06-2025

import math

def calcular_area_circulo(radio):
    """
    Calcula el área de un círculo usando la fórmula: área = π * r^2
    :param radio: float
    :return: float
    """
    area = math.pi * radio ** 2
    return area

# Solicita el radio al usuario
radio_usuario = float(input("Ingrese el radio del círculo: "))

# Calcula el área
area_resultado = calcular_area_circulo(radio_usuario)

# Muestra el resultado
print("El área del círculo es:", area_resultado)    