from tkinter import *

# Lista para guardar las tareas
tareas = []

# Función para agregar tarea
def agregar_tarea():
    tarea = entrada.get()
    if tarea:
        tareas.append({"texto": tarea, "completada": False})
        entrada.delete(0, END)
        actualizar_lista()

# Función para marcar como completada
def marcar_completada():
    seleccion = lista.curselection()
    if seleccion:
        index = seleccion[0]
        tareas[index]["completada"] = True
        actualizar_lista()

# Función para eliminar tarea
def eliminar_tarea():
    seleccion = lista.curselection()
    if seleccion:
        index = seleccion[0]
        tareas.pop(index)
        actualizar_lista()

# Función para actualizar la lista visual
def actualizar_lista():
    lista.delete(0, END)
    for tarea in tareas:
        texto = tarea["texto"]
        if tarea["completada"]:
            texto += " ✔️"
        lista.insert(END, texto)

# Crear ventana principal
ventana = Tk()
ventana.title("Lista de Tareas")
ventana.geometry("400x400")

# Campo de entrada
entrada = Entry(ventana, width=40)
entrada.pack(pady=10)

# Botones
Button(ventana, text="Añadir Tarea", command=agregar_tarea).pack(pady=5)
Button(ventana, text="Marcar como Completada", command=marcar_completada).pack(pady=5)
Button(ventana, text="Eliminar Tarea", command=eliminar_tarea).pack(pady=5)

# Lista de tareas
lista = Listbox(ventana, width=50)
lista.pack(pady=10)

# Ejecutar la app
ventana.mainloop()
