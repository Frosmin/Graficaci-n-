import customtkinter as ctk
import tkinter as tk
from tkinter import colorchooser, simpledialog
import math
from PIL import Image, ImageGrab
import os

class Gui:
    def __init__(self, master) -> None:
        self.master = master
        self.master.geometry('700x500')

        # Color
        self.color = ctk.StringVar(value='black')

        # Otras variables
        self.puntos = list()
        self.es_linea = False 
        self.es_circulo = False
        self.es_triangulo = False
        self.ready_to_draw = False
        self.tipo = ctk.IntVar(value=0)
        self.lista_elementos= list()
        self.lista_elementos_nombre = list()
        self.elemento_num = 1
        self.current_object = None  # ver que elemento esta seleccionado
        
        self.figura_seleccionada = None

        # Frame opciones
        self.frame_options = ctk.CTkFrame(self.master, width=700, height=100)
        #self.frame_options.configure(fg_color='red')
        self.frame_options.pack()

        # Boton linea
        self.img_linea = ctk.CTkImage(light_image=Image.open('./images/linea.png').resize((20,20)))
        self.boton_linea = ctk.CTkButton(self.frame_options, 
                                     width=20, height=20,
                                     corner_radius=5, 
                                     image=self.img_linea,
                                     text="",
                                     fg_color='misty rose',
                                     hover_color='#00ffff',
                                     command= self.set_linea, 
                                     border_width=1
                                     )
        self.boton_linea.pack(side='left')

        # Boton circulo
        self.img_circulo = ctk.CTkImage(light_image=Image.open('./images/circulo.png').resize((17,17)))
        self.boton_circulo = ctk.CTkButton(self.frame_options, 
                                     width=20, height=20,
                                     corner_radius=5, 
                                     image=self.img_circulo,
                                     text="",
                                     fg_color='misty rose',
                                     hover_color='#00ffff',
                                     command= self.set_circulo, 
                                     border_width=1
                                     )
        self.boton_circulo.pack(side='left')

        # Boton triangulo
        self.img_triangulo = ctk.CTkImage(light_image=Image.open('./images/triangulo.png').resize((19,19)))
        self.boton_triangulo = ctk.CTkButton(self.frame_options, 
                                     width=20, height=20,
                                     corner_radius=5, 
                                     image=self.img_triangulo,
                                     text="",
                                     fg_color='misty rose',
                                     hover_color='#00ffff',
                                     command= self.set_triangulo, 
                                     border_width=1
                                     )
        self.boton_triangulo.pack(side='left')

        # Combo box tipo
        self.tipo_linea = ['Normal', 'Segmentado']
        self.cmb_str = ctk.StringVar(value=self.tipo_linea[0])
        self.cmb_tipo = ctk.CTkComboBox(self.frame_options, 
                                     values=self.tipo_linea, 
                                     variable=self.cmb_str,
                                     width=120,
                                     corner_radius=5, 
                                     border_width=1,
                                     command= self.update_tipo,
                                     )
        self.cmb_tipo.pack(side='left')
    
        # Slider grosor 
        self.sld_int = ctk.IntVar(value=1)
        self.slider_grosor = ctk.CTkSlider(self.frame_options, 
                                           width=100,
                                           from_=1, to=10, 
                                           number_of_steps=9,
                                           command= self.update_grosor,
                                           )
        self.slider_grosor.pack(side='left')
        
        # Color selector
        self.boton_color = ctk.CTkButton(self.frame_options,
                                         width=100,
                                         corner_radius=5, 
                                         text='Choose color', 
                                         fg_color='misty rose',
                                         hover_color='#00ffff',
                                         command=self.color_picker,
                                         border_width=1,
                                         text_color='black'
                                         )
        self.boton_color.pack(side='left')

        # Combo box elementos
        self.cmb_elem = ctk.StringVar()
        self.cmb_elementos = ctk.CTkComboBox(self.frame_options, 
                                     values=self.lista_elementos, 
                                     variable=self.cmb_elem,
                                     width=120,
                                     corner_radius=5, 
                                     border_width=1,
                                     command=self.update_current
                                     )
        self.cmb_elementos.pack(side='left')

        # Frame Lienzo
        self.frame_canva = ctk.CTkFrame(self.master, width=700, height=400)
        self.frame_canva.configure(fg_color='yellow')
        self.frame_canva.pack()

        # Crear un lienzo (canvas)
        self.canvas = ctk.CTkCanvas(self.frame_canva, width=700, height=500)
        self.canvas.pack()
        self.canvas.config(bg="white")

        # Eventos
        self.canvas.bind('<Button-1>', self.handle_click)
        self.master.bind('<Escape>', self.event_scape)
        self.canvas.bind("<Button-3>", self.show_popup_menu)
        
        
        
    def escalar(self):
        # Muestra una ventana emergente para obtener sx
        aumento = simpledialog.askfloat("Escalar", "Introduce el valor de sx")  #ver que sea entero
        if aumento is None:  # Si el usuario canceló la ventana emergente
            return

        
        if isinstance(self.current_object, self.Triangulo):
                print("es triangulo")
                print (f"Escalando {self.current_object.puntos} con aumento={aumento}")
                puntos = self.current_object.puntos

                # Calcular el punto medio del triángulo
                punto_medio = ((puntos[0][0] + puntos[1][0] + puntos[2][0]) // 3, 
                            (puntos[0][1] + puntos[1][1] + puntos[2][1]) // 3)

               
                # Escalar los puntos del triángulo respecto al punto medio y redondear los resultados
        
                puntos_escalados = [tuple(round(punto_medio[i] + aumento * (valor - punto_medio[i])) for i, valor in enumerate(punto)) for punto in puntos]
                print(puntos_escalados)  # Imprime los puntos del triángulo escalado

                self.current_object.delete()
                
                

                # Dibujar el triángulo escalado
                self.current_object.draw(*puntos_escalados[0], *puntos_escalados[1], *puntos_escalados[2],
                                        color=self.color.get(), 
                                        tipo=self.cmb_tipo.get(), 
                                        grosor=self.slider_grosor.get())
                
                self.current_object.puntos = puntos_escalados
                        
                        
            
            
            
        
        if isinstance(self.current_object, self.Circle):
            print("es circulo")
            print (f"Escalando {self.current_object.puntos} con aumento={aumento}")
            puntos = self.current_object.puntos
            print (puntos[0][0] + aumento)
            
            p1 = self.current_object.puntos[0] #centro
            p2 = self.current_object.puntos[1]
            
            p2 = tuple(valor * aumento for valor in p2)
            
            self.current_object.delete()
            self.current_object.draw(*p1, *p2,
                                     color=self.color.get(), 
                                     tipo=self.cmb_tipo.get(), 
                                     grosor=self.slider_grosor.get())
            
            self.current_object.puntos = [p1,p2]
            
            
            
                        
        
        if isinstance(self.current_object, self.Line):
            print("es linea")
            print (f"Escalando {self.current_object.puntos} con aumento={aumento}")
            # p1 = self.current_object.puntos[0]
            # p2 = self.current_object.puntos[1]

            # p1= tuple(valor + aumento for valor in p1)
            # p2 = tuple(valor + aumento for valor in p2)
            
            puntos = self.current_object.puntos
            # puntos_aumentados = [tuple(valor + aumento for valor in punto) for punto in puntos]
            
            # # print(p1)
            # # print(p2)
            # #self.current_object.puntos = [p1,p2]
            
            # Calcular el punto medio de la línea
            punto_medio = ((puntos[0][0] + puntos[1][0]) // 2, (puntos[0][1] + puntos[1][1]) // 2)

            # Definir el factor de escala
            escala = aumento  # Cambia esto al valor que quieras

            # Escalar los puntos de la línea respecto al punto medio
            puntos_escalados = [tuple(punto_medio[i] + escala * (valor - punto_medio[i]) for i, valor in enumerate(punto)) for punto in puntos]

            print(puntos_escalados)  # Imprime los puntos de la línea escalada
            #print(self.current_object.puntos)
            self.current_object.delete()
            # print(puntos_aumentados)
            
            # Dibujar el triángulo escalado
            self.current_object.draw(*puntos_escalados[0], *puntos_escalados[1], *puntos_escalados[2],
                                    color=self.color.get(), 
                                    tipo=self.cmb_tipo.get(), 
                                    grosor=self.slider_grosor.get())
            
            self.current_object.puntos = puntos_escalados
            
           
    
    
    
    
    def guardar_imagen(self):
        ruta = tk.filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
        if ruta:
        # Captura la pantalla del lienzo y guarda la imagen
            x = self.master.winfo_rootx() + self.frame_canva.winfo_x()
            y = self.master.winfo_rooty() + self.frame_canva.winfo_y()
            x1 = x + self.frame_canva.winfo_width()
            y1 = y + self.frame_canva.winfo_height()
            ImageGrab.grab().crop((x, y, x1, y1)).save(ruta)
            image = Image.open(f'{ruta}')
            print(os.path.basename(ruta))
            image.show(title=f'{os.path.basename(ruta)}')
        
    def trasladar(self, dx, dy):
        for i in range(len(self.puntos)):
            self.puntos[i] = (self.puntos[i][0] + dx, self.puntos[i][1] + dy)
        self.redibujar()

   
    def rotar(self, theta):
        theta = math.radians(theta)
        for i in range(len(self.puntos)):
            x = self.puntos[i][0] * math.cos(theta) - self.puntos[i][1] * math.sin(theta)
            y = self.puntos[i][0] * math.sin(theta) + self.puntos[i][1] * math.cos(theta)
            self.puntos[i] = (x, y)
        self.redibujar()

    def redibujar(self):
        # Borra todas las figuras del canvas
        self.canvas.delete("all")

        # Dibuja la figura seleccionada
        if self.figura_seleccionada:
            puntos = self.figura_seleccionada
            for i in range(len(puntos) - 1):
                self.canvas.create_line(puntos[i][0], puntos[i][1], puntos[i+1][0], puntos[i+1][1])

    def handle_click(self, event = None):
        x , y = int(event.x) , int(event.y)
        self.figura_seleccionada = self.puntos

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
                self.puntos.clear()
        

        print(self.puntos)

    def event_scape(self, event):
        self.es_circulo=False
        self.es_linea=False
        self.es_triangulo=False
        self.boton_circulo.configure(fg_color='misty rose')
        self.boton_linea.configure(fg_color='misty rose')
        self.boton_triangulo.configure(fg_color='misty rose')

    def set_linea(self):
        self.puntos.clear()
        self.es_circulo=False ; self.es_triangulo=False
        self.es_linea=True
        self.boton_linea.configure(fg_color='#99ccff')
        self.boton_circulo.configure(fg_color='misty rose')
        self.boton_triangulo.configure(fg_color='misty rose')

    def set_circulo(self):
        self.puntos.clear()
        self.es_linea=False ; self.es_triangulo=False
        self.es_circulo=True
        self.boton_circulo.configure(fg_color='#99ccff')
        self.boton_linea.configure(fg_color='misty rose')
        self.boton_triangulo.configure(fg_color='misty rose')

    def set_triangulo(self):
        self.puntos.clear()
        self.es_linea=False
        self.es_triangulo=True
        self.es_circulo=False
        self.boton_triangulo.configure(fg_color='#99ccff')
        self.boton_circulo.configure(fg_color='misty rose')
        self.boton_linea.configure(fg_color='misty rose')

    def update_grosor(self, event):
        self.update_element()

    def update_tipo(self, event):
        self.update_element()

    def color_picker(self):
        self.color.set(colorchooser.askcolor()[1])
        if self.color.get() == 'None':
            self.color.set(value='black')

        self.update_element()
   
    def draw_line(self):
        linea = self.Line(self.canvas) 
        p1,p2 = self.puntos[0], self.puntos[1]
        linea.save_puntos(*p1,*p2)
        linea.draw(*p1,*p2, 
                    color=self.color.get(), 
                    tipo=self.cmb_tipo.get(), 
                    grosor=self.slider_grosor.get())
        linea.id = f"{self.elemento_num}. Linea" 
        self.lista_elementos.append(linea)
        self.lista_elementos_nombre.append(linea.id)
        self.elemento_num+=1

        self.cmb_elementos.set(value=linea.id)
        self.cmb_elementos.configure(values=self.lista_elementos_nombre)
        self.current_object = linea
        #print(self.cmb_elementos.get())

    def draw_circle(self):
        circulo = self.Circle(self.canvas)
        p1,p2 = self.puntos[0], self.puntos[1]
        circulo.save_puntos(*p1,*p2)
        circulo.draw(*p1, *p2, 
                      color=self.color.get(), 
                      tipo=self.cmb_tipo.get(), 
                      grosor=self.slider_grosor.get()
                      ) 
        circulo.id = f"{self.elemento_num}. Circulo "
        self.lista_elementos.append(circulo)
        self.lista_elementos_nombre.append(circulo.id)
        self.elemento_num+=1

        self.cmb_elementos.set(value=circulo.id)
        self.cmb_elementos.configure(values=self.lista_elementos_nombre)
        self.current_object= circulo
        #print(self.cmb_elementos.get())
    
    def draw_triangle(self):
        triangulo = self.Triangulo(self.canvas)
        p1,p2,p3 = self.puntos[0], self.puntos[1], self.puntos[2]
        triangulo.draw(*p1,*p2,*p3,
                        color=self.color.get(), 
                        tipo=self.cmb_tipo.get(), 
                        grosor=self.slider_grosor.get()
                        )
        triangulo.id = f"{self.elemento_num}. Triangulo"
        self.lista_elementos.append(triangulo)
        self.lista_elementos_nombre.append(triangulo.id)
        self.elemento_num+=1

        self.cmb_elementos.set(value=triangulo.id)
        self.cmb_elementos.configure(values=self.lista_elementos_nombre)
        self.current_object= triangulo
        #print(self.cmb_elementos.get())

    def update_current(self, event):
        current_id = int(self.cmb_elementos.get().split('.')[0]) - 1
        self.current_object = self.lista_elementos[current_id]
        print(self.current_object)
        
    def update_element(self):
        self.current_object.delete()
        if isinstance(self.current_object, self.Triangulo):
            p1 = self.current_object.puntos[0] 
            p2 = self.current_object.puntos[1]
            p3 = self.current_object.puntos[2]
            self.current_object.draw(*p1,*p2,*p3,
                                    color=self.color.get(), 
                                    tipo=self.cmb_tipo.get(), 
                                    grosor=self.slider_grosor.get()
                                    )
        elif isinstance(self.current_object, self.Circle):
            p1 = self.current_object.puntos[0]
            p2 = self.current_object.puntos[1]
            self.current_object.draw(*p1, *p2, 
                                     color=self.color.get(), 
                                     tipo=self.cmb_tipo.get(), 
                                     grosor=self.slider_grosor.get()
                                     )
        elif isinstance(self.current_object, self.Line):
            p1 = self.current_object.puntos[0]
            p2 = self.current_object.puntos[1]
            self.current_object.draw(*p1,*p2,
                                     color=self.color.get(),
                                     tipo=self.cmb_tipo.get(), 
                                     grosor=self.slider_grosor.get()
                                     )

    def delete(self):
        self.current_object.delete()

    def show_popup_menu(self, event):
        menu = tk.Menu(self.master, tearoff=0)
        menu.add_command(label="Trasladar")
        menu.add_command(label="Rellenar Triangulo", command=self.rellenar_triangulo)
        menu.add_command(label="Actualizar elemento", command=self.update_element)
        menu.add_command(label="Eliminar elemento", command=self.delete)
        menu.add_command(label="Save", command= self.guardar_imagen)
        menu.add_command(label="Limpiar", command=lambda: self.canvas.delete('all'))
        menu.add_command(label="Escalar", command=self.escalar)
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
                    #self.master.update()    
            # Opcional: Pintar los píxeles individuales
            # for x in range(x_start, x_end + 1):
            #     self.draw_pixel(x, y, color=color)

    # Limpiar los bordes activos
        active_edges.clear()

    class Line():
        def __init__(self, canva) -> None:
            self.canvas = canva
            self.segment = 15
            self.puntos = list()
            self.id = None
            self.grosor = 1

        def save_puntos(self, *args):
            x,y,z,w = args
            self.puntos.append((x,y))
            self.puntos.append((z,w))

        def draw_pixel(self, x, y, color="black", grosor=1):
            x1, y1 = (x,y)
            x2, y2 = ((x+grosor), (y+grosor))
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, width=0)              

        # def draw_line_bresenham
        def draw(self, x0, y0, x1, y1, color="black", tipo='Normal', grosor=1):
            self.grosor=grosor
            dx = abs(x1 - x0) 
            dy = abs(y1 - y0) 
            sx = -1 if x0 > x1 else 1
            sy = -1 if y0 > y1 else 1
            err = dx - dy
            while x0 != x1 or y0 != y1:
                if tipo == "Segmentado":
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

        def delete(self):
            self.draw(*self.puntos[0], *self.puntos[1], color="white",grosor=self.grosor)

        def __str__(self) -> str:
            return f"Hola soy la linea {self.id}"

    class Circle():
        def __init__(self, canva) -> None:
            self.canvas = canva
            self.segment = 15
            self.puntos = list()
            self.id = None
            self.grosor = 1

        def save_puntos(self, *args):
            x,y,z,w = args
            self.puntos.append((x,y))
            self.puntos.append((z,w))

        def calc_r(self,x1,y1,x2,y2):
            r = round(math.sqrt((x2-x1)**2 + (y2-y1)**2))
            return r

        def draw_pixel(self, x, y, color="black", grosor=1):
            x1, y1 = (x,y)
            x2, y2 = ((x+grosor), (y+grosor))
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, width=0)
  
        # def draw_circle_bresenham 
        def draw(self, x_center, y_center, x2, y2, color="black", tipo='Normal', grosor=1):
            self.grosor=grosor
            r = self.calc_r(x_center, y_center, x2, y2)
            def _draw():
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
                if tipo == 'Segmentado':
                    if self.segment == 0: self.segment = 15
                    if self.segment > 5:
                        _draw()
                    self.segment-=1
                else:
                    _draw()
                x += 1
                if p <= 0:
                    p = p + 2 * x + 1;
                else:
                    y -= 1
                    p = p + 2 * (x - y) + 1

        def delete(self):
            self.draw(*self.puntos[0], *self.puntos[1],color="white", tipo="Normal", grosor=self.grosor)

        def __str__(self) -> str:
            return f"Hola soy el circulo {self.id}"
        
    class Triangulo(Line):
        def __init__(self, canva) -> None:
            super().__init__(canva)
            self.puntos = list()
            self.id = None
            self.grosor = 1

        def draw(self,x1,y1,x2,y2,x3,y3,color='black',tipo='Normal',grosor=1):
            self.grosor=grosor
            self.puntos.append((x1,y1))
            self.puntos.append((x2,y2))
            self.puntos.append((x3,y3))
            super().draw(x1,y1,x2,y2, color=color, tipo=tipo, grosor=grosor)
            super().draw(x2,y2,x3,y3, color=color, tipo=tipo, grosor=grosor)
            super().draw(x3,y3,x1,y1, color=color, tipo=tipo, grosor=grosor)

        def delete(self):
            super().draw(*self.puntos[0],*self.puntos[1], color='white', tipo='Normal', grosor=self.grosor)
            super().draw(*self.puntos[1],*self.puntos[2], color='white', tipo='Normal', grosor=self.grosor)
            super().draw(*self.puntos[2],*self.puntos[0], color='white', tipo='Normal', grosor=self.grosor)
           
        def __str__(self) -> str:
            return f"Hola soy el triangulo {self.id}"

if __name__ == "__main__":
    root = ctk.CTk()
    my_gui = Gui(root)
    root.title('Mi Paint')
    root.iconbitmap(bitmap='./images/tortuga.ico')
    root.mainloop()
 