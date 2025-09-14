from tkinter import *
from tkinter import ttk

# Función para agregar datos
def agregar_dato():
    dato = entrada.get()
    if dato:
        lista_datos.insert(END, dato)
        tabla.insert("", END, values=(dato,))
        entrada.delete(0, END)

# Función para limpiar datos
def limpiar_datos():
    entrada.delete(0, END)
    lista_datos.delete(0, END)
    for item in tabla.get_children():
        tabla.delete(item)

# Ventana principal
ventana = Tk()
ventana.title("Aplicación GUI Básica")
ventana.geometry("400x400")

# Etiqueta
etiqueta = Label(ventana, text="Ingresa un dato:")
etiqueta.pack(pady=5)

# Campo de texto
entrada = Entry(ventana)
entrada.pack(pady=5)

# Botón Agregar
boton_agregar = Button(ventana, text="Agregar", bg="#a6d8e7", command=agregar_dato)
boton_agregar.pack(pady=5)

# Botón Limpiar
boton_limpiar = Button(ventana, text="Limpiar", bg="#f7b0b0", command=limpiar_datos)
boton_limpiar.pack(pady=5)

# Lista de datos
lista_datos = Listbox(ventana)
lista_datos.pack(pady=5)

# Tabla para mostrar datos
tabla = ttk.Treeview(ventana, columns=("Dato"), show="headings")
tabla.heading("Dato", text="Dato")
tabla.pack(pady=5)

# Ejecutar la app
ventana.mainloop()
