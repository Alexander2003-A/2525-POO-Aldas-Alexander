# inventario_app.py
# Sistema de Gestión de Inventarios con persistencia en archivo y manejo de excepciones.
# Formato de archivo: CSV simple (id,nombre,cantidad,precio)

from dataclasses import dataclass
from typing import Dict, Optional
import os

ARCHIVO_INVENTARIO = "inventario.txt"


@dataclass
class Producto:
    id: str
    nombre: str
    cantidad: int
    precio: float

    @staticmethod
    def desde_csv(linea: str) -> Optional["Producto"]:
        """Convierte 'id,nombre,cantidad,precio' en Producto. Devuelve None si está corrupta."""
        try:
            partes = [p.strip() for p in linea.split(",")]
            if len(partes) != 4:
                return None
            _id, nombre, cantidad, precio = partes
            return Producto(id=_id, nombre=nombre, cantidad=int(cantidad), precio=float(precio))
        except Exception:
            return None

    def a_csv(self) -> str:
        return f"{self.id},{self.nombre},{self.cantidad},{self.precio:.2f}"


class Inventario:
    def __init__(self, ruta_archivo: str = ARCHIVO_INVENTARIO):
        self.ruta = ruta_archivo
        self.productos: Dict[str, Producto] = {}
        self.cargar_desde_archivo()

    # ---------------------- Persistencia ----------------------

    def cargar_desde_archivo(self) -> None:
        """Carga los productos del archivo. Si no existe, lo crea vacío."""
        try:
            if not os.path.exists(self.ruta):
                # Crear archivo vacío de manera segura
                with open(self.ruta, "w", encoding="utf-8") as _:
                    pass
                print(f"[INFO] No se encontró '{self.ruta}'. Se creó un archivo nuevo.")
                return

            lineas_corruptas = 0
            with open(self.ruta, "r", encoding="utf-8") as f:
                for linea in f:
                    linea = linea.strip()
                    if not linea:
                        continue
                    prod = Producto.desde_csv(linea)
                    if prod is None:
                        lineas_corruptas += 1
                        continue
                    self.productos[prod.id] = prod

            print(f"[OK] Inventario cargado. Productos: {len(self.productos)}.")
            if lineas_corruptas:
                print(f"[ADVERTENCIA] {lineas_corruptas} línea(s) corrupta(s) ignorada(s) en '{self.ruta}'.")
        except PermissionError:
            print(f"[ERROR] Permiso denegado al leer '{self.ruta}'. Cierra el archivo o ajusta permisos.")
        except FileNotFoundError:
            # Muy raro porque lo verificamos antes, pero lo manejamos por robustez
            print(f"[ERROR] Archivo '{self.ruta}' no encontrado.")
        except OSError as e:
            print(f"[ERROR] Problema de E/S al leer '{self.ruta}': {e}")

    def guardar_en_archivo(self) -> bool:
        """Guarda el inventario en el archivo. Devuelve True si tuvo éxito."""
        try:
            with open(self.ruta, "w", encoding="utf-8") as f:
                for p in self.productos.values():
                    f.write(p.a_csv() + "\n")
            print(f"[OK] Cambios guardados en '{self.ruta}'.")
            return True
        except PermissionError:
            print(f"[ERROR] Permiso denegado al escribir en '{self.ruta}'.")
        except OSError as e:
            print(f"[ERROR] Problema de E/S al escribir en '{self.ruta}': {e}")
        return False

    # ---------------------- Operaciones CRUD ----------------------

    def anadir_producto(self, producto: Producto) -> bool:
        if producto.id in self.productos:
            print("[INFO] Ya existe un producto con ese ID. Use 'actualizar' si desea modificarlo.")
            return False
        self.productos[producto.id] = producto
        if self.guardar_en_archivo():
            print(f"[OK] Producto '{producto.nombre}' añadido y guardado.")
            return True
        else:
            # revertir en memoria si fallo al guardar
            self.productos.pop(producto.id, None)
            return False

    def actualizar_producto(self, id_: str, nombre: Optional[str] = None,
                            cantidad: Optional[int] = None, precio: Optional[float] = None) -> bool:
        p = self.productos.get(id_)
        if not p:
            print("[INFO] No existe un producto con ese ID.")
            return False

        # Copia para posible rollback
        copia = Producto(p.id, p.nombre, p.cantidad, p.precio)

        if nombre is not None:
            p.nombre = nombre
        if cantidad is not None:
            if cantidad < 0:
                print("[INFO] La cantidad no puede ser negativa.")
                return False
            p.cantidad = cantidad
        if precio is not None:
            if precio < 0:
                print("[INFO] El precio no puede ser negativo.")
                return False
            p.precio = precio

        if self.guardar_en_archivo():
            print(f"[OK] Producto '{id_}' actualizado.")
            return True
        else:
            # rollback si no se pudo guardar
            self.productos[id_] = copia
            return False

    def eliminar_producto(self, id_: str) -> bool:
        if id_ not in self.productos:
            print("[INFO] No existe un producto con ese ID.")
            return False

        respaldo = self.productos.pop(id_)
        if self.guardar_en_archivo():
            print(f"[OK] Producto '{id_}' eliminado.")
            return True
        else:
            # rollback
            self.productos[id_] = respaldo
            return False

    def listar(self) -> None:
        if not self.productos:
            print("Inventario vacío.")
            return
        print("\nID | NOMBRE | CANTIDAD | PRECIO")
        print("-" * 35)
        for p in self.productos.values():
            print(f"{p.id} | {p.nombre} | {p.cantidad} | {p.precio:.2f}")
        print("")

# ---------------------- Interfaz de consola ----------------------

def menu():
    inv = Inventario()

    opciones = {
        "1": "Listar productos",
        "2": "Añadir producto",
        "3": "Actualizar producto",
        "4": "Eliminar producto",
        "5": "Salir"
    }

    while True:
        print("\n====== SISTEMA DE INVENTARIO ======")
        for k, v in opciones.items():
            print(f"{k}. {v}")
        op = input("Elija una opción: ").strip()

        try:
            if op == "1":
                inv.listar()

            elif op == "2":
                id_ = input("ID: ").strip()
                nombre = input("Nombre: ").strip()
                cantidad = int(input("Cantidad: ").strip())
                precio = float(input("Precio: ").strip())
                inv.anadir_producto(Producto(id_, nombre, cantidad, precio))

            elif op == "3":
                id_ = input("ID del producto a actualizar: ").strip()
                print("Deje vacío cualquier campo para no cambiarlo.")
                nombre = input("Nuevo nombre: ").strip()
                cantidad_txt = input("Nueva cantidad: ").strip()
                precio_txt = input("Nuevo precio: ").strip()

                nombre = nombre or None
                cantidad = int(cantidad_txt) if cantidad_txt else None
                precio = float(precio_txt) if precio_txt else None

                inv.actualizar_producto(id_, nombre, cantidad, precio)

            elif op == "4":
                id_ = input("ID del producto a eliminar: ").strip()
                inv.eliminar_producto(id_)

            elif op == "5":
                print("Saliendo... ¡Hasta pronto!")
                break
            else:
                print("[INFO] Opción no válida.")
        except ValueError:
            # Errores típicos de conversión (por ejemplo, cantidad/precio no numérico)
            print("[ERROR] Entrada no válida. Revise los tipos de dato (cantidad entera, precio numérico).")
        except KeyboardInterrupt:
            print("\n[INFO] Interrupción detectada. Guardando y saliendo…")
            inv.guardar_en_archivo()
            break


if __name__ == "__main__":
    menu()
