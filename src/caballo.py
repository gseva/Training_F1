'''
Created on 05/04/2013

@author: sebastiang
'''

llamadas = 0


def calcular_posicion(pos, index, i, m_p):
    if index > 8:
        return None
    movimientos = [(2, 1), (2, -1), (1, 2), (-1, 2),
                   (-2, 1), (-2, -1), (-1, -2), (1, -2)]
    x = pos[0] + movimientos[index][0]
    y = pos[1] + movimientos[index][1]
    if not (x > 8 or x < 1 or y > 8 or y < 1):
        if m_p[i].__contains__((x, y)):
            return None
        tupla = (x, y)
        return tupla
    return None


def hacer_movimiento(pos_actual):
    movimientos_prohibidos = {}
    i = 0
    global llamadas
    lista = []
    lista_max = []
    lista.append(pos_actual)
    llamadas += 1

    while True:
        if len(lista) > len(lista_max):
            lista_max = lista[:]
        if not i in movimientos_prohibidos.keys():
            movimientos_prohibidos[i] = []
        try:
            movimientos_prohibidos[i].append(lista[-1])
            for item in lista:
                if not item in movimientos_prohibidos[i]:
                    movimientos_prohibidos[i].append(item)
        except:
            pass
        for iterador in range(8):
            pos_futura = calcular_posicion(pos_actual, iterador, i,
                                           movimientos_prohibidos)
            if pos_futura:
                break
        if not pos_futura:
            if i < 1:
                return lista_max
            i -= 1
            pos_anterior = lista.pop()
            movimientos_prohibidos[i].append(pos_actual)
            pos_actual = pos_anterior
            continue
        else:
            lista.append(pos_futura)
            if len(lista) >= 64:
                return lista
            i += 1
            pos_actual = pos_futura
            continue
    return lista_max


lista_cant_mov = []
for x in range(8):
    for y in range(8):
        pos = (x + 1, y + 1)
        lista = hacer_movimiento(pos)

        lista_tablero = {}
        counter = 1
        for item in lista:
            lista_tablero[(item[0] - 1) * 8 + (item[1] - 1)] = counter
            counter += 1

        print "empezando en la pos: ", pos
        print "maxima cantidad de moviemientos:", len(lista)
        lista_cant_mov.append(len(lista))
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
