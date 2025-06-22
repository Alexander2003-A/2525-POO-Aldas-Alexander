# ===================================
# EJEMPLO 1: SISTEMA DE TIENDA ONLINE
# ===================================

class Producto:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

class Carrito:
    def __init__(self):
        self.productos = []

    def agregar_producto(self, producto):
        self.productos.append(producto)

    def calcular_total(self):
        return sum(p.precio for p in self.productos)

class ClienteTienda:
    def __init__(self, nombre):
        self.nombre = nombre
        self.carrito = Carrito()

    def comprar(self):
        total = self.carrito.calcular_total()
        print(f"{self.nombre} debe pagar: ${total}")

# ===================================
# EJEMPLO 2: SISTEMA DE RESERVAS DE HOTEL
# ===================================

class Habitacion:
    def __init__(self, numero, tipo):
        self.numero = numero
        self.tipo = tipo
        self.disponible = True

class Hotel:
    def __init__(self):
        self.habitaciones = [Habitacion(i, "Estándar") for i in range(1, 4)]

    def reservar_habitacion(self, cliente):
        for h in self.habitaciones:
            if h.disponible:
                h.disponible = False
                print(f"Habitación {h.numero} reservada para {cliente.nombre}")
                return
        print("No hay habitaciones disponibles.")

class ClienteHotel:
    def __init__(self, nombre):
        self.nombre = nombre

# ===================================
# EJEMPLO 3: SISTEMA ESCOLAR
# ===================================

class Profesor:
    def __init__(self, nombre):
        self.nombre = nombre

class Curso:
    def __init__(self, nombre, profesor):
        self.nombre = nombre
        self.profesor = profesor

class Estudiante:
    def __init__(self, nombre):
        self.nombre = nombre
        self.cursos = []

    def inscribirse(self, curso):
        self.cursos.append(curso)
        print(f"{self.nombre} se inscribió en {curso.nombre} con {curso.profesor.nombre}")

# ===================================
# PRUEBAS DE CADA EJEMPLO
# ===================================
if __name__ == "__main__":
    print("\n--- TIENDA ---")
    p1 = Producto("Camisa", 25)
    p2 = Producto("Zapatos", 60)
    cliente_tienda = ClienteTienda("Alexander")
    cliente_tienda.carrito.agregar_producto(p1)
    cliente_tienda.carrito.agregar_producto(p2)
    cliente_tienda.comprar()

    print("\n--- HOTEL ---")
    hotel = Hotel()
    cliente_hotel1 = ClienteHotel("Laura")
    cliente_hotel2 = ClienteHotel("Carlos")
    hotel.reservar_habitacion(cliente_hotel1)
    hotel.reservar_habitacion(cliente_hotel2)

    print("\n--- ESCUELA ---")
    prof = Profesor("Srta. Andrade")
    curso = Curso("Programación", prof)
    est = Estudiante("Sofía")
    est.inscribirse(curso)
