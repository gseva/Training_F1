'''
Created on 26/03/2013

@author: sebastiang
'''


from ZODB import FileStorage, DB
from nodo import Nodo
import transaction
import logging
logging.basicConfig()

storage = FileStorage.FileStorage('/tmp/test-filestorage10.fs')
db = DB(storage)
conn = db.open()
root = conn.root()

teclas = {1: "1", 2: ("2", "a", "b", "c"), 3: ("3", "d", "e", "f"),
          4: ("4", "g", "h", "i"), 5: ("5", "j", "k", "l"),
          6: ("6", "m", "n", "o"), 7: ("7", "p", "q", "r", "s"),
          8: ("8", "t", "u", "v"), 9: ("9", "w", "x", "y", "z"),
          0: "0", "#": " "}

nodo_madre = Nodo()
root['madre'] = nodo_madre

for tecla, contenido in teclas.items():
    print tecla, contenido
    try:
        int(tecla)
    except:
        break
    try:
        nodo_madre.agregar_nodo(Nodo(), tecla)
    except:
        print "problema con tecla:", tecla

    for item in contenido:
        print nodo_madre.nodos[tecla]
        nodo_madre.nodos[tecla].agregar_palabra(item)

for item in nodo_madre.nodos.values():
    for palabra in item.palabras:
        print item, "tiene palabra:", palabra


def list_to_node(lista, palabra, nodo):
    if len(lista) == 0:
#        print "soy nodo:", nodo, "Y tengo palabra:", palabra
        if not nodo.palabras.__contains__(palabra):
            nodo.agregar_palabra(palabra)
        return
    item = lista[0]
    try:
        item = int(item)
    except:
        return
    if not nodo.nodos[item]:
        nodo.agregar_nodo(Nodo(), item)
    list_to_node(lista[1:], palabra, nodo.nodos[item])


def txt_to_code():
    diccionario = []
    archivo = open("lista_bkp.txt", "r")
    porcentaje = 0
    for n, line in enumerate(archivo.read().split("\n")):
        if n % 895 == 0:
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
    return lista_palabras

print "cargando palabras"
palabras = txt_to_code()
print "commiteando, no apagar"
transaction.commit()
print "listo"
db.close()
