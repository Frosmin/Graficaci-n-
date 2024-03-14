import tkinter as tk

# Función para dibujar un pixel en la posición (x, y)
def draw_pixel(canvas, x, y, color):
    x1, y1 = (x, y)
    x2, y2 = (x + 1, y + 1)
    canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)

# Crear una ventana tkinter
root = tk.Tk()
root.title("Dibujar Pixel")

# Crear un lienzo (canvas)
canvas_width = 400
canvas_height = 300
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack()

# Definir el color del pixel (en este caso, rojo)
pixel_color = "red"

# Dibujar un pixel en la posición (100, 100)
draw_pixel(canvas, 100, 100, pixel_color)

# Ejecutar la ventana principal
root.mainloop()
