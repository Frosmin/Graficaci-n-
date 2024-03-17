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
        self.draw_line_dda(300,100,50,250)
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
            self.draw_pixel(x0, y0)
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy
        
    def draw_line_dda(self, x0, y0, x1, y1):
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
            self.draw_pixel(round(x), round(y))
            x += x_increment
            y += y_increment
        
    def draw_circle_bresenham(self, x_center, y_center, r):
        x = 0
        y = r
        p = 1 - r

        while x < y:
            self.draw_pixel(x_center + x, y_center + y)
            self.draw_pixel(x_center - x, y_center + y)
            self.draw_pixel(x_center + x, y_center - y)
            self.draw_pixel(x_center - x, y_center - y)
            self.draw_pixel(x_center + y, y_center + x)
            self.draw_pixel(x_center - y, y_center + x)
            self.draw_pixel(x_center + y, y_center - x)
            self.draw_pixel(x_center - y, y_center - x)

            x += 1
            if p < 0:
                p = p + 2 * x + 1;
            else:
                y -= 1
                p = p + 2 * (x - y) + 1
    
root = tk.Tk()

root.title("Algoritmos para graficacion")

my_gui = Gui(root)

root.mainloop()
