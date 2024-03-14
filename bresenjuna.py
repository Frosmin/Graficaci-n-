import tkinter as tk

# Función para dibujar una línea utilizando el algoritmo de Bresenham
def draw_line_bresenham(canvas, x0, y0, x1, y1, color):
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = -1 if x0 > x1 else 1
    sy = -1 if y0 > y1 else 1
    err = dx - dy

    while x0 != x1 or y0 != y1:
        canvas.create_rectangle(x0, y0, x0 + 1, y0 + 1, fill=color, outline=color)
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

# Crear una ventana tkinter
root = tk.Tk()
root.title("Algoritmo de Bresenham")

# Crear un lienzo (canvas)
canvas_width = 400
canvas_height = 300
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="black")
canvas.pack()

# Dibujar una línea utilizando el algoritmo de Bresenham
draw_line_bresenham(canvas, 50, 50, 350, 250, "white")

# Ejecutar la ventana principal
root.mainloop()
