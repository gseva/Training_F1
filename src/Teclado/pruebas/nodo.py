# -*- coding: latin-1 -*-
'''
Created on 26/03/2013

@author: sebastiang
'''
from persistent import Persistent


class Nodo(Persistent):
    """
    Clase de nodo, hereda de Persistent para poder ser guardada en la base de
    datos.

    self.nodos = diccionario con referencias a nodos transversales
    self.palabras = lista de palabras correspondiente a este nodo
    """

    def __init__(self):
        self.nodos = {1: None, 2: None, 3: None, 4: None, 5: None,
                      6: None, 7: None, 8: None, 9: None, 0: None}
        self.palabras = []

    def agregar_palabra(self, palabra):
        if not self.palabras.__contains__(palabra):
            self.palabras.append(palabra)
        self._p_changed = True

    def agregar_nodo(self, nodo, index):
        self.nodos[index] = nodo
        self._p_changed = True

    def devolver_palabras(self, numero_de_llamadas=4):
        """
        Devuelve la lista con palabras del nodo actual y los nodos a los
        que hace referencia, los cuales a su vez devuelven las palabras de
        los nodos referenciados recursivamente. Las veces que agrega las
        palabras de sus nodos 'hijos' se pueden limitar pasando como parametro
        (por defecto - 4 veces). Si se llama con -1 como parametro, devuelve
        todas las posibles palabras de si mismo y de todos los nodos hijos,
        nietos y demás.
        """
        inc = 1
        if numero_de_llamadas == -1:
            inc = 0
        string = []
        string.extend(self.palabras)
        if numero_de_llamadas == 0:
            return string
        for item in self.nodos.values():
            try:
                string.extend(item.devolver_palabras(numero_de_llamadas - inc))
            except:
                continue
        return string
