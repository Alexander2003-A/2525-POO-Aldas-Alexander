# inventario.py — versión simple

class Producto:
    def __init__(self, id_, nombre, cantidad, precio):
        self.set_id(id_); self.set_nombre(nombre)
        self.set_cantidad(cantidad); self.set_precio(precio)

    # getters
    def get_id(self): return self._id
    def get_nombre(self): return self._nombre
    def get_cantidad(self): return self._cantidad
    def get_precio(self): return self._precio

    # setters (validaciones básicas)
    def set_id(self, v):
        if not isinstance(v, int) or v < 0: raise ValueError("ID entero no negativo")
        self._id = v
    def set_nombre(self, v):
        if not isinstance(v, str) or not v.strip(): raise ValueError("Nombre no vacío")
        self._nombre = v.strip()
    def set_cantidad(self, v):
        if not isinstance(v, int) or v < 0: raise ValueError("Cantidad entera ≥ 0")
        self._cantidad = v
    def set_precio(self, v):
        v = float(v)
        if v < 0: raise ValueError("Precio ≥ 0")
        self._precio = v

    def fila(self):
        return f"{self._id:>3} | {self._nombre:<18} | {self._cantidad:>4} | ${self._precio:>7.2f}"


class Inventario:
    def __init__(self): self.items = []  # lista de productos

    def anadir(self, prod):                # ID único
        if any(p.get_id() == prod.get_id() for p in self.items): return False
        self.items.append(prod); return True

    def eliminar_por_id(self, id_):
        for i,p in enumerate(self.items):
            if p.get_id() == id_: del self.items[i]; return True
        return False

    def actualizar_por_id(self, id_, cantidad=None, precio=None):
        p = self.obtener_por_id(id_)
        if not p: return False
        if cantidad is not None: p.set_cantidad(int(cantidad))
        if precio   is not None: p.set_precio(float(precio))
        return True

    def buscar_por_nombre(self, texto):
        t = texto.lower().strip()
        return [p for p in self.items if t in p.get_nombre().lower()]

    def mostrar_todos(self):
        print(" ID | Nombre             | Cant |  Precio")
        print("------------------------------------------")
        if not self.items: print("(inventario vacío)")
        for p in self.items: print(p.fila())

    def obtener_por_id(self, id_):
        for p in self.items:
            if p.get_id() == id_: return p


# -------- Interfaz de consola --------
def leer_int(msg):
    while True:
        try: return int(input(msg))
        except: print("Ingresa un entero válido.")

def leer_float(msg):
    while True:
        try: return float(input(msg))
        except: print("Ingresa un número válido.")

def menu():
    print("""
1) Añadir producto
2) Eliminar por ID
3) Actualizar por ID
4) Buscar por nombre
5) Mostrar todos
0) Salir
""")

def main():
    inv = Inventario()
    # Datos de ejemplo (opcional)
    inv.anadir(Producto(1,"Arroz",10,1.2))
    inv.anadir(Producto(2,"Leche",5,0.9))

    while True:
        menu(); op = input("Opción: ").strip()
        if op=="1":
            pid = leer_int("ID: "); nom = input("Nombre: ")
            cant = leer_int("Cantidad: "); pre = leer_float("Precio: ")
            print("Agregado" if inv.anadir(Producto(pid,nom,cant,pre)) else "ID existente")
        elif op=="2":
            print("Eliminado" if inv.eliminar_por_id(leer_int("ID: ")) else "No existe")
        elif op=="3":
            pid = leer_int("ID: ")
            q = input("Nueva cantidad (vacío = igual): "); p = input("Nuevo precio (vacío = igual): ")
            print("Actualizado" if inv.actualizar_por_id(pid,
                    cantidad=int(q) if q else None,
                    precio=float(p) if p else None) else "No existe")
        elif op=="4":
            for p in inv.buscar_por_nombre(input("Texto a buscar: ")): print(p.fila())
        elif op=="5":
            inv.mostrar_todos()
        elif op=="0":
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()
