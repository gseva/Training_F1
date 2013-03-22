'''
Created on 22/03/2013

@author: sebastiang
'''

from curses.ascii import _ctoi
import re


def main():
    """La funcion madre, interroga al usuario"""
    patente = ""
    promt = "Ingrese su patente o 'q' para salir: "
    while patente != "q":
        patente = raw_input(promt)
        print reemplazo_patente(patente.lower()), "\n",\
            "*" * 20


def crear_diccionario():
    """Crea un diccionario asigandole un valor de la tabla
       a todos los caracteres low case ASCII. Hice esta funcion
       porque me daba fiaca escribir el diccionario a mano"""
    lista = "14 01 00 16 05 02 19 09 24 07 21 08 04\
             13 25 22 18 10 02 06 12 23 11 03 15 17"
    diccionario = {}
    i = 0
    for item in lista.split():
        diccionario.__setitem__(chr(_ctoi("a") + i), item)
        i += 1
    return diccionario


def verificacion_longitud(valor):
    """Verifica que cada valor sea menor que 10, en caso
       contrario vuelvo a sumar sus digitos"""
    nuevo_valor = valor
    while nuevo_valor >= 10:
        nuevo_valor = 0
        for char in str(valor):
            nuevo_valor += int(char)
        if nuevo_valor >= 10:
            return verificacion_longitud(nuevo_valor)
    return nuevo_valor


def calculo_digito(lista):
    """Devuelve la suma reversa alternada de los
       valores de una lista pasada """
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
    respuesta = "Su digito de verificacion es: " + \
                "".join([str(valor_2), str(valor_1)])
    return respuesta


def reemplazo_patente(patente=""):
    """Verifica que la patente sea letras seguidas de numeros,
       y la convierte en una lista de enteros de 1 digito"""
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
