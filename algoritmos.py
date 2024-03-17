#/usr/bin/env python3

import tkinter as tk

class Gui:
    def __init__(self, master) -> None:
        self.master = master
        
        # Crear un lienzo (canvas)
        self.canvas = tk.Canvas(self.master, width=400, height=300)
        self.canvas.pack()
        self.canvas.config(bg="white")

        self.draw_pixel(10,10)
        self.draw_line_bresenham(20,20,150,150)
        self.draw_circle_bresenham(300,200,20)
        
    def draw_pixel(self, x, y):
        x1, y1 = (x,y)
        x2, y2 = (x + 1, y + 1)
        self.canvas.create_rectangle(x1, y1, x2, y2)

    def draw_line_bresenham(self, x0, y0, x1, y1):
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = -1 if x0 > x1 else 1
        sy = -1 if y0 > y1 else 1
        err = dx - dy

        while x0 != x1 or y0 != y1:
            #self.canvas.create_rectangle(x0, y0, x0 + 1, y0 + 1)
            self.draw_pixel(x0, y0)
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy
        
    def draw_circle_bresenham(self, x_center, y_center, radius):
        x = radius
        y = 0
        err = 0

        while x >= y:
            self.draw_pixel(x_center + y, y_center + x)
            self.draw_pixel(x_center - y, y_center + x)
            self.draw_pixel(x_center - x, y_center + y)
            self.draw_pixel(x_center - x, y_center - y)
            self.draw_pixel(x_center + x, y_center + y)
            self.draw_pixel(x_center - y, y_center - x)
            self.draw_pixel(x_center + y, y_center - x)
            self.draw_pixel(x_center + x, y_center - y)

            if err <= 0:
                y += 1
                err += 2 * y + 1
            if err > 0:
                x -= 1
                err -= 2 * x + 1

    
root = tk.Tk()

root.title("Algoritmos para graficacion")

my_gui = Gui(root)

root.mainloop()
