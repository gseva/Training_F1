'''
Created on 26/03/2013

@author: sebastiang
'''

from ZODB import FileStorage, DB
from nodo import Nodo

storage = FileStorage.FileStorage('/tmp/test-filestorage10.fs')
db = DB(storage)
conn = db.open()
root = conn.root()

nodo_madre = root['madre']


def code_to_list(code, nodo):
    lista_code = list(code)
    print "listaza:", lista_code
    item = lista_code[0]
    lista_code = lista_code[1:]
    print "item popeado:", item
    item = int(item)
    if not lista_code:
#        try:
        return nodo.nodos[item].devolver_palabras()
#        except:
#            return ["No hay tal palabra"]
    elif nodo.nodos[item]:
        return code_to_list((str(x) for x in lista_code),
                            nodo.nodos[item])
    else:
        return ["Algo ha sido malo"]


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
