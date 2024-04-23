import colorsys
import copy
import subprocess
from circulo import Circle
from triangulo import Triangulo
from linea import Line

import customtkinter as ctk
import tkinter as tk
from tkinter import NW, colorchooser
import math
from PIL import Image, ImageGrab, ImageTk
import os

class Gui:
    def __init__(self, master) -> None:
        
        self.master = master
        self.master.geometry('700x700')

        # Color
        self.color = ctk.StringVar(value='#000000')
        self.colorBorde = ctk.StringVar(value='#000000')

        # Otras variables
        self.puntos = list()
        self.es_linea = False 
        self.es_circulo = False
        self.es_triangulo = False
        self.ready_to_draw = False
        self.tipo = ctk.IntVar(value=0)
        self.lista_elementos = list()
        self.lista_elementos_nombre = list()
        self.current_object = None
        self.para_mover=False
        self.para_escala=False
        self.para_rotar=False
        self.n_escala = 1
        self.theta_rotacion=float()


        # Frame opciones
        self.frame_options = ctk.CTkFrame(self.master)
        #self.frame_options.configure(fg_color='red')
        # al usar pack reduce el size a sus hijos
        self.frame_options.pack()

        # Boton linea
        self.img_linea = ctk.CTkImage(light_image=Image.open('./images/linea.png').resize((20,20)))
        self.boton_linea = ctk.CTkButton(
            self.frame_options, 
            width=20, height=20,
            corner_radius=8, 
            image=self.img_linea,
            text="",
            fg_color='misty rose',
            hover_color="#00ffff",
            command= self.set_linea, 
            border_width=2
        )
        self.boton_linea.pack(side='left', padx=5, pady=5)

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
            border_width=2
        )
        self.boton_circulo.pack(side='left', padx=5, pady=5)

        # Boton triangulo
        self.img_triangulo = ctk.CTkImage(light_image=Image.open('./images/triangulo.png').resize((19,19)))
        self.boton_triangulo = ctk.CTkButton(
            self.frame_options, 
            width=20, height=20,
            corner_radius=5, 
            image=self.img_triangulo,
            text="",
            fg_color='misty rose',
            hover_color='#00ffff',
            command= self.set_triangulo, 
            border_width=2
        )
        self.boton_triangulo.pack(side='left', padx=5, pady=5)
        
        # Combo box tipo delineado
        self.tipo_linea = ['Normal', 'Segmentado']
        self.cmb_str = ctk.StringVar(value=self.tipo_linea[0])
        self.cmb_tipo = ctk.CTkComboBox(
            self.frame_options, 
            values=self.tipo_linea, 
            variable=self.cmb_str,
            width=120,
            corner_radius=8, 
            border_width=0,
            command= self.update_tipo,
            state='readonly'
        )
        self.cmb_tipo.pack(side='left', padx=5, pady=5)
    
        # Slider grosor delineado
        self.sld_int = ctk.IntVar(value=1)
        self.slider_grosor = ctk.CTkSlider(self.frame_options, 
                                           width=100,
                                           from_=1, to=10, 
                                           number_of_steps=10,
                                           command= self.update_grosor,
                                           )
        self.slider_grosor.pack(side='left', padx=5, pady=5)
        
        
        # Color picker relleno
        self.boton_color_relleno = ctk.CTkButton(
            self.frame_options,
            width=100,
            corner_radius=5,
            text='Color relleno',
            fg_color=self.color.get(),
            hover_color='#00ffff',
            command=lambda: self.color_picker(self.boton_color_relleno, self.color),
            border_width=1,
            text_color='#ffffff'
        )
        self.boton_color_relleno.pack(side='left', padx=5, pady=5)
        
        # Color picker borde
        self.boton_color_borde = ctk.CTkButton(
            self.frame_options,
            width=100,
            corner_radius=5,
            text='Color borde',
            fg_color=self.colorBorde.get(),
            hover_color='#00ffff',
            command=lambda: self.color_picker(self.boton_color_borde, self.colorBorde),
            border_width=1,
            text_color='#ffffff'
        )
        self.boton_color_borde.pack(side='left', padx=5, pady=5)
        
        # Combo box elementos
        self.cmb_elem = ctk.StringVar()
        self.cmb_elementos = ctk.CTkComboBox(
            self.frame_options, 
            values=self.lista_elementos, 
            variable=self.cmb_elem,
            width=120,
            corner_radius=5, 
            border_width=1,
            command=self.update_current,
            state='readonly'
        )
        self.cmb_elementos.pack(side='left')

        # Frame Lienzo
        self.frame_canva = ctk.CTkFrame(self.master, width=700, height=600)
        self.frame_canva.configure(fg_color='yellow')
        self.frame_canva.pack()

        # Crear un lienzo (canvas)
        self.canvas = ctk.CTkCanvas(self.frame_canva, width=700, height=600)

        #self.canvas.config(bg="#ffffff")

        # imagen donde dibujaremos todo
        self.imagen = Image.new("RGB", (700, 600), color=(255, 255, 255))
        self.imagen_tk = ImageTk.PhotoImage(self.imagen)
        self.canvas.create_image(0, 0, anchor=NW, image=self.imagen_tk)
        self.canvas.pack()
        
        # actualizar la imagen
        #self.imagen_tk.paste(self.imagen)
        #self.canvas.update()
        # Eventos
        self.canvas.bind('<Button-1>', self.handle_click)
        self.master.bind('<Escape>', self.event_scape)
        self.canvas.bind("<Button-3>", self.show_popup_menu)

    def guardar_imagen(self):
        ruta = tk.filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if ruta:
            if self.imagen.mode != "RGB":
                self.imagen = self.imagen.convert("RGB")
            self.imagen.save(ruta, format="PNG")
            print("Imagen guardada en:", ruta)
            rutaCorregida = os.path.normpath(ruta)
            print("Imagen guardada en carpeta:", rutaCorregida)
            #subprocess.Popen(f'explorer /select,"{rutaCorregida}"')
            
            im = Image.open(ruta)
            im.show()

    def handle_click(self, event):
        x , y = event.x, event.y
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
        elif self.para_mover:
            self.puntos.append((x,y))
            if len(self.puntos) == 2:
                self.mover()
                self.puntos.clear()
        elif self.para_escala:
            self.puntos.append((x,y))
            if len(self.puntos) == 1:
                self.escala()
                self.puntos.clear()
        elif self.para_rotar:
            self.puntos.append((x,y))
            if len(self.puntos) == 1:
                self.rotar()
                self.puntos.clear()
        print(self.puntos)

    def event_scape(self, event):
        self.es_circulo=False
        self.es_linea=False
        self.es_triangulo=False
        self.para_mover=False
        self.para_escala=False
        self.para_rotar=False
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

    def set_mover(self):
        self.puntos.clear()
        self.es_linea=False
        self.es_triangulo=False
        self.es_circulo=False
        self.boton_triangulo.configure(fg_color='misty rose')
        self.boton_circulo.configure(fg_color='misty rose')
        self.boton_linea.configure(fg_color='misty rose')
        self.para_mover=True

    def set_escala(self):
        self.puntos.clear()
        self.es_linea=False
        self.es_triangulo=False
        self.es_circulo=False
        self.para_mover=False
        self.para_rotar=False
        self.boton_triangulo.configure(fg_color='misty rose')
        self.boton_circulo.configure(fg_color='misty rose')
        self.boton_linea.configure(fg_color='misty rose')
        self.para_escala=True
        dialog = ctk.CTkInputDialog(text="Escada de:", title="Escala")
        self.n_escala = float(dialog.get_input())  
        #print(type(self.n_escala))
        #print(self.n_escala)

    def set_rotar(self):
        self.puntos.clear()
        self.es_linea=False
        self.es_triangulo=False
        self.es_circulo=False
        self.para_mover=False
        self.para_escala=False
        self.boton_triangulo.configure(fg_color='misty rose')
        self.boton_circulo.configure(fg_color='misty rose')
        self.boton_linea.configure(fg_color='misty rose')
        self.para_rotar=True
        dialog = ctk.CTkInputDialog(text="Ingrese ángulo de rotación:", title="Rotación")
        self.theta_rotacion = float(dialog.get_input())  
        
    def update_grosor(self, event):
        self.update_element()

    def update_tipo(self, event):
        self.update_element()

    def color_picker(self, button_caller, colorVar):
        nuevo_color = colorchooser.askcolor()[1]
        if nuevo_color:
            colorVar.set(nuevo_color)
        
        # para seleccionar el color de texto
        r = int(colorVar.get()[1:3], 16) / 255.0
        g = int(colorVar.get()[3:5], 16) / 255.0
        b = int(colorVar.get()[5:7], 16) / 255.0
        # Convertir color RGB a HSL
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        # Si la luminosidad es menor a 0.5, elige un color claro para el texto
        button_caller.configure(fg_color=colorVar.get(), text_color="#FFFFFF" if (l < 0.6 or s < 0.5) else "#000000")
        print("colores: ", self.color.get(), "; ", self.colorBorde.get())
        self.update_element()
   
    def draw_line(self):
        linea = Line(
            self.canvas,
            f"{len(self.lista_elementos)+1}. Linea",
            self.colorBorde.get(),
            self.cmb_tipo.get(),
            int(self.slider_grosor.get()),
            self.puntos[0],
            self.puntos[1]
        ) 
        
        linea.draw(self.imagen)
        self.imagen_tk.paste(self.imagen)
        self.canvas.update()
        
        self.lista_elementos.append(linea)
        self.lista_elementos_nombre.append(linea.id)

        self.cmb_elementos.set(value=linea.id)
        self.cmb_elementos.configure(values=self.lista_elementos_nombre)
        self.current_object = linea
    
    def draw_circle(self):
        centro, distancia = self.puntos[0], self.puntos[1]
        circulo = Circle(
            self.canvas,
            f"{len(self.lista_elementos)+1}. Circulo",
            self.color.get(),
            self.colorBorde.get(),
            self.cmb_tipo.get(),
            int(self.slider_grosor.get()),
            centro,
            self.distancia_entre_puntos(*centro, *distancia)
        )
        
        #circulo.save_puntos(*p1,*p2)
        circulo.draw(self.imagen)
        self.imagen_tk.paste(self.imagen)
        self.canvas.update()
        
        self.lista_elementos.append(circulo)
        self.lista_elementos_nombre.append(circulo.id)

        self.cmb_elementos.set(value=circulo.id)
        self.cmb_elementos.configure(values=self.lista_elementos_nombre)
        self.current_object= circulo
    
    def draw_triangle(self):
        triangulo = Triangulo(
            self.canvas,
            f"{len(self.lista_elementos)+1}. Triangulo",
            self.color.get(),
            self.colorBorde.get(),
            self.cmb_tipo.get(),
            int(self.slider_grosor.get()),
            copy.deepcopy(self.puntos)
        )
        
        triangulo.draw(self.imagen)
        self.imagen_tk.paste(self.imagen)
        self.canvas.update()
        
        self.lista_elementos.append(triangulo)
        self.lista_elementos_nombre.append(triangulo.id)

        self.cmb_elementos.set(value=triangulo.id)
        self.cmb_elementos.configure(values=self.lista_elementos_nombre)
        self.current_object= triangulo
        
    def update_current(self, event):
        current_id = int(self.cmb_elementos.get().split('.')[0]) - 1
        self.current_object = self.lista_elementos[current_id]
        print(self.current_object)
        
    def update_element(self):
        if self.current_object:
            if isinstance(self.current_object, Triangulo):
                self.current_object.colorRelleno = self.color.get()
                self.current_object.colorBorde = self.colorBorde.get()
                self.current_object.tipoBorde = self.cmb_str.get()
                self.current_object.bordeAncho = int(self.slider_grosor.get())
            elif isinstance(self.current_object, Circle):
                self.current_object.tipoBorde = self.cmb_str.get()
                self.current_object.colorRelleno = self.color.get()
                self.current_object.colorBorde = self.colorBorde.get()
                self.current_object.bordeAncho = int(self.slider_grosor.get())
            elif isinstance(self.current_object, Line):
                self.current_object.colorBorde = str(self.colorBorde.get()),
                self.current_object.tipoBorde = self.cmb_str.get(),
                self.current_object.bordeAncho = int(self.slider_grosor.get())
                #reset a la imagen
            self.imagen = Image.new("RGB", (700, 600), color=(255, 255, 255))
            self.drawAll()
            self.imagen_tk.paste(self.imagen)
            self.canvas.update()
    
    def drawAll(self):
        for elemento in self.lista_elementos:
            elemento.draw(self.imagen)

    def delete(self):
        if self.current_object:
            self.lista_elementos.remove(self.current_object)
            self.lista_elementos_nombre.remove(self.current_object.id)
            #volveriamos al elemento anterior
            #self.current_object = self.lista_elementos_nombre[-1] if self.lista_elementos_nombre else None
            #self.cmb_elementos.set(value=self.lista_elementos_nombre[-1] if self.lista_elementos_nombre else "")
            self.cmb_elementos.set(value="")
            self.cmb_elementos.configure(values=self.lista_elementos_nombre)
            self.current_object = None
            self.imagen = Image.new("RGB", (700, 600), color=(255, 255, 255))
            self.drawAll()
            self.imagen_tk.paste(self.imagen)
            self.canvas.update()
        else:
            print("no hay elemento seleccionado")

    def cambiarRelleno(self, isFilled):
        if self.current_object:
            self.current_object.isFilled = isFilled

            self.imagen = Image.new("RGB", (700, 600), color=(255, 255, 255))
            self.drawAll()
            self.imagen_tk.paste(self.imagen)
            self.canvas.update()
    def limpiarTodo(self):
        self.imagen = Image.new("RGB", (700, 600), color=(255, 255, 255))
        self.imagen_tk.paste(self.imagen)
        self.canvas.update()

    def show_popup_menu(self, event):
        self.context_menu_x = event.x
        self.context_menu_y = event.y
        menu = tk.Menu(self.master, tearoff=0)
        menu.add_command(label="Mover", command=self.set_mover)
        menu.add_command(label="Rotar", command=self.set_rotar)
        menu.add_command(label="Escala", command=self.set_escala)
        #menu.add_command(label="Actualizar elemento", command=self.update_element)
        menu.add_command(label="Rellenar", command=lambda: self.cambiarRelleno(True))
        menu.add_command(label="Quitar relleno", command=lambda: self.cambiarRelleno(False))
        menu.add_command(label="Eliminar elemento", command=self.delete)
        menu.add_command(label="Guardar imagen", command= self.guardar_imagen)
        menu.add_command(label="Limpiar canvas", command=self.limpiarTodo)
        menu.post(event.x_root, event.y_root)


    def mover(self):
        if self.current_object:
            self.current_object.trasladar(self.puntos[0],self.puntos[1])
            self.imagen = Image.new("RGB", (700, 600), color=(255, 255, 255))
            self.drawAll()
            self.imagen_tk.paste(self.imagen)
            self.canvas.update()

    def escala(self):
        pivot = self.puntos[0]
        if self.current_object:
            self.current_object.escalar(self.n_escala)
            self.imagen = Image.new("RGB", (700, 600), color=(255, 255, 255))
            self.drawAll()
            self.imagen_tk.paste(self.imagen)
            self.canvas.update()
    
    def rotar(self):
        pivot = self.puntos[0]
        if self.current_object:
            self.current_object.rotar(self.theta_rotacion)
            self.imagen = Image.new("RGB", (700, 600), color=(255, 255, 255))
            self.drawAll()
            self.imagen_tk.paste(self.imagen)
            self.canvas.update()
       
    def distancia_entre_puntos(self, x1, y1, x2, y2):
        distancia = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return round(distancia) 

if __name__ == "__main__":
    root = ctk.CTk()
    my_gui = Gui(root)
    root.title('Mi Paint')
    root.iconbitmap(bitmap='./images/tortuga.ico')
    root.mainloop()