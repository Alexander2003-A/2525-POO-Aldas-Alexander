from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry

# Función para agregar evento
def agregar_evento():
    fecha = campo_fecha.get()
    hora = campo_hora.get()
    descripcion = campo_desc.get()
    if fecha and hora and descripcion:
        tabla.insert("", END, values=(fecha, hora, descripcion))
        actualizar_total()
        campo_hora.delete(0, END)
        campo_desc.delete(0, END)

# Función para eliminar evento seleccionado
def eliminar_evento():
    seleccionado = tabla.selection()
    for item in seleccionado:
        tabla.delete(item)
    actualizar_total()

# Función para actualizar el total de eventos
def actualizar_total():
    total = len(tabla.get_children())
    etiqueta_total.config(text=f"Total de eventos: {total}")

# Crear ventana principal
ventana = Tk()
ventana.title("Agenda Personal")
ventana.geometry("500x500")

# Frame de entrada de datos
frame_entrada = Frame(ventana)
frame_entrada.pack(pady=10)

Label(frame_entrada, text="Fecha:").grid(row=0, column=0)
campo_fecha = DateEntry(frame_entrada, date_pattern='dd/mm/yyyy')
campo_fecha.grid(row=0, column=1)

Label(frame_entrada, text="Hora:").grid(row=1, column=0)
campo_hora = Entry(frame_entrada)
campo_hora.grid(row=1, column=1)

Label(frame_entrada, text="Descripción:").grid(row=2, column=0)
campo_desc = Entry(frame_entrada)
campo_desc.grid(row=2, column=1)

# Botones
frame_botones = Frame(ventana)
frame_botones.pack(pady=10)

Button(frame_botones, text="Agregar Evento", bg="#a6d8e7", command=agregar_evento).grid(row=0, column=0, padx=5)
Button(frame_botones, text="Eliminar Evento Seleccionado", bg="#f7b0b0", command=eliminar_evento).grid(row=0, column=1, padx=5)
Button(frame_botones, text="Salir", bg="#d3d3d3", command=ventana.quit).grid(row=0, column=2, padx=5)

# Tabla de eventos
tabla = ttk.Treeview(ventana, columns=("Fecha", "Hora", "Descripción"), show="headings")
tabla.heading("Fecha", text="Fecha")
tabla.heading("Hora", text="Hora")
tabla.heading("Descripción", text="Descripción")
tabla.pack(pady=10)

# Etiqueta de total de eventos
etiqueta_total = Label(ventana, text="Total de eventos: 0")
etiqueta_total.pack()

# Ejecutar la app
ventana.mainloop()


