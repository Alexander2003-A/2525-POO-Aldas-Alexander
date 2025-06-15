# Programa para calcular el promedio semanal de temperatura usando programación tradicional

# Función para ingresar las temperaturas de los 7 días de la semana
def ingresar_temperaturas():
    temperaturas = []
    for i in range(7):
        temp = float(input(f"Ingrese la temperatura del día {i + 1}: "))
        temperaturas.append(temp)  # Agrega cada temperatura a la lista
    return temperaturas

# Función para calcular el promedio de una lista de temperaturas
def calcular_promedio(temperaturas):
    return sum(temperaturas) / len(temperaturas)  # Promedio = suma / cantidad

# Función principal que coordina el flujo del programa
def main():
    print("Cálculo del promedio semanal de temperaturas (Programación Tradicional)")
    temps = ingresar_temperaturas()       # Entrada de datos
    promedio = calcular_promedio(temps)   # Cálculo del promedio
    print(f"El promedio semanal de temperatura es: {promedio:.2f}°C")  # Resultado

# Llamado al programa principal
main()