import os


def mostrar_codigo(ruta_script):
    # Asegúrate de que la ruta al script es absoluta
    ruta_script_absoluta = os.path.abspath(ruta_script)
    try:
        with open(ruta_script_absoluta, 'r') as archivo:
            print(f"\n--- Código de {ruta_script} ---\n")
            print(archivo.read())
    except FileNotFoundError:
        print("El archivo no se encontró.")
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {e}")


def mostrar_menu():
    # Define la ruta base donde se encuentra el dashboard.py
    ruta_base = os.path.dirname(__file__)

    opciones = {
        '1': 'Parcial 01/Semana 02/2.1 Tarea Semana 02.py',
        '2': 'Parcial 01/Semana 03/Programacion_(POO).py',
        '3': 'Parcial 01/Semana 03/Programacion_tradicional.py',
        '4': 'Parcial 01/Semana 04/EjemplosMundoReal_POO.py',
        '5': 'Parcial 01/Semana 05/Area_Circulo.py',
        '6': 'Parcial 01/Semana 06/Tarea_POO_vehiculos.py',
        '7': 'Parcial 01/Semana 07/prueba.txt',
        '8': 'Parcial 01/Semana 07/Tarea_Contructores_Destructores.py',

        # Agrega aquí el resto de las rutas de los scripts
    }

    while True:
        print("\nMenu Principal - Dashboard")
        # Imprime las opciones del menú
        for key in opciones:
            print(f"{key} - {opciones[key]}")
        print("0 - Salir")

        eleccion = input("Elige un script para ver su código o '0' para salir: ")
        if eleccion == '0':
            break
        elif eleccion in opciones:
            # Asegura que el path sea absoluto
            ruta_script = os.path.join(ruta_base, opciones[eleccion])
            mostrar_codigo(ruta_script)
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")


# Ejecutar el dashboard
if __name__ == "__main__":
    mostrar_menu()