import math

class Triangulo():
    def __init__(self, canvas, id, colorRelleno, colorBorde, tipoBorde, bordeAncho, puntos) -> None:
        self.isFilled = False
        self.canvas = canvas
        self.id = id
        self.colorRelleno = colorRelleno
        self.colorBorde = colorBorde
        self.tipoBorde = tipoBorde
        self.bordeAncho = bordeAncho
        self.puntos = puntos
        self.angulo = 0
        self.escala = 1
        self.angulo = 0
        self.segment = 8
    
    def trasladar(self, fromCords, toCords):
        x1, y1 = fromCords
        x2, y2 = toCords
        deltaX = x2 - x1
        deltaY = y2 - y1
        for i in range(len(self.puntos)):
            x, y = self.puntos[i]
            self.puntos[i] = (x + deltaX, y + deltaY)
    
    def escalar(self, escala):
        self.escala = escala
        puntosEscala = self._escalar()
        self.puntos = puntosEscala
    
    def rotar(self, angulo):
        self.angulo = angulo
        nuevosPuntos = self._rotar(self.puntos)
        self.puntos = nuevosPuntos
    
    def _escalar(self):
        # Calcular el punto de anclaje (primer punto)
        anchor_x, anchor_y = self.puntos[0]
        # Llevar todos los puntos a coordenadas locales (respecto al primer punto)
        puntos_locales = []
        for x, y in self.puntos:
            puntos_locales.append((x - anchor_x, y - anchor_y))
        # Escalar los puntos
        puntos_escala = []
        for x, y in puntos_locales:
            puntos_escala.append((int(x * self.escala),int( y * self.escala)))

        # Devolver los puntos a sus coordenadas originales
        puntos_finales = []
        for x, y in puntos_escala:
            puntos_finales.append((x + anchor_x, y + anchor_y))

        return puntos_finales
    
    def draw(self, imagen):
        self.segment = 8
        nuevosPuntos = self.puntos
        if self.isFilled:
            self.scanline(imagen, nuevosPuntos)
        self.bresenham(imagen, *nuevosPuntos[0], *nuevosPuntos[1], self.colorBorde)
        self.bresenham(imagen, *nuevosPuntos[1], *nuevosPuntos[2], self.colorBorde)
        self.bresenham(imagen, *nuevosPuntos[2], *nuevosPuntos[0], self.colorBorde)
    
    def draw_pixel(self, imagen, x, y, color="#000000", grosor=1):
        if ((0 <= x < 700 ) and (0 <= y < 600)):
            suma = 0 if (grosor%2==0) else 1
            half_thickness = int(grosor // 2)
            for dx in range(-half_thickness, half_thickness + suma):
                for dy in range(-half_thickness, half_thickness + suma):
                    #draw.line([(x + dx, y + dy), (x + dx + 1, y + dy + 1)], fill=color, width=1)
                    if ((0 <= int(x+dx) < 700) and (0 <= int(y+dy ) < 600)):
                        imagen.putpixel((int(x + dx), int(y + dy)), self.hex_to_rgb(color))    

    def bresenham(self, imagen, x0, y0, x1, y1, color):
        dx = abs(x1 - x0) 
        dy = abs(y1 - y0) 
        sx = -1 if x0 > x1 else 1
        sy = -1 if y0 > y1 else 1
        err = dx - dy
        while x0 != x1 or y0 != y1:
            if self.tipoBorde == "Segmentado":
                if self.segment == 0: self.segment = 15
                if self.segment > 5:
                    self.draw_pixel(imagen, x0, y0, color, self.bordeAncho)
                self.segment-=1
            else:
                self.draw_pixel(imagen, x0, y0, color, self.bordeAncho)
            e2 = 2 * err
            if e2 > -dy:
                err -= (dy)
                x0 += (sx)
            if e2 < dx:
                err += (dx)
                y0 += (sy)
    
    def bresenhamSinSegmentadoXD(self, imagen, x0, y0, x1, y1, color):
        dx = abs(x1 - x0) 
        dy = abs(y1 - y0) 
        sx = -1 if x0 > x1 else 1
        sy = -1 if y0 > y1 else 1
        err = dx - dy
        while x0 != x1 or y0 != y1:
            self.draw_pixel(imagen, x0, y0, color)
            e2 = 2 * err
            if e2 > -dy:
                err -= (dy)
                x0 += (sx)
            if e2 < dx:
                err += (dx)
                y0 += (sy)
    
    def _rotar(self, nuevosPuntos):
        # Calcular el punto de anclaje (primer punto)
        anchor_x, anchor_y = nuevosPuntos[0]
        angulo_radianes = math.radians(self.angulo)
        # Llevar todos los puntos a coordenadas locales (respecto al primer punto)
        puntos_locales = []
        for x, y in nuevosPuntos:
            puntos_locales.append((x - anchor_x, y - anchor_y))

        # Rotar los puntos
        puntos_rotados = []
        for x, y in puntos_locales:
            # Aplicar la rotación usando trigonometría
            x_rotado = x * math.cos(angulo_radianes) - y * math.sin(angulo_radianes)
            y_rotado = x * math.sin(angulo_radianes) + y * math.cos(angulo_radianes)
            puntos_rotados.append((x_rotado, y_rotado))

        # Devolver los puntos a sus coordenadas originales
        puntos_finales = []
        for x, y in puntos_rotados:
            puntos_finales.append((int(x + anchor_x), int(y + anchor_y)))

        # Actualizar los puntos del triángulo
        return puntos_finales
    
    def scanline(self, imagen, puntosNuevos):
        # Encontrar los límites del triángulo en y
        min_y = min(pt[1] for pt in puntosNuevos)
        max_y = max(pt[1] for pt in puntosNuevos)
        
        # Para cada línea horizontal (scanline) dentro de los límites y del triángulo
        for y in range(min_y, max_y + 1):
            # Encontrar las intersecciones de la línea horizontal con los lados del triángulo
            intersecciones = []
            for i in range(3):
                p1 = puntosNuevos[i]
                p2 = puntosNuevos[(i + 1) % 3]
                if p1[1] != p2[1]:  # Evitar divisiones por cero
                    if min(p1[1], p2[1]) <= y < max(p1[1], p2[1]):
                        x_intersect = p1[0] + (y - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1])
                        intersecciones.append(x_intersect)
            
            # Ordenar las intersecciones para obtener los pares de puntos
            intersecciones.sort()
            
            # Dibujar los píxeles entre los pares de puntos
            for i in range(0, len(intersecciones), 2):
                x0 = int(intersecciones[i])
                x1 = int(intersecciones[i + 1])
                self.bresenhamSinSegmentadoXD(imagen, x0, y, x1, y, self.colorRelleno)

    def hex_to_rgb(self, hex_color):
        # Eliminar el caracter '#' si está presente
        hex_color = hex_color.lstrip('#')
        
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
        return f"Hola soy el triangulo {self.id}"