import math


class Line:
    # def __init__(self, canva, id, colorRelleno, colorBorde, tipoBorde, bordeAncho, centro, radio) -> None:
    def __init__(
        self, canva, id, colorBorde, tipoBorde, bordeAncho, puntoInicio, puntoFinal
    ) -> None:
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

    def draw_pixel(self, imagen, x, y, colorsssssss, grosor=1):
        if 0 <= x < 700 and 0 <= y < 600:
            nuevoColor = self.hex_to_rgb(colorsssssss)
            imagen.putpixel((int(x), int(y)), nuevoColor)

    # def draw_line_bresenham
    def draw(self, imagen):
        grosor = self.bordeAncho

        puntosEscalados = self._escalar()
        puntosRotados = self._rotar(puntosEscalados)

        x0, y0 = puntosRotados[0]
        x1, y1 = puntosRotados[1]

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = -1 if x0 > x1 else 1
        sy = -1 if y0 > y1 else 1
        err = dx - dy
        while x0 != x1 or y0 != y1:
            if self.tipoBorde == "Segmentado":
                if self.segment == 0:
                    self.segment = 15
                if self.segment > 5:
                    self.draw_pixel(imagen, x0, y0, self.colorBorde)
                self.segment -= 1
            else:
                self.draw_pixel(imagen, x0, y0, self.colorBorde)
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

    def _escalar(self):
        x0, y0 = self.puntoInicio
        x1, y1 = self.puntoFinal
        # Escalar los puntos de inicio y final de la línea y devolver nueva lista
        puntoInicioEscalado = (x0, y0)
        puntoFinalEscalado = (
            ((x1 - x0) * self.escala) + x0,
            ((y1 - y0) * self.escala) + y0,
        )
        return [puntoInicioEscalado, puntoFinalEscalado]

    def rotar(self, angulo):
        self.angulo = angulo

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
