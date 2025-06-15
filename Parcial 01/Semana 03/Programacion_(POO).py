# Programa para calcular el promedio semanal de temperatura usando Programación Orientada a Objetos (POO)

# Clase que representa la información climática semanal
class ClimaSemanal:
    def __init__(self):
        # Atributo privado que almacena las temperaturas (encapsulamiento)
        self.__temperaturas = []

    # Metodo para ingresar las temperaturas del usuario
    def ingresar_datos(self):
        for i in range(7):
            temp = float(input(f"Ingrese la temperatura del día {i + 1}: "))
            self.__temperaturas.append(temp)

    # Metodo para calcular el promedio de temperaturas
    def calcular_promedio(self):
        if len(self.__temperaturas) == 0:
            return 0
        return sum(self.__temperaturas) / len(self.__temperaturas)

    # Metodo para mostrar el promedio calculado
    def mostrar_promedio(self):
        promedio = self.calcular_promedio()
        print(f"El promedio semanal de temperatura es: {promedio:.2f}°C")

# Función principal que crea un objeto de la clase y llama a sus métodos
def main():
    print("Cálculo del promedio semanal de temperaturas (POO)")
    clima = ClimaSemanal()   # Crear objeto
    clima.ingresar_datos()   # Llamar metodo para ingresar datos
    clima.mostrar_promedio() # Mostrar promedio

# Llamado al programa principal
main()