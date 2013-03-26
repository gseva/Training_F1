'''
Created on 26/03/2013

@author: sebastiang
'''


from ZODB import FileStorage, DB
from BTrees.OOBTree import OOBTree
from persistent import Persistent
#
#storage = FileStorage.FileStorage('/tmp/test-filestorage.fs')
#db = DB(storage)
#conn = db.open()

teclas = {1: "1", 2: ("2", "a", "b", "c"), 3: ("3", "d", "e", "f"),
          4: ("4", "g", "h", "i"), 5: ("5", "j", "k", "l"),
          6: ("6", "m", "n", "o"), 7: ("7", "p", "q", "r", "s"),
          8: ("8", "t", "u", "v"), 9: ("9", "w", "x", "y", "z"),
          0: "0", "#": " "}


class Nodo():

    def __init__(self):
        self.lista_nodos = [None, None, None, None, None,
                   None, None, None, None, None]
        self.lista_palabras = []

    def agregar_palabra(self, palabra):
        self.lista_palabras.append(palabra)

    def agregar_nodo(self, nodo, index):
        self.lista_nodos[index] = nodo

    def devolver_palabras(self):
        string = []
        string.extend(self.lista_palabras)
        for item in self.lista_nodos:
            try:
                string.extend(item.devolver_palabras())
            except:
                continue
        return string

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


def list_to_node(lista, palabra, nodo):
#    print "mi lista es:", lista
#    print "estoy en nodo:", nodo
    if len(lista) == 1:
        print "soy nodo:", nodo, "Y tengo palabra:", palabra
        nodo.agregar_palabra(palabra)
        return
    item = lista[0]
#    print "estoy con item:", item
    try:
        item = int(item)
    except:
        return
    if not nodo.lista_nodos[item]:
        nodo.agregar_nodo(Nodo(), item)
    list_to_node(lista[1:], palabra, nodo.lista_nodos[item])


def txt_to_code():
    diccionario = []
    archivo = open("lista.txt", "r")
    porcentaje = 0
    for n, line in enumerate(archivo.read().split("\n")):
        if n == 895:
            n = 0
            porcentaje += 1
            print "terminado un " + str(porcentaje) + "%"
        diccionario.append(unicode(line.split(" ", 1)[0]))
    archivo.close
    lista_palabras = []
    for item in diccionario:
        lista_items = []
        for char in item:
            lista_items.append(
            "".join([str(tecla) for tecla, contenido in teclas.items() \
                         if contenido.__contains__(char)]),
            )
        lista_palabras.append(lista_items)
        list_to_node(lista_items, item, nodo_madre)
#    print lista_palabras
    return lista_palabras


def code_to_list(code, nodo):
    lista_code = list(code)
    print "listaza:", lista_code
    item = lista_code[0]
    lista_code = lista_code[1:]
    print "item popeado:", item
    item = int(item)
    if not lista_code:
        try:
            return nodo.lista_nodos[item].devolver_palabras()
        except:
            return "No hay tal palabra"
    elif nodo.lista_nodos[item]:
        return code_to_list((str(x) for x in lista_code),
                            nodo.lista_nodos[item])
    else:
        return "Algo ha sido malo"


class Index(OOBTree):
    pass


palabras = txt_to_code()
while True:
    ingreso = raw_input("prompt (q para salir):")
    if ingreso == "q":
        break
    try:
        int(ingreso)
    except:
        print "promt invalido"
        continue
    for item in code_to_list(ingreso, nodo_madre):
        print item
