import tkinter as tk

# Función para dibujar una línea utilizando el algoritmo DDA
def draw_line_dda(canvas, x0, y0, x1, y1, color):
    dx = x1 - x0
    dy = y1 - y0

    if abs(dx) > abs(dy):
        steps = abs(dx)
    else:
        steps = abs(dy)

    x_increment = dx / steps
    y_increment = dy / steps

    x = x0
    y = y0

    for i in range(steps):
        canvas.create_rectangle(round(x), round(y), round(x) + 1, round(y) + 1, fill=color, outline=color)
        x += x_increment
        y += y_increment

# Crear una ventana tkinter
root = tk.Tk()
root.title("Algoritmo DDA para Línea")

# Crear un lienzo (canvas)
canvas_width = 400
canvas_height = 300
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="black")
canvas.pack()

# Dibujar una línea utilizando el algoritmo DDA
draw_line_dda(canvas, 100, 1000, 350, 250, "white")

# Ejecutar la ventana principal
root.mainloop()
