'''
Created on 28/03/2013

@author: sebastiang
'''


from ZODB import FileStorage, DB
from nodo_prueba import Nodo
import transaction
import logging
logging.basicConfig()


storage = FileStorage.FileStorage('/tmp/test-filestorage13.fs')
db = DB(storage)
conn = db.open()
root = conn.root()

teclas = {1: "1", 2: ("2", "a", "b", "c"), 3: ("3", "d", "e", "f"),
          4: ("4", "g", "h", "i"), 5: ("5", "j", "k", "l"),
          6: ("6", "m", "n", "o"), 7: ("7", "p", "q", "r", "s"),
          8: ("8", "t", "u", "v"), 9: ("9", "w", "x", "y", "z"),
          0: "0", "#": " "}

nodo_madre = Nodo("madre")
root[nodo_madre.name] = nodo_madre

for tecla, contenido in teclas.items():
    print tecla, contenido
    try:
        int(tecla)
    except:
        break
    try:
        root["madre"][tecla] = Nodo(tecla)
    except:
        print "problema con tecla:", tecla

    for item in contenido:
        print root["madre"][tecla]
        root["madre"][tecla].agregar_palabra(item)

for item in root["madre"].values():
    for palabra in item.palabras:
        print item, "tiene palabra:", palabra


def list_to_node(lista, palabra, nodo):
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
    if not nodo.get(item):
        nodo.agregar_nodo(Nodo(item))
    list_to_node(lista[1:], palabra, nodo.get(item))


def txt_to_code():
    diccionario = []
    archivo = open("lista.txt", "r")
    for n, line in enumerate(archivo.read().split("\n")):
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


def code_to_list(code, nodo):
    lista_code = list(code)
    print "listaza:", lista_code
    item = lista_code[0]
    lista_code = lista_code[1:]
    print "item popeado:", item
    item = int(item)
    if not lista_code:
#        try:
        return nodo[item].devolver_palabras()
#        except:
#            return ["No hay tal palabra"]
    elif nodo[item]:
        return code_to_list((str(x) for x in lista_code),
                            nodo[item])
    else:
        return ["Algo ha sido malo"]

#start = time.time()
#for item in code_to_list("2", nodo_madre):
#    print item
#elapsed = (time.time() - start)
#start2 = time.time()
#for item in code_to_list("2", nodo_madre):
#    print item
#elapsed2 = (time.time() - start2)
#print "time:", elapsed
#print "time2", elapsed2

while True:
    ingreso = raw_input("codigo de cifras (q para salir):")
    if ingreso == "q":
        break
    try:
        int(ingreso)
    except:
        print "promt invalido"
        continue
    for item in code_to_list(ingreso, nodo_madre):
        print item

db.close()
