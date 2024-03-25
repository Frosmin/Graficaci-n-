#/usr/bin/env python3

import tkinter as tk
import math
import time 
from multiprocessing import Process
import threading


class Gui:
    def __init__(self, master) -> None:
        self.master = master
        
        self.pixel_size = 10
        self.grid_size = 50

        # Crear un lienzo (canvas)
        self.canvas = tk.Canvas(self.master, width=self.grid_size*self.pixel_size, height=self.grid_size*self.pixel_size)
        self.canvas.pack()
        self.canvas.config(bg="white")

        self.draw_grid()

    
    def draw_grid(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x1, y1 = (i*self.pixel_size, j*self.pixel_size)
                x2, y2 = ((i+1)*self.pixel_size, (j+1)*self.pixel_size)
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="gray", width=1)
    
    def draw_pixel(self, x, y):
        x1, y1 = (x*self.pixel_size,y*self.pixel_size)
        x2, y2 = ((x+1)*self.pixel_size, (y+1)*self.pixel_size)
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="black")

    def draw_line_basic(self, x0, y0, x1, y1):
        begin = time.time()
        m = (y1 - y0)/(x1 - x0)       
        b = y0 - m * x0
        
        self.draw_pixel(x0, y0)
        x = x0
        y = y0
        if x0 < x1:
            while x <= x1:
                y = m * x + b
                self.draw_pixel(x, y)
                x += 1
        else:
            while x >= x1:
                y = m * x + b
                self.draw_pixel(x, y)
                x -= 1


        end = time.time()
        print(begin)
        print(end)
        print(f"timpo de ejecucion linea basico: {end - begin}")




    def draw_line_dda(self, x0, y0, x1, y1):
        begin = time.time()
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
            end = time.time()
            self.master.update()
            time.sleep(0.5)
        print(begin)
        print(end)
        print(f"timpo de ejecucion linea DDA: {end - begin}")

    
    def draw_line_bresenham(self, x0, y0, x1, y1):
        begin = time.time()
        dx = abs(x1 - x0) 
        dy = abs(y1 - y0) 
        sx = -1 if x0 > x1 else 1
        sy = -1 if y0 > y1 else 1
        err = dx - dy

        while x0 != x1 or y0 != y1:
            self.draw_pixel(x0, y0)
            e2 = 2 * err
            if e2 > -dy:
                err -= (dy)
                x0 += (sx)
            if e2 < dx:
                err += (dx)
                y0 += (sy)
            self.master.update()
            time.sleep(0.5)
            

        end = time.time()
        print(begin)
        print(end)
        print(f"timpo de ejecucion liena bresenham: {end - begin}")

    def draw_circle_basic(self, xc, yc, r):
        begin = time.time()
        for x in range(xc - r, xc + r ):  #200 200 100      100, 100   
            y_positivo = yc + int((r ** 2 - (x - xc) **  2) ** 0.5)
            y_negativo = yc - int((r ** 2 - (x - xc) ** 2) ** 0.5)
            self.draw_pixel(x, y_positivo)
            self.draw_pixel(x, y_negativo)
        end = time.time()
        print(begin)
        print(end)
        print(f"Tiempo de ejecución circunferencia basico: {end - begin}")
        
    def draw_circle_polar(self, xc, yc, r):
        begin = time.time()
        for i in range(360):
            sin_values = r * math.sin(i * math.pi / 180)
            cos_values = r * math.cos(i * math.pi / 180) 
            x = xc + cos_values
            y = yc + sin_values
            self.draw_pixel(round(x), round(y))
        end = time.time()
        print(f"Tiempo de inicio: {begin}")
        print(f"Tiempo de fin: {end}")
        print(f"Tiempo de ejecución circunferencia polar: {end - begin}")

    def draw_circle_bresenham(self, x_center, y_center, r):
        begin = time.time()
        x = 0
        y = r
        p = 1 - r

        while x <= y:
            self.draw_pixel(x_center + x, y_center + y)
            self.draw_pixel(x_center - x, y_center + y)
            self.draw_pixel(x_center + x, y_center - y)
            self.draw_pixel(x_center - x, y_center - y)
            self.draw_pixel(x_center + y, y_center + x)
            self.draw_pixel(x_center - y, y_center + x)
            self.draw_pixel(x_center + y, y_center - x)
            self.draw_pixel(x_center - y, y_center - x)

            x += 1
            if p <= 0:
                p = p + 2 * x + 1;
            else:
                y -= 1
                p = p + 2 * (x - y) + 1
            self.master.update()
            time.sleep(1)

        end = time.time()
        print(f"Tiempo de inicio: {begin}")
        print(f"Tiempo de fin: {end}")
        print(f"Tiempo de ejecución circunferencia Bresenham: {end - begin}")

    
def crear_interfaz(name,funcion,titulo,*arg):
    name = tk.Tk()
    my_gui = Gui(name)
    name.title(titulo)
    if funcion == "bres":
        x,y,z = arg
        my_gui.draw_circle_bresenham(x,y,z)
    elif funcion == "polar" :
        x,y,z = arg
        my_gui.draw_circle_polar(x,y,z)
    elif funcion == "dda":
        x,y,z,w = arg
        my_gui.draw_line_dda(x,y,z,w)
    else:    
        x,y,z,w = arg
        my_gui.draw_line_bresenham(x,y,z,w)
    name.mainloop()

if __name__ == "__main__":
    t1 = Process(target=crear_interfaz, args=("root1","dda","Algoritmo dda linea",10,10,40,35))
    t2 = Process(target=crear_interfaz, args=("root2","asdf","Algoritmo b linea",10,10,40,35))

    t1.start()
    t2.start()

    t1.join()
    t2.join()
