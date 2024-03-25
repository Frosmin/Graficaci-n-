#/usr/bin/env python3

import tkinter as tk
import math
import time 



class Gui:
    def __init__(self, master) -> None:
        self.master = master
        
        # Crear un lienzo (canvas)
        self.canvas = tk.Canvas(self.master, width=1000, height=700)
        self.canvas.pack()
        self.canvas.config(bg="white")
     
     
        self.linea_basica = 0
        self.linea_dda = 0
        self.linea_bresenham = 0
        
        self.circulo_bresem = 0
        self.circulo_basico = 0
        self.circulo_polar = 0
        
      
  ###########################################################################################  
        for i in range(41):
            self.draw_line_basic(i*10,  i * 10, 500, i * 20)
        avr = self.linea_basica/40
        print(f"Promedio de linea_basica {avr} ")
        
        
        for i in range(41):
            self.draw_line_dda(i*10,  i * 10, 500, i * 20)
        avr2 = self.linea_dda/40
        print(f"Promedio de linea_basica {avr2} ")
        
        for i in range(41):
            self.draw_line_bresenham(i*10,  i * 10, 500, i * 20)
        avr3 = self.linea_bresenham/40
        print(f"Promedio de linea_basica {avr3} ")
        
        for i in range(41):
            self.draw_circle_basic(20 * i,100,50 )
        avr4 = self.circulo_basico/40
        print (f"Promedio de circulo_basico {avr4}")
        
        for i in range(41):
            self.draw_circle_polar(20 * i,100,50 )
        avr5 = self.circulo_polar/40
        print (f"Promedio de circulo_polar {avr5}")
    
        for i in range(41):
            self.draw_circle_bresenham(20 * i,100,50 )
        avr6 = self.circulo_bresem/40
        print (f"Promedio de circulo_bresem {avr6}")
            
  ##########################################################################################      
        
        
        
    def draw_pixel(self, x, y):
        x1, y1 = (x,y)
        x2, y2 = (x + 1, y + 1)
        self.canvas.create_rectangle(x1, y1, x2, y2)

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
        
        self.linea_basica += (end - begin)
        # print(begin)
        # print(end)
        # print(f"timpo de ejecucion linea basico: {end - begin}")


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
        self.linea_dda += (end - begin)    
        # print(begin)
        # print(end)
        # print(f"timpo de ejecucion linea DDA: {end - begin}")

    
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
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy
        end = time.time()
        self.linea_bresenham += (end - begin)
        # print(begin)
        # print(end)
        # print(f"timpo de ejecucion liena bresenham: {end - begin}")

    def draw_circle_basic(self, xc, yc, r):
        begin = time.time()
        for x in range(xc - r, xc + r ):  #En otras palabras, recorre todas las coordenadas x donde podría estar el círculo, según su radio r.
            y_positivo = yc + int((r ** 2 - (x - xc) **  2) ** 0.5) #Calcula la coordenada y positiva del círculo, según la ecuación de la circunferencia.
            y_negativo = yc - int((r ** 2 - (x - xc) ** 2) ** 0.5) #Calcula la coordenada y negativa del círculo, según la ecuación de la circunferencia.
            self.draw_pixel(x, y_positivo)
            self.draw_pixel(x, y_negativo)
        end = time.time()
        self.circulo_basico += (end - begin)
        # print(begin)
        # print(end)
        # print(f"Tiempo de ejecución circunferencia basico: {end - begin}")
        
    def draw_circle_polar(self, xc, yc, r):
        begin = time.time()
        for i in range(360):
            sin_values = r * math.sin(i * math.pi / 180) #Se calculan los valores de seno y coseno para cada ángulo i.
            cos_values = r * math.cos(i * math.pi / 180) 
            x = xc + cos_values # aqui se convierten las corenads polares a coordenadas cartesianas
            y = yc + sin_values
            self.draw_pixel(round(x), round(y))
        end = time.time()
        self.circulo_polar += (end - begin)
        # print(f"Tiempo de inicio: {begin}")
        # print(f"Tiempo de fin: {end}")
        # print(f"Tiempo de ejecución circunferencia polar: {end - begin}")

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
        end = time.time()
        self.circulo_bresem += (end - begin)
        # print(f"Tiempo de inicio: {begin}")
        # print(f"Tiempo de fin: {end}")
        # print(f"Tiempo de ejecución circunferencia Bresenham: {end - begin}")

    
root = tk.Tk()

root.title("Algoritmos para graficacion")   

my_gui = Gui(root)

root.mainloop()
