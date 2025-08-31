from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple, Set
import json
import os

# -------------------------------
# Clase Producto
# -------------------------------
@dataclass
class Producto:
    """
    Clase Producto
    - id: Identificador único
    - nombre: Nombre del producto
    - cantidad: Unidades disponibles
    - precio: Precio unitario
    """
    id: str
    nombre: str
    cantidad: int
    precio: float

    # Ejemplo de uso de tuplas: devolver un resumen inmutable
    def identidad(self) -> Tuple[str, str]:
        return (self.id, self.nombre)

    def actualizar_cantidad(self, nueva_cantidad: int) -> None:
        if nueva_cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa.")
        self.cantidad = nueva_cantidad

    def actualizar_precio(self, nuevo_precio: float) -> None:
        if nuevo_precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        self.precio = nuevo_precio


# -------------------------------
# Clase Inventario
# -------------------------------
class Inventario:
    """
    Clase Inventario
    - Usa un diccionario {id: Producto}
    - Usa un set como índice auxiliar de nombres
    """
    def __init__(self) -> None:
        self._productos: Dict[str, Producto] = {}
        self._indice_nombres: Dict[str, Set[str]] = {}

    # CRUD
    def agregar(self, producto: Producto) -> None:
        if producto.id in self._productos:
            raise ValueError(f"Ya existe un producto con ID '{producto.id}'.")
        self._productos[producto.id] = producto
        self._agregar_indice_nombre(producto)

    def eliminar_por_id(self, id_producto: str) -> bool:
        prod = self._productos.pop(id_producto, None)
        if prod is None:
            return False
        clave = prod.nombre.strip().lower()
        if clave in self._indice_nombres and id_producto in self._indice_nombres[clave]:
            self._indice_nombres[clave].discard(id_producto)
            if not self._indice_nombres[clave]:
                del self._indice_nombres[clave]
        return True

    def actualizar_cantidad(self, id_producto: str, nueva_cantidad: int) -> bool:
        prod = self._productos.get(id_producto)
        if not prod:
            return False
        prod.actualizar_cantidad(nueva_cantidad)
        return True

    def actualizar_precio(self, id_producto: str, nuevo_precio: float) -> bool:
        prod = self._productos.get(id_producto)
        if not prod:
            return False
        prod.actualizar_precio(nuevo_precio)
        return True

    # Búsqueda y listado
    def buscar_por_nombre(self, nombre: str) -> List[Producto]:
        clave = nombre.strip().lower()
        ids = self._indice_nombres.get(clave, set())
        return [self._productos[i] for i in ids]

    def listar_todos(self) -> List[Producto]:
        return sorted(self._productos.values(), key=lambda p: p.nombre.lower())

    # Persistencia
    def guardar_en_archivo(self, ruta: str) -> None:
        data = {"productos": [asdict(p) for p in self._productos.values()]}
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @classmethod
    def cargar_desde_archivo(cls, ruta: str) -> "Inventario":
        inv = cls()
        if not os.path.exists(ruta):
            return inv
        with open(ruta, "r", encoding="utf-8") as f:
            raw = json.load(f)
        for p in raw.get("productos", []):
            prod = Producto(
                id=str(p["id"]),
                nombre=p["nombre"],
                cantidad=int(p["cantidad"]),
                precio=float(p["precio"]),
            )
            inv._productos[prod.id] = prod
            inv._agregar_indice_nombre(prod)
        return inv

    def _agregar_indice_nombre(self, producto: Producto) -> None:
        clave = producto.nombre.strip().lower()
        if clave not in self._indice_nombres:
            self._indice_nombres[clave] = set()
        self._indice_nombres[clave].add(producto.id)


# -------------------------------
# Interfaz de Usuario (consola)
# -------------------------------
ARCHIVO_DATOS = "inventario.json"

def imprimir_producto(p: Producto) -> None:
    print(f"[{p.id}] {p.nombre} | Cant: {p.cantidad} | Precio: ${p.precio:.2f}")

def menu() -> None:
    inv = Inventario.cargar_desde_archivo(ARCHIVO_DATOS)
    print("=== Sistema de Inventarios (POO + Colecciones) ===")
    while True:
        print("\nOpciones:")
        print("1) Añadir producto")
        print("2) Eliminar producto por ID")
        print("3) Actualizar cantidad")
        print("4) Actualizar precio")
        print("5) Buscar productos por nombre")
        print("6) Mostrar todo el inventario")
        print("7) Guardar inventario y salir")
        print("0) Salir sin guardar")
        opcion = input("Elige una opción: ").strip()

        try:
            if opcion == "1":
                idp = input("ID (único): ").strip()
                nombre = input("Nombre: ").strip()
                cantidad = int(input("Cantidad: ").strip())
                precio = float(input("Precio: ").strip())
                inv.agregar(Producto(id=idp, nombre=nombre, cantidad=cantidad, precio=precio))
                print("Producto agregado correctamente.")

            elif opcion == "2":
                idp = input("ID a eliminar: ").strip()
                ok = inv.eliminar_por_id(idp)
                print("Eliminado." if ok else "No se encontró el ID.")

            elif opcion == "3":
                idp = input("ID: ").strip()
                nueva = int(input("Nueva cantidad: ").strip())
                ok = inv.actualizar_cantidad(idp, nueva)
                print("Cantidad actualizada." if ok else "No se encontró el ID.")

            elif opcion == "4":
                idp = input("ID: ").strip()
                nuevo = float(input("Nuevo precio: ").strip())
                ok = inv.actualizar_precio(idp, nuevo)
                print("Precio actualizado." if ok else "No se encontró el ID.")

            elif opcion == "5":
                nombre = input("Nombre exacto a buscar: ").strip()
                resultados = inv.buscar_por_nombre(nombre)
                if not resultados:
                    print("Sin resultados.")
                else:
                    print(f"Resultados para '{nombre}':")
                    for p in resultados:
                        imprimir_producto(p)

            elif opcion == "6":
                todos = inv.listar_todos()
                if not todos:
                    print("Inventario vacío.")
                else:
                    print("Listado de productos:")
                    for p in todos:
                        imprimir_producto(p)

            elif opcion == "7":
                inv.guardar_en_archivo(ARCHIVO_DATOS)
                print(f"Inventario guardado en '{ARCHIVO_DATOS}'. ¡Hasta luego!")
                break

            elif opcion == "0":
                print("Saliendo sin guardar...")
                break

            else:
                print("Opción no válida. Intenta de nuevo.")

        except ValueError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    menu()
