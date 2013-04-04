# -*- coding: latin-1 -*-
'''
Created on 26/03/2013

@author: sebastiang
'''

"""
Este scrpit:
    - Crea el nodo madre que tendrá referencia a los nodos con las primeras
      letras
    - Lee el archivo en la funcion txt_to_code (se puede especificar como
      parametro - lista_bkp.txt por defecto)
    - Transforma cada palabra en el archivo en una lista de codigo
      correspondiente, especificado en el diccionario teclas
    - Guarda cada palabra en un nodo. Crea los nodos necesarios
    - Guarda cada nodo en la base de datos con sus respectivas referencias
      y su lista de palabras

    Por ejemplo:
        Si quiero agregar la palabra "hola", su codigo segun el diccionario
        'teclas' sera: [4, 6, 5, 2]. Entonces dentro del nodo madre se creará
        referencia a un nuevo nodo 4, que a su vez referenciará al nodo 6,
        que referenciará al nodo 5, que finalmente referenciará al nodo 2
        donde voy a guardar la palabra 'hola'. Ahora, si quiero agregar la
        palabra 'hoja' que tiene el mismo código, no voy a necesitar crear más
        nodos, directamente extiendo la lista de palabras del último nodo 2
        con la string 'hoja'.
        Desde la base de datos podré acceder a estas palabras con:
        >>> root['madre'].nodos[4].nodos[6].nodos[5].nodos[2].palabras
            ["hola", "hoja"]

    El sistema es rebuscado y pesado, pero veloz a la hora de buscar palabras y
    devolver listas de palabras.
"""

from ZODB import FileStorage, DB
from nodo import Nodo
import transaction
import logging
logging.basicConfig()

storage = FileStorage.FileStorage('/tmp/test-filestorage10.fs')
db = DB(storage)
conn = db.open()
root = conn.root()

cantidad_nodos = 0
cantidad_palabras = 0

teclas = {1: "1", 2: ("2", "a", "b", "c", "á"),
          3: ("3", "d", "e", "f", "é"),
          4: ("4", "g", "h", "i", "í"), 5: ("5", "j", "k", "l"),
          6: ("6", "m", "n", "o", "ó", "ñ"), 7: ("7", "p", "q", "r", "s"),
          8: ("8", "t", "u", "v", "ü", "ú"), 9: ("9", "w", "x", "y", "z"),
          0: "0", "#": " "}

if not 'madre' in root.keys():
    nodo_madre = Nodo()
    root['madre'] = nodo_madre
else:
    nodo_madre = root['madre']

for tecla, contenido in teclas.items():
    print tecla, contenido
    try:
        int(tecla)
    except:
        break
    try:
        if not nodo_madre.nodos[tecla]:
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
    """
    Segun el codigo pasado crea nodos recursivamente (si no están
    creados), hasta llegar al final de la lista. Cuando se acaba
    la lista, a la lista de nodo actual se le agrega la palabra.
    """

    global cantidad_nodos
    if len(lista) == 0:
        if not nodo.palabras.__contains__(palabra):
            nodo.agregar_palabra(palabra)
            print "soy nodo", nodo, "y tengo palabra", palabra
        return
    item = lista[0]
    try:
        item = int(item)
    except:
        return
    if not nodo.nodos[item]:
        print "Creo un nuevo nodo"
        cantidad_nodos += 1
        nodo.agregar_nodo(Nodo(), item)
    list_to_node(lista[1:], palabra, nodo.nodos[item])


def txt_to_code(archivo="lista_bkp.txt"):
    """
    Lee el archivo en busqueda de palabras separadas por saltos de linea
    y espacios, y las guarda en una lista diccionario. Luego, recorre el
    diccionario, y para cada palabra crea un codigo correspondiente.
    Finalmente llama a la funcion list_to_node, pasandole el codigo y su 
    respectiva palabra.

    Devuelve la lista de codigos del diccionario.
    """

    global cantidad_palabras
    diccionario = []
    archivo = open(archivo, "r")
    for n, line in enumerate(archivo.read().split("\n")):
        for item in line.split(" "):
            diccionario.append(item.decode("utf-8"))
    archivo.close
    lista_palabras = []
    for n, item in enumerate(diccionario):
        if n % 3000 == 0:
            transaction.commit()
            print "commiteando"
        lista_items = []
        for char in item:
            lista_items.append(
            "".join([str(tecla) for tecla, contenido in teclas.items() \
                         if contenido.__contains__(char)]),
            )
        lista_palabras.append(lista_items)
        list_to_node(lista_items, item, nodo_madre)
        cantidad_palabras += 1
    return lista_palabras

print "cargando palabras"
palabras = txt_to_code()
print "commiteando, no apagar"
transaction.commit()
print "nodos creados:", cantidad_nodos, "palabras guardadas:", cantidad_palabras
print "listo"
db.close()
