import math

class Triangulo():
    def __init__(self, canvas, id, colorRelleno, colorBorde, tipoBorde, bordeAncho, puntos) -> None:
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
    
    def rotar(self, angulo):
        self.angulo = angulo

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
            puntos_escala.append((x * self.escala, y * self.escala))

        # Devolver los puntos a sus coordenadas originales
        puntos_finales = []
        for x, y in puntos_escala:
            puntos_finales.append((x + anchor_x, y + anchor_y))

        return puntos_finales

    def draw(self):
        puntosEscala = self._escalar()
        nuevosPuntos = self._rotar(puntosEscala)
        
        self.scanline(nuevosPuntos)
    
        self.bresenham(*nuevosPuntos[0], *nuevosPuntos[1], self.colorBorde)
        self.bresenham(*nuevosPuntos[1], *nuevosPuntos[2], self.colorBorde)
        self.bresenham(*nuevosPuntos[2], *nuevosPuntos[0], self.colorBorde)
        
    def draw_pixel(self, x, y, color="#000000", grosor=1):
        x1, y1 = (x,y)
        x2, y2 = ((x+grosor), (y+grosor))
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, width=0)        

    def bresenham(self, x0, y0, x1, y1, color):
        dx = abs(x1 - x0) 
        dy = abs(y1 - y0) 
        sx = -1 if x0 > x1 else 1
        sy = -1 if y0 > y1 else 1
        err = dx - dy
        while x0 != x1 or y0 != y1:
            if self.tipoBorde == "Segmentado":
                if self.segment == 0: self.segment = 15
                if self.segment > 5:
                    self.draw_pixel(x0, y0, color, self.bordeAncho)
                self.segment-=1
            else:
                self.draw_pixel(x0, y0, color, self.bordeAncho)
            e2 = 2 * err
            if e2 > -dy:
                err -= (dy)
                x0 += (sx)
            if e2 < dx:
                err += (dx)
                y0 += (sy)
                
    def bresenhamSinSegmentadoXD(self, x0, y0, x1, y1, color):
        dx = abs(x1 - x0) 
        dy = abs(y1 - y0) 
        sx = -1 if x0 > x1 else 1
        sy = -1 if y0 > y1 else 1
        err = dx - dy
        while x0 != x1 or y0 != y1:
            self.draw_pixel(x0, y0, color)
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
    
    def scanline(self, puntosNuevos):
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
                self.bresenhamSinSegmentadoXD(x0, y, x1, y, self.colorRelleno)

    
    def __str__(self) -> str:
        return f"Hola soy el triangulo {self.id}"