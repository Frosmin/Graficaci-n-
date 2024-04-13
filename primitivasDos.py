#/usr/bin/env python3

import tkinter as tk
from tkinter import colorchooser, ttk, filedialog
import math
import time
from PIL import Image, ImageTk , ImageGrab

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
        self.es_triangulo = False
        self.ready_to_draw = False
        self.tipo = tk.IntVar(value=0)
        

        # Frame opciones
        self.frame_options = tk.Frame(self.master, width=700, height=100)
        self.frame_options.config(bg='red')
        self.frame_options.pack()

        # Boton linea
        self.img_linea = ImageTk.PhotoImage(Image.open('./images/linea.png').resize((20,20)))
        self.boton_linea = tk.Button(self.frame_options, 
                                     width=20, height=20, 
                                     image=self.img_linea, 
                                     command= self.set_linea, 
                                     )
        self.boton_linea.pack(side='left')
    
        # Boton circulo
        self.img_circulo = ImageTk.PhotoImage(Image.open('./images/circulo.png').resize((17,17)))
        self.boton_circulo = tk.Button(self.frame_options, 
                                       width=20, height=20, 
                                       image=self.img_circulo, 
                                       command= self.set_circulo,
                                       )
        self.boton_circulo.pack(side='left')

        # Boton triangulo
        self.img_triangulo = ImageTk.PhotoImage(Image.open('./images/triangulo.png').resize((17,17)))
        self.boton_triangulo = tk.Button(self.frame_options, 
                                       width=20, height=20, 
                                       image=self.img_triangulo, 
                                       command= self.set_triangulo,
                                       )
        self.boton_triangulo.pack(side='left')

        # Combo box tipo
        self.tipo_linea = ['Normal', 'Segmentado']
        self.cmb_str = tk.StringVar(value=self.tipo_linea[0])
        self.cmb_tipo = ttk.Combobox(self.frame_options, 
                                     values=self.tipo_linea, 
                                     textvariable=self.cmb_str,
                                     width=12)
        self.cmb_tipo.pack(side='left')

        # Spin box grosor
        self.grosor_linea = [x for x in range(1,11)]
        self.spn_int = tk.IntVar(value=self.grosor_linea[0])
        self.spb_grosor = ttk.Spinbox(self.frame_options, 
                                      from_=1, to=10, 
                                      increment=1, 
                                      textvariable=self.spn_int,
                                      width=3)
        self.spb_grosor.pack(side='left')

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
        self.canvas = tk.Canvas(self.frame_canva, width=700, height=500)
        self.canvas.pack()
        self.canvas.config(bg="white")

        # Eventos
        self.canvas.bind('<Button-1>', self.handle_click)
        self.master.bind('<Escape>', self.event_scape)
        self.cmb_tipo.bind('<<ComboboxSelected>>', self.escoger_tipo)
        self.canvas.bind("<Button-3>", self.show_popup_menu)
        #self.spb_grosor.bind('<<Increment o Decrement :v>>')
        
        
        #Guardar imagen
        self.boton_guardar = tk.Button(self.frame_options, text='Guardar', command=self.guardar_imagen)
        self.boton_guardar.pack(side='left')
    
    
    
    def guardar_imagen(self):
        ruta = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
        if ruta:
        # Captura la pantalla del lienzo y guarda la imagen
            x = self.master.winfo_rootx() + self.frame_canva.winfo_x()
            y = self.master.winfo_rooty() + self.frame_canva.winfo_y()
            x1 = x + self.frame_canva.winfo_width()
            y1 = y + self.frame_canva.winfo_height()
            ImageGrab.grab().crop((x, y, x1, y1)).save(ruta)
        
        
    def trasladar(self, dx, dy):
        for i in range(len(self.puntos)):
            self.puntos[i] = (self.puntos[i][0] + dx, self.puntos[i][1] + dy)
        self.redibujar()

    def escalar(self, sx, sy):
        for i in range(len(self.puntos)):
            self.puntos[i] = (self.puntos[i][0] * sx, self.puntos[i][1] * sy)
        self.redibujar()

    def rotar(self, theta):
        theta = math.radians(theta)
        for i in range(len(self.puntos)):
            x = self.puntos[i][0] * math.cos(theta) - self.puntos[i][1] * math.sin(theta)
            y = self.puntos[i][0] * math.sin(theta) + self.puntos[i][1] * math.cos(theta)
            self.puntos[i] = (x, y)
        self.redibujar()

    def redibujar(self):
        self.canvas.delete('all')  # Elimina todos los elementos del lienzo
        for punto in self.puntos:
            x, y = punto
            self.canvas.create_oval(x, y, x+1, y+1, fill=self.color.get())  # Dibuja un punto en el lienzo
        
        
    def color_picker(self):
        self.color.set(colorchooser.askcolor()[1])
        if self.color.get() == 'None':
            self.color.set(value='black')
        
    def escoger_tipo(self, event):
        self.tipo.set(self.cmb_tipo.current()) 

    def event_scape(self, event):
        self.es_circulo=False
        self.es_linea=False
        self.es_triangulo=False
        self.boton_circulo.config(bg='misty rose')
        self.boton_linea.config(bg='misty rose')
        self.boton_triangulo.config(bg='misty rose')

    def set_linea(self):
        self.puntos.clear()
        self.es_circulo=False ; self.es_triangulo=False
        self.es_linea=True
        self.boton_linea.config(bg='#ffff80')
        self.boton_circulo.config(bg='misty rose')
        self.boton_triangulo.config(bg='misty rose')
    
    def set_circulo(self):
        self.puntos.clear()
        self.es_linea=False ; self.es_triangulo=False
        self.es_circulo=True
        self.boton_circulo.config(bg='#ffff80')
        self.boton_linea.config(bg='misty rose')
        self.boton_triangulo.config(bg='misty rose')

    def set_triangulo(self):
        self.puntos.clear()
        self.es_linea=False
        self.es_triangulo=True
        self.es_circulo=False
        self.boton_triangulo.config(bg='#ffff80')
        self.boton_circulo.config(bg='misty rose')
        self.boton_linea.config(bg='misty rose')

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
        elif self.es_triangulo:
            self.puntos.append((x,y))
            if len(self.puntos) == 3:
                self.draw_triangle()
                #self.puntos.clear()

        print(self.puntos)
        if self.ready_to_draw:
            ruta = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
            if ruta:
                self.guardar_imagen(ruta)

    def draw_line(self):
        linea = self.Line(self.canvas) 
        p1,p2 = self.puntos
        linea.draw_line_bresenham(*p1,*p2, 
                                  color=self.color.get(), 
                                  tipo=self.tipo.get(), 
                                  grosor=self.spn_int.get()) 
        self.is_drawing=False
    
    def draw_circle(self):
        def calc_r(x1,y1,x2,y2):
            r = round(math.sqrt((x2-x1)**2 + (y2-y1)**2))
            return r
        circulo = self.Circle(self.canvas)
        p1,p2 = self.puntos
        circulo.draw_circle_bresenham(*p1, 
                                      calc_r(*p1, *p2), 
                                      color=self.color.get(), 
                                      tipo=self.tipo.get(), 
                                      grosor=self.spn_int.get())

    def draw_triangle(self):
        linea = self.Line(self.canvas)
        p1,p2,p3 = self.puntos
        linea.draw_line_bresenham(*p1,*p2, color=self.color.get(), tipo=self.tipo.get(), grosor=self.spn_int.get())
        linea.draw_line_bresenham(*p2,*p3, color=self.color.get(), tipo=self.tipo.get(), grosor=self.spn_int.get())
        linea.draw_line_bresenham(*p3,*p1, color=self.color.get(), tipo=self.tipo.get(), grosor=self.spn_int.get())
    def show_popup_menu(self, event):
        menu = tk.Menu(self.master, tearoff=0)
        menu.add_command(label="Rellenar Triangulo", command=self.rellenar_triangulo)
        menu.add_command(label="Salir", command=self.master.quit)
        menu.post(event.x_root, event.y_root)

    def rellenar_triangulo(self):
        color = self.color.get()

    # Obtener los puntos del triángulo desde self.puntos
        p1 = self.puntos[0]
        p2 = self.puntos[1]
        p3 = self.puntos[2]

    # Obtener los límites verticalmente del triángulo
        y_min = min(p1[1], p2[1], p3[1])
        y_max = max(p1[1], p2[1], p3[1])

    # Crear una lista para almacenar los bordes del triángulo
        edges = []

    # Agregar las tres líneas del triángulo a la lista de bordes
        edges.append((p1, p2))
        edges.append((p2, p3))
        edges.append((p3, p1))

    # Ordenar las líneas por su coordenada y
        edges.sort(key=lambda edge: edge[0][1])

    # Crear una lista para almacenar los bordes activos
        active_edges = []

    # Iterar sobre cada línea horizontal del triángulo
        for y in range(y_min, y_max + 1):
        # Eliminar los bordes activos cuyo y máximo sea menor o igual a y
            active_edges = [edge for edge in active_edges if edge[1][1] > y]

        # Agregar los bordes activos correspondientes a esta línea
            for edge in edges:
                if edge[0][1] <= y < edge[1][1] or edge[1][1] <= y < edge[0][1]:
                    active_edges.append(edge)

        # Ordenar los bordes activos por su coordenada x del punto de intersección con y
            active_edges.sort(key=lambda edge: (edge[0][0] + (edge[1][0] - edge[0][0]) *
                                             (y - edge[0][1]) / (edge[1][1] - edge[0][1])))

        # Iterar sobre cada par de bordes activos para pintar la línea horizontal
            for i in range(0, len(active_edges), 2):
                if i + 1 < len(active_edges):  # Verificar si hay suficientes elementos en active_edges
                    x_start = int(active_edges[i][0][0] + (y - active_edges[i][0][1]) *
                                (active_edges[i][1][0] - active_edges[i][0][0]) /
                                (active_edges[i][1][1] - active_edges[i][0][1]))
                    x_end = int(active_edges[i + 1][0][0] + (y - active_edges[i + 1][0][1]) *
                                (active_edges[i + 1][1][0] - active_edges[i + 1][0][0]) /
                                (active_edges[i + 1][1][1] - active_edges[i + 1][0][1]))

                # Pintar la línea horizontal entre los puntos de intersección
                for x in range(x_start, x_end + 1):
                    self.canvas.create_rectangle(x, y, x + 1, y + 1, fill=color, outline=color)
                    self.master.update()    
            # Opcional: Pintar los píxeles individuales
            # for x in range(x_start, x_end + 1):
            #     self.draw_pixel(x, y, color=color)

    # Limpiar los bordes activos
        active_edges.clear()
    class Line():
        def __init__(self, canva) -> None:
            self.canvas = canva
            self.segment = 15

        def draw_pixel(self, x, y, color="black", grosor=1):
            x1, y1 = (x,y)
            x2, y2 = ((x+grosor), (y+grosor))
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, width=0)        
                
        def draw_line_basic(self, x0, y0, x1, y1):
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

        def draw_line_bresenham(self, x0, y0, x1, y1, color="black", tipo=0, grosor=1):
            dx = abs(x1 - x0) 
            dy = abs(y1 - y0) 
            sx = -1 if x0 > x1 else 1
            sy = -1 if y0 > y1 else 1
            err = dx - dy
            while x0 != x1 or y0 != y1:
                if tipo == 1:
                    if self.segment == 0: self.segment = 15
                    if self.segment > 5:
                        self.draw_pixel(x0, y0, color=color, grosor=grosor)
                    self.segment-=1
                else:
                    self.draw_pixel(x0, y0, color=color, grosor=grosor)
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
            self.segment = 15

        def draw_pixel(self, x, y, color="black", grosor=1):
            x1, y1 = (x,y)
            x2, y2 = ((x+grosor), (y+grosor))
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, width=0)

        def draw_circle_basic(self, xc, yc, r):
            for x in range(xc - r, xc + r ):  #200 200 100      100, 100   
                y_positivo = yc + int((r ** 2 - (x - xc) **  2) ** 0.5)
                y_negativo = yc - int((r ** 2 - (x - xc) ** 2) ** 0.5)
                self.draw_pixel(x, y_positivo)
                self.draw_pixel(x, y_negativo)

        def draw_circle_polar(self, xc, yc, r):
            for i in range(360):
                sin_values = r * math.sin(i * math.pi / 180)
                cos_values = r * math.cos(i * math.pi / 180) 
                x = xc + cos_values
                y = yc + sin_values
                self.draw_pixel(round(x), round(y))  
  
        def draw_circle_bresenham(self, x_center, y_center, r, color="black", tipo=0, grosor=1):
            def draw():
                self.draw_pixel(x_center + x, y_center + y, color=color, grosor=grosor)
                self.draw_pixel(x_center - x, y_center + y, color=color, grosor=grosor)
                self.draw_pixel(x_center + x, y_center - y, color=color, grosor=grosor)
                self.draw_pixel(x_center - x, y_center - y, color=color, grosor=grosor)
                self.draw_pixel(x_center + y, y_center + x, color=color, grosor=grosor)
                self.draw_pixel(x_center - y, y_center + x, color=color, grosor=grosor)
                self.draw_pixel(x_center + y, y_center - x, color=color, grosor=grosor)
                self.draw_pixel(x_center - y, y_center - x, color=color, grosor=grosor)
            x = 0
            y = r
            p = 1 - r

            while x <= y:
                if tipo == 1:
                    if self.segment == 0: self.segment = 15
                    if self.segment > 5:
                        draw()
                    self.segment-=1
                else:
                    draw()
                x += 1
                if p <= 0:
                    p = p + 2 * x + 1;
                else:
                    y -= 1
                    p = p + 2 * (x - y) + 1

if __name__ == "__main__":
    root = tk.Tk()
    my_gui = Gui(root)
    root.title('Mi Paint')
    root.iconbitmap(bitmap='./images/tortuga.ico')
    root.mainloop()
