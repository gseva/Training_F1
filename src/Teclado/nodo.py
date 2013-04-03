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

    def devolver_palabras(self, numero_de_llamadas=0):
        inc = 1
        if numero_de_llamadas == -1:
            inc = 0
        string = []
        string.extend(self.palabras)
        if numero_de_llamadas == 4:
            return string
        for item in self.nodos.values():
            try:
                string.extend(item.devolver_palabras(numero_de_llamadas + inc))
            except:
                continue
        return string
