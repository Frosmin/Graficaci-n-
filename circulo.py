from PIL import ImageGrab, Image
import tkinter as tk


class Circle:
    def __init__(
        self, canva, id, colorRelleno, colorBorde, tipoBorde, bordeAncho, centro, radio
    ) -> None:
        self.isFilled = False
        self.canvas = canva
        self.segment = 30
        self.puntos = list()
        self.id = id
        self.grosor = 1
        self.colorRelleno = colorRelleno
        self.colorBorde = colorBorde
        self.tipoBorde = tipoBorde
        self.bordeAncho = bordeAncho
        self.centro = centro
        self.radio = radio
        self.escala = 1
        self.angulo = 0

    # TODO agregar el grosor de borde PRIORITY:HIGH
    def draw_pixel(self, imagen, x, y, color="#000000", grosor=1):
        
        if (0 <= x < 700) and (0 <= y < 600):
            suma = 0 if (grosor%2==0) else 1
            half_thickness = int(grosor // 2)
            for dx in range(-half_thickness, half_thickness + suma):
                for dy in range(-half_thickness, half_thickness + suma):
                    #draw.line([(x + dx, y + dy), (x + dx + 1, y + dy + 1)], fill=color, width=1)
                    if ((0 < (int(x + dx)< 700) and (0 < int(y + dy) < 600)):
                        imagen.putpixel((int(x + dx), int(y + dy)), self.hex_to_rgb(color))

    # def draw_circle_bresenham
    def draw(self, imagen):
        self.segment = 20
        def drawOctantes(colorrrr):
            self.draw_pixel(
                imagen,
                self.centro[0] + x,
                self.centro[1] + y,
                color=colorrrr,
                grosor=self.bordeAncho,
            )
            self.draw_pixel(
                imagen,
                self.centro[0] - x,
                self.centro[1] + y,
                color=colorrrr,
                grosor=self.bordeAncho,
            )
            self.draw_pixel(
                imagen,
                self.centro[0] + x,
                self.centro[1] - y,
                color=colorrrr,
                grosor=self.bordeAncho,
            )
            self.draw_pixel(
                imagen,
                self.centro[0] - x,
                self.centro[1] - y,
                color=colorrrr,
                grosor=self.bordeAncho,
            )
            self.draw_pixel(
                imagen,
                self.centro[0] + y,
                self.centro[1] + x,
                color=colorrrr,
                grosor=self.bordeAncho,
            )
            self.draw_pixel(
                imagen,
                self.centro[0] - y,
                self.centro[1] + x,
                color=colorrrr,
                grosor=self.bordeAncho,
            )
            self.draw_pixel(
                imagen,
                self.centro[0] + y,
                self.centro[1] - x,
                color=colorrrr,
                grosor=self.bordeAncho,
            )
            self.draw_pixel(
                imagen,
                self.centro[0] - y,
                self.centro[1] - x,
                color=colorrrr,
                grosor=self.bordeAncho,
            )

        
        if self.isFilled:
            x = 0
            y = self.radio
            p = 1 - self.radio

            while x <= y:
                drawOctantes(self.colorRelleno)
                x += 1
                if p <= 0:
                    p = p + 2 * x + 1
                else:
                    y -= 1
                    p = p + 2 * (x - y) + 1
            # self.floodFill()
            self.flood_fill(
                imagen,
                self.centro[0],
                self.centro[1],
                self.colorRelleno,
                self.colorBorde,
            )
        x = 0
        y = self.radio
        p = 1 - self.radio

        while x <= y:
            if self.tipoBorde == "Segmentado":
                if self.segment == 0:
                    self.segment = 20
                if self.segment > 12:
                    drawOctantes(self.colorBorde)
                self.segment -= 1
            else:
                drawOctantes(self.colorBorde)

            x += 1
            if p <= 0:
                p = p + 2 * x + 1
            else:
                y -= 1
                p = p + 2 * (x - y) + 1

    def delete(self):
        self.draw(
            *self.puntos[0],
            *self.puntos[1],
            color="white",
            tipo="Normal",
            grosor=self.grosor,
        )
        self.puntos.clear()

    def trasladar(self, fromCords, toCords):
        x1, y1 = fromCords
        x2, y2 = toCords
        deltaX = x2 - x1
        deltaY = y2 - y1
        self.centro = (self.centro[0] + deltaX, self.centro[1] + deltaY)

    def mover(self, toCords):
        self.centro = toCords

    def escalar(self, escala):
        self.escala = escala
        self.radio = int (self.radio * self.escala)

    def rotar(self, angulo):
        self.angulo = angulo


    # esto no es flood fill xd
    # def flood_fill_circle(self):
    #     radio = self.radio * self.escala
    #     for y in range(round(self.centro[1] - radio), round(self.centro[1] + radio)):
    #         for x in range(
    #             round(self.centro[0] - radio), round(self.centro[0] + radio)
    #         ):
    #             if (x - self.centro[0]) ** 2 + (y - self.centro[1]) ** 2 <= radio**2:
    #                 self.canvas.create_rectangle(
    #                     x,
    #                     y,
    #                     x + 1,
    #                     y + 1,
    #                     fill=self.colorRelleno,
    #                     outline=self.colorRelleno,
    #                 )

    def flood_fill(self, imagen, xi, yi, fill_color, border_color):
        stack = [(xi, yi)]
        visited = set()

        while stack:
            x, y = stack.pop()
            if (0 <= x < 700) and (0 <= y < 600) and (x, y) not in visited:
                current_color = imagen.getpixel((x, y))
                if current_color != self.hex_to_rgb(
                    fill_color
                ) and current_color != self.hex_to_rgb(border_color):
                    self.draw_pixel(imagen, x, y, fill_color)
                    visited.add((x, y))
                    # Agregar solo los pixeles no visitados al stack
                    if (x, y + 1) not in visited:
                        stack.append((x, y + 1))
                    if (x - 1, y) not in visited:
                        stack.append((x - 1, y))
                    if (x + 1, y) not in visited:
                        stack.append((x + 1, y))
                    if (x, y - 1) not in visited:
                        stack.append((x, y - 1))

    def hex_to_rgb(self, hex_color):
        # Eliminar el caracter '#' si está presente
        hex_color = hex_color.lstrip("#")

        # Verificar si el color es un formato válido de 3 o 6 caracteres
        if len(hex_color) == 3:
            r = int(hex_color[0] * 2, 16)
            g = int(hex_color[1] * 2, 16)
            b = int(hex_color[2] * 2, 16)
        elif len(hex_color) == 6:
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
        else:
            raise ValueError("Formato de color hexadecimal inválido.")

        return (r, g, b)

    def __str__(self) -> str:
        return f"Hola soy el circulo {self.id}"
