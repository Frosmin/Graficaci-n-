import math


class Line:
    # def __init__(self, canva, id, colorRelleno, colorBorde, tipoBorde, bordeAncho, centro, radio) -> None:
    def __init__(
        self, canva, id, colorBorde, tipoBorde, bordeAncho, puntoInicio, puntoFinal
    ):
        self.isFilled = False
        self.canvas = canva
        self.id = id
        self.colorBorde = colorBorde
        self.tipoBorde = tipoBorde
        self.bordeAncho = bordeAncho
        self.puntoInicio = puntoInicio
        self.puntoFinal = puntoFinal
        self.segment = 15
        self.escala = 1
        self.angulo = 0

    def hex_to_rgb(self, colorsitoo):
        # Eliminar el caracter '#' si está presente
        if isinstance(colorsitoo, tuple):
            colorsitoo = colorsitoo[0]
        elif not isinstance(colorsitoo, str):
            return 0, 0, 0
       
        colorsitoo = colorsitoo.lstrip("#")

        # Verificar si el color es un formato válido de 3 o 6 caracteres
        if len(colorsitoo) == 3:
            r = int(colorsitoo[0] * 2, 16)
            g = int(colorsitoo[1] * 2, 16)
            b = int(colorsitoo[2] * 2, 16)
        elif len(colorsitoo) == 6:
            r = int(colorsitoo[0:2], 16)
            g = int(colorsitoo[2:4], 16)
            b = int(colorsitoo[4:6], 16)
        else:
            raise ValueError("Formato de color hexadecimal inválido.")

        return (r, g, b)

    def draw_pixel(self, imagen, x, y, color, grosor=1):
        if 0 <= x < 700 and 0 <= y < 600:
            suma = 0 if (grosor%2==0) else 1
            half_thickness = int(grosor // 2)
            for dx in range(-half_thickness, half_thickness + suma):
                for dy in range(-half_thickness, half_thickness + suma):
                    #draw.line([(x + dx, y + dy), (x + dx + 1, y + dy + 1)], fill=color, width=1)
                    if ((0 < x < 700) and (0 < y < 700)):
                        imagen.putpixel((int(x + dx), int(y + dy)), self.hex_to_rgb(color))

    # def draw_line_bresenham
    def draw(self, imagen):
        self.segment = 15
        grosor = self.bordeAncho
        x0, y0 = self.puntoInicio
        x1, y1 = self.puntoFinal

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = -1 if x0 > x1 else 1
        sy = -1 if y0 > y1 else 1
        err = dx - dy
        while x0 != x1 or y0 != y1:

            if self.tipoBorde == "Segmentado" or self.tipoBorde[0] == "Segmentado": # odio mi vida
                if self.segment == 0:
                    self.segment = 15
                if self.segment > 5:
                    self.draw_pixel(imagen, x0, y0, self.colorBorde, grosor)
                self.segment -= 1
            else:
                self.draw_pixel(imagen, x0, y0, self.colorBorde, grosor)
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
                
            if e2 < dx:
                err += dx
                y0 += sy
               

    def trasladar(self, fromCords, toCords):
        print(f"de {fromCords} hasta {toCords}")
        x1, y1 = fromCords
        x2, y2 = toCords
        deltaX = x2 - x1
        deltaY = y2 - y1
        print(f"antes {self.puntoFinal}")

        self.puntoInicio = (self.puntoInicio[0] + deltaX, self.puntoInicio[1] + deltaY)
        self.puntoFinal = (self.puntoFinal[0] + deltaX, self.puntoFinal[1] + deltaY)
        print(f"antes {self.puntoInicio}")

    def escalar(self, escala):
        self.escala = escala
        puntosEscalados = self._escalar()
        self.puntoInicio = puntosEscalados[0]
        self.puntoFinal = puntosEscalados[1]
        #puntosRotados = self._rotar(puntosEscalados)


    def _escalar(self):
        x0, y0 = self.puntoInicio
        x1, y1 = self.puntoFinal
        # Escalar los puntos de inicio y final de la línea y devolver nueva lista
        puntoInicioEscalado = (x0, y0)
        puntoFinalEscalado = (
            int(((x1 - x0) * self.escala) + x0),
            int(((y1 - y0) * self.escala) + y0),
        )
        return [puntoInicioEscalado, puntoFinalEscalado]

    def rotar(self, angulo):
        self.angulo = angulo
        puntosRotados = self._rotar([self.puntoInicio, self.puntoFinal])
        self.puntoInicio = puntosRotados[0]
        self.puntoFinal = puntosRotados[1]

    def _rotar(self, puntosEscalados):
        x0, y0 = puntosEscalados[0]
        x1, y1 = puntosEscalados[1]

        # Convertir el ángulo de grados a radianes
        angulo_radianes = math.radians(self.angulo)

        # Calcular las coordenadas relativas al punto de origen
        x0_rel, y0_rel = x0 - x0, y0 - y0
        x1_rel, y1_rel = x1 - x0, y1 - y0

        # Aplicar la rotación
        x1_rotado = x1_rel * math.cos(angulo_radianes) - y1_rel * math.sin(
            angulo_radianes
        )
        y1_rotado = x1_rel * math.sin(angulo_radianes) + y1_rel * math.cos(
            angulo_radianes
        )

        # Calcular las coordenadas finales rotadas
        puntoInicioRotado = (x0, y0)
        puntoFinalRotado = (int(x1_rotado + x0), int(y1_rotado + y0))

        return [puntoInicioRotado, puntoFinalRotado]

    def __str__(self) -> str:
        return f"Hola soy la linea {self.id} ✋"
