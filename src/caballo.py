'''
Created on 05/04/2013

@author: sebastiang
'''

llamadas = 0


class cobayo_handler():

    def __init__(self, pos):
        self.pos = pos
        self.movimientos_prohibidos = {}
#        self.lista_movs = []
        self.pos_actual = ()
        self.pos_futura = ()
#        self.posicion_inicial = ()
        self.lista_listas = {}
        self.lista_max = []
        self.movimientos = [(2, 1), (2, -1), (1, 2), (-1, 2),
                            (-2, 1), (-2, -1), (-1, -2), (1, -2)]
        self.llamadas = 0

    def calcular_posicion(self, pos, index, i, m_p):
        if index > 8:
            return None
        x = pos[0] + self.movimientos[index][0]
        y = pos[1] + self.movimientos[index][1]
        if not (x > 8 or x < 1 or y > 8 or y < 1):
            if m_p[i].__contains__((x, y)):
                return None
#            try:
            if self.lista_listas[i].__contains__((x, y)):
                return None
#            except:
#                pass
            tupla = (x, y)
            return tupla
        return None

    def hacer_movimiento(self, pos_inicial):

        self.pos_inicial = ()
        self.pos_actual = pos_inicial
        self.lista_movs = []
        self.lista_movs.append(pos_inicial)
        self.llamadas += 1
#        self.movimientos_prohibidos = {}
        i = 0

        while True:
            if len(self.lista_movs) > len(self.lista_max):
                self.lista_max = self.lista_movs[:]
            if not i in self.movimientos_prohibidos.keys():
                self.movimientos_prohibidos[i] = []
            if not i in self.lista_listas.keys():
                self.lista_listas[i] = []
            for item in self.lista_movs:
                if not item in self.movimientos_prohibidos[i]:
                    self.movimientos_prohibidos[i].append(item)
            for iterador in range(8):
                self.pos_futura = self.calcular_posicion(self.pos_actual,
                                  iterador, i, self.movimientos_prohibidos)
                if self.pos_futura:
                    break
            if not self.pos_futura:
#                if contador < 1:
#                    return self.lista_max
#                contador -= 1
#                pos_anterior = self.lista_movs.pop()
#                self.movimientos_prohibidos[i].append(self.pos_actual)
#                self.pos_actual = pos_anterior
                self.lista_listas[i].append(self.pos_actual)
                self.movimientos_prohibidos[i - 1].append(self.pos_actual)
#                print " llegue a hacer", len(self.lista_movs), "movimientos"
                try:
                    return self.hacer_movimiento(pos_inicial)
                except:
                    return self.lista_max
            else:
                self.lista_movs.append(self.pos_futura)
                if len(self.lista_movs) >= 64:
                    return self.lista_movs
                i += 1
                self.pos_actual = self.pos_futura
                continue
        return self.lista_max

lista_cant_mov = []
for x in range(8):
    for y in range(8):
        pos = (x + 1, y + 1)
        ch = cobayo_handler(pos)
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
print lista_cant_mov
