#/usr/bin/env python3

import tkinter as tk
from tkinter import colorchooser, ttk, filedialog
import math
import time
from PIL import Image, ImageTk , ImageGrab
import tkinter.simpledialog as simpledialog


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
        
        
        #escalar
       #escalar
        # self.entrada_sx = tk.Entry(self.frame_options)
        # self.entrada_sx.pack(side='left')
        # self.entrada_sy = tk.Entry(self.frame_options)
        # self.entrada_sy.pack(side='left')
        self.boton_escalar = tk.Button(self.frame_options, text='Escalar', command=lambda: self.escalar())
        self.boton_escalar.pack(side='left')
        
        self.figuras = [] 
        
        self.boton_borrar = tk.Button(self.frame_options, text="Borrar", command=self.borrar)
        self.boton_borrar.pack(side='left')
        
        self.xd = tk.Button(self.frame_options, text="verlista", command=self.ver_lista)
        self.xd.pack(side='left')


    def ver_lista(self):
        for figura in self.figuras:
            print(figura)    
    
    
    def borrar_ultimo(self):
        if self.figuras:
            self.figuras.pop()
            self.redibujar()
    
    
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

        
    def escalar(self):
        # Muestra una ventana emergente para obtener sx
        sx = simpledialog.askfloat("Escalar", "Introduce el valor de sx")
        if sx is None:  # Si el usuario canceló la ventana emergente
            return

        # Muestra una ventana emergente para obtener sy
        sy = simpledialog.askfloat("Escalar", "Introduce el valor de sy")
        if sy is None:  # Si el usuario canceló la ventana emergente
            return

        print(f"Escalar llamado con sx={sx}, sy={sy}")
        if self.figuras:  # Comprueba si hay figuras en la lista
            # Escala la última figura
            figura = self.figuras[-1]
            # Calcula el centro de la figura
            cx = sum(punto[0] for punto in figura) / len(figura)
            cy = sum(punto[1] for punto in figura) / len(figura)
            # Aplica la escala con respecto al centro de la figura
            self.figuras[-1] = [((punto[0] - cx) * sx + cx, (punto[1] - cy) * sy + cy) for punto in figura]
            self.redibujar()

    def borrar(self):
        if self.figuras:  # Comprueba si hay figuras en la lista
            # Elimina la última figura
            self.figuras.pop()
            # Guarda el color actual
            color_actual = self.color.get()
            # Cambia el color a blanco
            self.color.set('white')
            # Redibuja las figuras
            self.redibujar()
            # Restablece el color original
            self.color.set(color_actual)
    
            
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

        p1 = self.puntos[0]
        p2 = self.puntos[1]
        p3 = self.puntos[2]

        y_min = min(p1[1], p2[1], p3[1])
        y_max = max(p1[1], p2[1], p3[1])

        edges = []

        edges.append((p1, p2))
        edges.append((p2, p3))
        edges.append((p3, p1))

        edges.sort(key=lambda edge: edge[0][1])

        active_edges = []

        for y in range(y_min, y_max + 1):
            active_edges = [edge for edge in active_edges if edge[1][1] > y]

            for edge in edges:
                if edge[0][1] <= y < edge[1][1] or edge[1][1] <= y < edge[0][1]:
                    active_edges.append(edge)

            active_edges.sort(key=lambda edge: (edge[0][0] + (edge[1][0] - edge[0][0]) *
                                             (y - edge[0][1]) / (edge[1][1] - edge[0][1])))

            for i in range(0, len(active_edges), 2):
                if i + 1 < len(active_edges):  
                    x_start = int(active_edges[i][0][0] + (y - active_edges[i][0][1]) *
                                (active_edges[i][1][0] - active_edges[i][0][0]) /
                                (active_edges[i][1][1] - active_edges[i][0][1]))
                    x_end = int(active_edges[i + 1][0][0] + (y - active_edges[i + 1][0][1]) *
                                (active_edges[i + 1][1][0] - active_edges[i + 1][0][0]) /
                                (active_edges[i + 1][1][1] - active_edges[i + 1][0][1]))

                # Pintar la línea horizontal entre los puntos de intersección
                for x in range(x_start, x_end + 1):
                    self.canvas.create_rectangle(x, y, x + 1, y + 1, fill=color, outline=color)
                

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
