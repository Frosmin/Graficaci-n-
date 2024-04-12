#/usr/bin/env python3

import tkinter as tk
from tkinter import colorchooser
import math
import time 
from PIL import Image, ImageTk

class Gui:
    def __init__(self, master) -> None:
        self.master = master
        self.master.geometry('700x500')

        # Color
        self.color = tk.StringVar(value='black')

        # Otras variables
        self.puntos = list()
        self.es_linea = False 
        self.es_circulo = False
        self.ready_to_draw = False

        # Frame opciones
        self.frame_options = tk.Frame(self.master, width=700, height=100)
        self.frame_options.config(bg='red')
        self.frame_options.pack()

        # Boton linea
        self.img_linea = ImageTk.PhotoImage(Image.open('./images/linea.png').resize((20,20)))
        self.boton_linea = tk.Button(self.frame_options, width=20, height=20, image=self.img_linea, command= self.set_linea)
        self.boton_linea.pack(side='left')

        # Boton circulo
        self.img_circulo = ImageTk.PhotoImage(Image.open('./images/circulo.png').resize((17,17)))
        self.boton_circulo = tk.Button(self.frame_options, width=20, height=20, image=self.img_circulo, command= self.set_circulo)
        self.boton_circulo.pack(side='left')

        # Combo box elementos

        # Boton Scan-Line

        # Boton Inundacion

        # Mover

        # Scale

        # Rotate

        # Color selector
        self.boton_color = tk.Button(self.frame_options, text='Choose color', command=self.color_picker)
        self.boton_color.pack(side='left')


        # Frame Lienzo
        self.frame_canva = tk.Frame(self.master, width=700, height=400)
        self.frame_canva.config(bg='yellow')
        self.frame_canva.pack()
        
        # Crear un lienzo (canvas)
        #self.canvas = tk.Canvas(self.master, width=self.grid_size*self.pixel_size, height=self.grid_size*self.pixel_size)
        self.canvas = tk.Canvas(self.frame_canva, width=700, height=500)
        self.canvas.pack()
        self.canvas.config(bg="white")
        #self.draw_grid()

        # Eventos
        self.canvas.bind('<Button-1>', self.handle_click)

        

    def color_picker(self):
        my_color = colorchooser.askcolor()[0]
        self.color.set(my_color)
        print(self.color.get())
    
    def set_linea(self):
        self.puntos.clear()
        self.es_circulo = False
        self.es_linea = True
    
    def set_circulo(self):
        self.puntos.clear()
        self.es_linea = False
        self.es_circulo = True


    def handle_click(self, event = None):
        x , y = int(event.x) , int(event.y)

        if self.es_linea:
            self.puntos.append((x,y))
            if len(self.puntos) == 2:
                self.draw_line()
                self.puntos.clear()
        elif self.es_circulo:
            self.puntos.append((x,y))
            if len(self.puntos) == 2:
                self.draw_circle()
                self.puntos.clear()

        print(self.puntos)

    def draw_line(self):
        linea = self.Line(self.canvas) 
        linea.draw_line_bresenham(*self.puntos[-1],*self.puntos[-2])
        self.is_drawing=False
    
    def draw_circle(self):
        def calc_r(x1,y1,x2,y2):
            r = round(math.sqrt((x2-x1)**2 + (y2-y1)**2))
            return r
        circulo = self.Circle(self.canvas)
        circulo.draw_circle_bresenham(*self.puntos[0], calc_r(*self.puntos[0], *self.puntos[1]))


    class Line():
        def __init__(self, canva) -> None:
            self.canvas = canva

        def draw_pixel(self, x, y):
    
            x1, y1 = (x,y)
            x2, y2 = ((x+1), (y+1))
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
                time.sleep(0.02)
            print(begin)
            print(end)
            print(f"timpo de ejecucion linea DDA: {end - begin}")

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
                    err -= (dy)
                    x0 += (sx)
                if e2 < dx:
                    err += (dx)
                    y0 += (sy)

    
    class Circle():
        def __init__(self, canva) -> None:
            self.canvas = canva

        def draw_pixel(self, x, y):
            #x1, y1 = (x*self.pixel_size,y*self.pixel_size)
            #x2, y2 = ((x+1)*self.pixel_size, (y+1)*self.pixel_size)
            x1, y1 = (x,y)
            x2, y2 = ((x+1), (y+1))
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="black")

        def draw_circle_basic(self, xc, yc, r):
            begin = time.time()
            for x in range(xc - r, xc + r ):  #200 200 100      100, 100   
                y_positivo = yc + int((r ** 2 - (x - xc) **  2) ** 0.5)
                y_negativo = yc - int((r ** 2 - (x - xc) ** 2) ** 0.5)
                self.draw_pixel(x, y_positivo)
                self.draw_pixel(x, y_negativo)
                self.master.update()
                time.sleep(0.1)
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
                self.master.update()
                time.sleep(0.02)    
            end = time.time()
            print(f"Tiempo de inicio: {begin}")
            print(f"Tiempo de fin: {end}")
            print(f"Tiempo de ejecución circunferencia polar: {end - begin}")

        def draw_circle_bresenham(self, x_center, y_center, r):
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

if __name__ == "__main__":
    root = tk.Tk()
    my_gui = Gui(root)
    root.title('Grafiación por computadora')
    root.iconbitmap(bitmap='./images/tortuga.ico')
    root.mainloop()
