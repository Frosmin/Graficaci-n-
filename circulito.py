import tkinter as tk

# Función para dibujar una circunferencia utilizando el algoritmo de Bresenham
def draw_circle_bresenham(canvas, x_center, y_center, radius, color):
    x = radius
    y = 0
    err = 0

    while x >= y:
        canvas.create_rectangle(x_center + x, y_center + y, x_center + x + 1, y_center + y + 1, fill=color, outline=color)
        canvas.create_rectangle(x_center + y, y_center + x, x_center + y + 1, y_center + x + 1, fill=color, outline=color)
        canvas.create_rectangle(x_center - y, y_center + x, x_center - y + 1, y_center + x + 1, fill=color, outline=color)
        canvas.create_rectangle(x_center - x, y_center + y, x_center - x + 1, y_center + y + 1, fill=color, outline=color)
        canvas.create_rectangle(x_center - x, y_center - y, x_center - x + 1, y_center - y + 1, fill=color, outline=color)
        canvas.create_rectangle(x_center - y, y_center - x, x_center - y + 1, y_center - x + 1, fill=color, outline=color)
        canvas.create_rectangle(x_center + y, y_center - x, x_center + y + 1, y_center - x + 1, fill=color, outline=color)
        canvas.create_rectangle(x_center + x, y_center - y, x_center + x + 1, y_center - y + 1, fill=color, outline=color)

        if err <= 0:
            y += 1
            err += 2 * y + 1
        if err > 0:
            x -= 1
            err -= 2 * x + 1

# Crear una ventana tkinter
root = tk.Tk()
root.title("Algoritmo de Bresenham para Circunferencia")

# Crear un lienzo (canvas)
canvas_width = 1000
canvas_height = 300
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="black")
canvas.pack()

# Dibujar una circunferencia utilizando el algoritmo de Bresenham
draw_circle_bresenham(canvas, 210,160, 10, "red")

# Ejecutar la ventana principal
root.mainloop()
