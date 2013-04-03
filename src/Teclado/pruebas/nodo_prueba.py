'''
Created on 28/03/2013

@author: sebastiang
'''
from BTrees.OOBTree import BTree


class Nodo(BTree):

    def __init__(self, name):
        BTree.__init__(self)
        self.update = {1: None, 2: None, 3: None, 4: None, 5: None,
                       6: None, 7: None, 8: None, 9: None, 0: None}
        self.palabras = []
        self.name = name

    def agregar_palabra(self, palabra):
        self.palabras.append(palabra)
        print "soy nodo", self, "y tengo palabra", self.palabras
        self._p_changed = True

    def agregar_nodo(self, nodo):
        self[nodo.name] = nodo
        self._p_changed = True

    def devolver_palabras(self):
        string = []
        string.extend(self.palabras)
        for item in self.nodos.values():
            try:
                string.extend(item.devolver_palabras())
            except:
                continue
        return string
