'''
Created on 26/03/2013

@author: sebastiang
'''


from ZODB import FileStorage, DB
from BTrees.OOBTree import OOBTree
from persistent import Persistent

storage = FileStorage.FileStorage('/tmp/test-filestorage.fs')
db = DB(storage)
conn = db.open()

teclas = {1: "1", 2: ("2", "a", "b", "c"), 3: ("3", "d", "e", "f"),
          4: ("4", "g", "h", "i"), 5: ("5", "j", "k", "l"),
          6: ("6", "m", "n", "o"), 7: ("7", "p", "q", "r", "s"),
          8: ("8", "t", "u", "v"), 9: ("9", "w", "x", "y", "z"),
          0: "0", "#": " "}

tupa = (1, 2, 3, 4, "5")


class Nodo():

    def __init__(self):
        self.lista_nodos = [None, None, None, None, None,
                   None, None, None, None, None]
        self.lista_palabras = []

    def agregar_palabra(self, palabra):
        self.lista_palabras.append(palabra)

    def agregar_nodo(self, nodo, index):
        self.lista_nodos[index] = nodo

nodo_madre = Nodo()

for tecla, contenido in teclas.items():
    print tecla, contenido
    try:
        int(tecla)
    except:
        break
    nodo_madre.agregar_nodo(Nodo(), tecla)
    try:
        nodo_madre.agregar_nodo(Nodo(), tecla)
    except:
        print "problema con tecla:", tecla

    for item in contenido:
        print nodo_madre.lista_nodos[tecla]
        nodo_madre.lista_nodos[tecla].agregar_palabra(item)

for item in nodo_madre.lista_nodos:
    for palabra in item.lista_palabras:
        print item, "tiene palabra:", palabra



def txt_to_code():
    diccionario = []
    lista = open("lista.txt", "r")
    for n, line in enumerate(lista.read().split("\n")):
        if n % 5000 == 0:
            print n
        diccionario.append(unicode(line.split(" ", 1)[0]))
    lista.close
    lista_palabras = []
    for item in diccionario:
        lista_items = []
        for char in item:
            lista_items.append(
            "".join([str(tecla) for tecla, contenido in teclas.items() \
                         if contenido.__contains__(char)]),
            )
        lista_palabras.append(lista_items)
    print lista_palabras
    return lista_palabras


def code_to_string(code, lista_palabras):
    lista_strings = []
    lista_code = list(code)
    i = 0
    print lista_palabras


def list_to_node(lista):
    for palabra in lista:
        for i in len(palabra):
            pass


def devolver_palabras(list):
    if len(list):
        pass


class Index(OOBTree):
    pass


palabras = txt_to_code()
code_to_string("234", palabras)
print nodo_madre.lista_nodos[4].lista_palabras
print nodo_madre.lista_nodos[6].lista_palabras
print nodo_madre.lista_nodos[8].lista_palabras
