'''
Created on 26/03/2013

@author: sebastiang
'''
from persistent import Persistent


class Nodo(Persistent):

    def __init__(self):
        self.nodos = {1: None, 2: None, 3: None, 4: None, 5: None,
                      6: None, 7: None, 8: None, 9: None, 0: None}
        self.palabras = []

    def agregar_palabra(self, palabra):
        self.palabras.append(palabra)
        self._p_changed = True

    def agregar_nodo(self, nodo, index):
        self.nodos[index] = nodo
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
