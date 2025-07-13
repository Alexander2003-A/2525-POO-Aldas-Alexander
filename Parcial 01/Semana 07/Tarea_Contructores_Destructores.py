# clase.py
class Archivo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.archivo = open(nombre, 'w')
        print(f"[INIT] Archivo '{self.nombre}' ha sido creado y abierto.")

    def escribir(self, texto):
        self.archivo.write(texto)
        print(f"[WRITE] Se escribió en el archivo '{self.nombre}'.")

    def __del__(self):
        self.archivo.close()
        print(f"[DEL] Archivo '{self.nombre}' ha sido cerrado correctamente.")

# Uso de la clase
def main():
    archivo = Archivo("prueba.txt")
    archivo.escribir("Hola, esto es una prueba.")
    # Cuando termine el programa o se destruya el objeto, __del__ se ejecuta automáticamente.

if __name__ == "__main__":
    main()