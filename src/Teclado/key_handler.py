'''
Created on 25/03/2013

@author: sebastiang
'''
from random import choice


teclas = {1: "1", 2: ("2", "a", "b", "c"), 3: ("3", "d", "e", "f"),
          4: ("4", "g", "h", "i"), 5: ("5", "j", "k", "l"),
          6: ("6", "m", "n", "o"), 7: ("7", "p", "q", "r", "s"),
          8: ("8", "t", "u", "v"), 9: ("9", "w", "x", "y", "z"),
          0: "0", "#": "espacio"}

botones = ["1", "2\nabc", "3\ndef", "4\nghi", "5\njkl", "6\nmno",
           "7\npqrs", "8\ntuv", "9\nwxyz", "0", "#\nespacio", "Enviar",
           "Borrar"]

diccionario = ["hola", "como", "estas", "amigo", "soy", "todo",
              "un", "campeon", "volvi", "del", "super", "que",
              "paso", "programo", "en", "python", "por", "helado",
              "actualmente", "porque", "soy", "hindu", "buenas"]

global _tecla_actual


def procesar_texto(ingreso, palabra_actual):
    lista_palabras = []
    valor = ""
    if ingreso.startswith("#"):
        return " ", " "
    if ingreso == "Borrar":
        return "Borrar", "Borrar"
    for part in ingreso.split("\n"):
        valor += part
        print "valor: ", valor
    for palabra in diccionario:
        for char in valor:
            pedazo = palabra_actual + char
            if palabra.startswith(pedazo):
                lista_palabras.append(palabra)
    print "sorted(lista_palabras):", sorted(lista_palabras)
    return sorted(lista_palabras), valor


def devolver_caracter(lista_palabras, palabra_actual, tecla):
    if lista_palabras:
        if lista_palabras == " ":
            return " "
        elif lista_palabras == "Borrar":
            return "Borrar"
        else:
            l = len(palabra_actual)
            return lista_palabras[0][l:l + 1]
    else:
        print "tecla_actual: ", tecla
        try:
            return tecla[choice(range(1, 3, 1))]
        except:
            return tecla[0]
