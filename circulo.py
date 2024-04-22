from PIL import ImageGrab, Image
import tkinter as tk


class Circle:
    def __init__(
        self, canva, id, colorRelleno, colorBorde, tipoBorde, bordeAncho, centro, radio
    ) -> None:
        self.isFilled = False
        self.canvas = canva
        self.segment = 15
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
        if 0 <= x < 700 and 0 <= y < 600:
            imagen.putpixel((int(x), int(y)), self.hex_to_rgb(color))

    # def draw_circle_bresenham
    def draw(self, imagen):

        def drawOctantes():
            self.draw_pixel(
                imagen,
                self.centro[0] + x,
                self.centro[1] + y,
                color=self.colorBorde,
                grosor=self.bordeAncho,
            )
            self.draw_pixel(
                imagen,
                self.centro[0] - x,
                self.centro[1] + y,
                color=self.colorBorde,
                grosor=self.bordeAncho,
            )
            self.draw_pixel(
                imagen,
                self.centro[0] + x,
                self.centro[1] - y,
                color=self.colorBorde,
                grosor=self.bordeAncho,
            )
            self.draw_pixel(
                imagen,
                self.centro[0] - x,
                self.centro[1] - y,
                color=self.colorBorde,
                grosor=self.bordeAncho,
            )
            self.draw_pixel(
                imagen,
                self.centro[0] + y,
                self.centro[1] + x,
                color=self.colorBorde,
                grosor=self.bordeAncho,
            )
            self.draw_pixel(
                imagen,
                self.centro[0] - y,
                self.centro[1] + x,
                color=self.colorBorde,
                grosor=self.bordeAncho,
            )
            self.draw_pixel(
                imagen,
                self.centro[0] + y,
                self.centro[1] - x,
                color=self.colorBorde,
                grosor=self.bordeAncho,
            )
            self.draw_pixel(
                imagen,
                self.centro[0] - y,
                self.centro[1] - x,
                color=self.colorBorde,
                grosor=self.bordeAncho,
            )

        x = 0
        y = self.radio * self.escala
        p = 1 - self.radio

        while x <= y:
            if self.tipoBorde == "Segmentado":
                if self.segment == 0:
                    self.segment = 15
                if self.segment > 5:
                    drawOctantes()
                self.segment -= 1
            else:
                drawOctantes()

            x += 1
            if p <= 0:
                p = p + 2 * x + 1
            else:
                y -= 1
                p = p + 2 * (x - y) + 1
        # self.floodFill()
        if self.isFilled:
            self.flood_fill(
                imagen,
                self.centro[0],
                self.centro[1],
                self.colorRelleno,
                self.colorBorde,
            )

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

    def rotar(self, angulo):
        self.angulo = angulo

    # TODO
    def floodFill(self):
        photo_image = tk.PhotoImage(
            master=self.canvas,
            width=self.canvas.winfo_reqwidth(),
            height=self.canvas.winfo_reqheight(),
        )
        x = 10  # Ejemplo: coordenada x
        y = 20  # Ejemplo: coordenada y
        color = photo_image.get(x, y)
        print("Color en la posición ({}, {}): {}".format(x, y, color))

    # esto no es flood fill xd
    def flood_fill_circle(self):
        radio = self.radio * self.escala
        for y in range(round(self.centro[1] - radio), round(self.centro[1] + radio)):
            for x in range(
                round(self.centro[0] - radio), round(self.centro[0] + radio)
            ):
                if (x - self.centro[0]) ** 2 + (y - self.centro[1]) ** 2 <= radio**2:
                    self.canvas.create_rectangle(
                        x,
                        y,
                        x + 1,
                        y + 1,
                        fill=self.colorRelleno,
                        outline=self.colorRelleno,
                    )

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
