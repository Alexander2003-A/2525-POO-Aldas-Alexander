# Clase base: Vehiculo
class Vehiculo:
    def __init__(self, marca, modelo):
        self.__marca = marca  # atributo privado (encapsulamiento)
        self.__modelo = modelo  # atributo privado (encapsulamiento)

    def obtener_informacion(self):
        return f"Marca: {self.__marca}, Modelo: {self.__modelo}"

    def encender(self):
        return "El vehículo está encendido"

# Clase derivada: Auto (hereda de Vehiculo)
class Auto(Vehiculo):
    def __init__(self, marca, modelo, puertas):
        super().__init__(marca, modelo)
        self.puertas = puertas

    # Método sobrescrito (polimorfismo)
    def encender(self):
        return "El auto está encendido con llave"

# Clase derivada: Moto (hereda de Vehiculo)
class Moto(Vehiculo):
    def __init__(self, marca, modelo, cilindrada):
        super().__init__(marca, modelo)
        self.cilindrada = cilindrada

    # Método sobrescrito (polimorfismo)
    def encender(self):
        return "La moto está encendida con botón"

# Instanciación de objetos y demostración
vehiculos = [
    Auto("Toyota", "Corolla", 4),
    Moto("Yamaha", "FZ", "150cc")
]

for v in vehiculos:
    print(v.obtener_informacion())
    print(v.encender())
    print("-----")
