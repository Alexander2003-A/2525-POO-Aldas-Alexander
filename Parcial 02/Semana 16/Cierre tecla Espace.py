from tkinter import *

# Lista de tareas
tareas = []

# Función para actualizar la lista visual
def actualizar_lista():
    lista.delete(0, END)
    for tarea in tareas:
        texto = tarea["texto"]
        if tarea["completada"]:
            texto += " ✔️"
        lista.insert(END, texto)

# Función para agregar tarea
def agregar_tarea(event=None):
    texto = entrada.get()
    if texto:
        tareas.append({"texto": texto, "completada": False})
        entrada.delete(0, END)
        actualizar_lista()

# Función para marcar como completada
def marcar_completada(event=None):
    seleccion = lista.curselection()
    if seleccion:
        index = seleccion[0]
        tareas[index]["completada"] = True
        actualizar_lista()

# Función para eliminar tarea
def eliminar_tarea(event=None):
    seleccion = lista.curselection()
    if seleccion:
        index = seleccion[0]
        tareas.pop(index)
        actualizar_lista()

# Función para cerrar la app
def cerrar_app(event=None):
    ventana.destroy()

# Crear ventana principal
ventana = Tk()
ventana.title("Gestión de Tareas")
ventana.geometry("400x400")

# Campo de entrada
entrada = Entry(ventana, width=40)
entrada.pack(pady=10)
entrada.focus()

# Lista de tareas
lista = Listbox(ventana, width=50)
lista.pack(pady=10)

# Botones
Button(ventana, text="Añadir Tarea", command=agregar_tarea).pack(pady=5)
Button(ventana, text="Marcar como Completada", command=marcar_completada).pack(pady=5)
Button(ventana, text="Eliminar Tarea", command=eliminar_tarea).pack(pady=5)

# Atajos de teclado
ventana.bind("<Return>", agregar_tarea)
ventana.bind("<c>", marcar_completada)
ventana.bind("<d>", eliminar_tarea)
ventana.bind("<Delete>", eliminar_tarea)
ventana.bind("<Escape>", cerrar_app)

# Ejecutar la app
ventana.mainloop()
