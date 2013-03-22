'''
Created on 22/03/2013

@author: sebastiang
'''

from curses.ascii import _ctoi
import re


def main():
    patente = ""
    promt = "Ingrese su patente o 'q' para salir: "
    while patente != "q":
        patente = raw_input(promt)
        print reemplazo_patente(patente.lower()), "\n",\
            "*" * 20


def crear_diccionario():
    lista = "14 01 00 16 05 02 19 09 24 07 21 08 04\
             13 25 22 18 10 02 06 12 23 11 03 15 17"
    diccionario = {}
    i = 0
    for item in lista.split():
        diccionario.__setitem__(chr(_ctoi("a") + i), item)
        i += 1
    return diccionario


def verificacion_longitud(valor):
    nuevo_valor = valor
    while nuevo_valor >= 10:
        nuevo_valor = 0
        for char in str(valor):
            nuevo_valor += int(char)
        if nuevo_valor >= 10:
            return verificacion_longitud(nuevo_valor)
    return nuevo_valor


def calculo_digito(lista):
    valor_1 = 0
    valor_2 = 0
    iterador = len(lista)
    while iterador > 0:
        if iterador % 2 == 0:
            valor_1 += lista[iterador - 1]
        else:
            valor_2 += lista[iterador - 1]
        iterador -= 1
    valor_1 = verificacion_longitud(valor_1)
    valor_2 = verificacion_longitud(valor_2)
    respuesta = "Su digito de verificacion es:",\
                "".join([str(valor_2), str(valor_1)])
    return respuesta


def reemplazo_patente(patente=""):
    lista = []
    pattern = re.compile("([a-zA-Z]+)([0-9]+)")
    clave_separada = re.match(pattern, patente)

    if not clave_separada or len(clave_separada.group(1)) + \
            len(clave_separada.group(2)) != len(patente):
        return "Patente invalida"
    diccionario = crear_diccionario()

    for char in clave_separada.group(1):
        valor = diccionario.get(char)
        for char in valor:
            lista.append(int(char))
    for i in clave_separada.group(2):
        lista.append(int(i))
    return calculo_digito(lista)


if __name__ == "__main__":
    main()
