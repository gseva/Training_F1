'''
Created on 05/04/2013

@author: sebastiang
'''
import random

llamadas = 0
from Queue import PriorityQueue


class cobayo_handler():

    def __init__(self):
        self.movimientos_prohibidos = {}
        self.pos_actual = ()
        self.pos_futura = ()
        self.lista_max = []
        self.movimientos = [(2, 1), (2, -1), (1, 2), (-1, 2),
                            (-2, 1), (-2, -1), (-1, -2), (1, -2)]
        self.llamadas = 0
        self.contador = 0
        self.movs_anteriores = []

    def devolver_pos_movs(self, pos, i):
        posibles_movimientos = []
        for index in range(8):
            x = pos[0] + self.movimientos[index][0]
            y = pos[1] + self.movimientos[index][1]
            if not (x > 8 or x < 1 or y > 8 or y < 1):
                if i in self.movimientos_prohibidos.keys():
                    if self.movimientos_prohibidos[i].__contains__((x, y)):
                        continue
                posibles_movimientos.append((x, y))
        return posibles_movimientos

    def calcular_posicion(self, pos, i):
        random.shuffle(self.movimientos)
        cola = PriorityQueue()
        posibles_movimientos = self.devolver_pos_movs(pos, i)
        if not posibles_movimientos:
            return None
        for item in posibles_movimientos:
            prioridad = 100
            x = item[0]
            y = item[1]
#            if pos[0] == 8 or pos[0] == 1:
#                if y != 8 and y != 1 \
#                    and x != 8 and x != 1:
#                    prioridad -= 15
#            if pos[1] == 8 or pos[1] == 1:
#                if y != 8 and y != 1 \
#                    and x != 8 and x != 1:
#                    prioridad -= 15
#            if (pos[0] == 2 and (pos[1] == 3 or pos[1] == 6)) or\
#               (pos[0] == 3 and (pos[1] == 2 or pos[1] == 7)) or\
#               (pos[0] == 6 and (pos[1] == 2 or pos[1] == 7)) or\
#               (pos[0] == 7 and (pos[1] == 3 or pos[1] == 6)):
#                if (x == 4 or x == 5) and\
#                   (y == 4 or y == 5):
#                    prioridad -= 20
#            prox_pos = self.devolver_pos_movs((x, y), i + 1)
#            for element in prox_pos:
#                prox_prox_pos = self.devolver_pos_movs(element, i + 2)
#                for i in range(len(prox_prox_pos)):
#                    prioridad += 5
#            for i in range(len(prox_pos)):
#                prioridad += 10
#            if x == 1 or x == 8:
#                prioridad -= 10
#            if pos[0] == 2:
#                if x == 1 or x == 8:
#                    prioridad -= 10
#            if pos[0] == 7:
#                if x == 1 or x == 8:
#                    prioridad -= 10
#            if pos[1] == 2:
#                if y == 1 or y == 8:
#                    prioridad -= 10
#            if pos[1] == 7:
#                if y == 1 or y == 8:
#                    prioridad -= 10
            if y == 1 or y == 8:
                prioridad -= 10
            if x == 1 or x == 8:
                prioridad -= 10
            if x == 2 or x == 7:
                prioridad -= 5
            if y == 2 or y == 7:
                prioridad -= 5
            if x == 3 or x == 5:
                prioridad -= 1
            if y == 3 or y == 5:
                prioridad -= 1
            cola.put((prioridad, item))
        return cola.get()[1]

    def hacer_movimiento(self, pos_inicial):

        self.pos_inicial = ()
        self.pos_actual = pos_inicial
        self.lista_movs = []
        self.lista_movs.append(pos_inicial)
        self.llamadas += 1
        i = 0

        while True:
            if len(self.lista_movs) > len(self.lista_max):
                self.lista_max = self.lista_movs[:]
            if not i in self.movimientos_prohibidos.keys():
                self.movimientos_prohibidos[i] = []
            for item in self.lista_movs:
                if i in self.movimientos_prohibidos.keys():
                    if not item in self.movimientos_prohibidos[i]:
                        self.movimientos_prohibidos[i].append(item)
            self.pos_futura = self.calcular_posicion(self.pos_actual, i)
            if not self.pos_futura:
                if i - 1 in self.movimientos_prohibidos.keys():
                    self.movimientos_prohibidos[i - 1].append(self.pos_actual)
                if self.llamadas <= 50:
                    self.movs_anteriores = self.lista_movs[:]
                    return self.hacer_movimiento(pos_inicial)
                else:
                    break
            else:
                self.lista_movs.append(self.pos_futura)
                i += 1
                if len(self.lista_movs) >= 64:
                    return self.lista_movs
                self.pos_actual = self.pos_futura
                continue
        return self.lista_max

lista_cant_mov = []
for x in range(8):
    for y in range(8):
        pos = (x + 1, y + 1)
        ch = cobayo_handler()
        lista_movs = ch.hacer_movimiento(pos)
        lista_tablero = {}
        counter = 1
        for item in lista_movs:
            lista_tablero[(item[0] - 1) * 8 + (item[1] - 1)] = counter
            counter += 1
        print "empezando en la pos: ", pos
        print "maxima cantidad de moviemientos:", len(lista_movs)
        lista_cant_mov.append(len(lista_movs))
        string = ""
        for i in range(64):
            if i in lista_tablero.keys():
                char = str(lista_tablero[i])
                if len(char) == 1:
                    string += " " + char + " "
                else:
                    string += " " + char
            else:
                string += " . "
            if (i + 1) % 8 == 0:
                string += "\n"
        print string

print "Cantidades de movimientos:", lista_cant_mov
l1 = [60, 64, 60, 61, 62, 63, 62, 62, 61, 63, 64, 62, 64, 63, 61, 60, 61, 64,
      60, 62, 61, 63, 63, 62, 62, 62, 62, 60, 63, 63, 62, 60, 59, 62, 62, 61,
      61, 60, 62, 62, 61, 64, 64, 63, 64, 60, 64, 62, 63, 63, 62, 62, 60, 61,
      64, 64, 62, 60, 62, 62, 61, 60, 62, 63]
suma = 0
for item in lista_cant_mov:
    suma += item
print "promedio:", float(suma) / len(lista_cant_mov)
print "Cantidades de movimientos para 995 llamadas recursivas:", l1
print "Son iguales?: ", l1 == lista_cant_mov
