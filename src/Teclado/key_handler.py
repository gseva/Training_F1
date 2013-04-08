# -*- coding: latin-1 -*-
'''
Created on 25/03/2013

@author: sebastiang
'''

from random import choice
from ZODB import FileStorage, DB
from nodo import Nodo
import transaction


class key_handler():
    """
    Clase que interactua con las peticiones del usuario y la base de datos

    storage = el archivo de la base de datos
    teclas = diccionario de teclas y sus respectivas letras
    botones = lista de botones a crear en el gui
    """

    storage = FileStorage.FileStorage('/tmp/test-filestorage10.fs')
    db = DB(storage)
    conn = db.open()
    root = conn.root()

    nodo_madre = root['madre']

    teclas = {1: "1", 2: ("2", "a", "b", "c", "á"),
              3: ("3", "d", "e", "f", "é"),
              4: ("4", "g", "h", "i", "í"), 5: ("5", "j", "k", "l"),
              6: ("6", "m", "n", "o", "ó", "ñ"), 7: ("7", "p", "q", "r", "s"),
              8: ("8", "t", "u", "v", "ü", "ú"), 9: ("9", "w", "x", "y", "z"),
              0: "0"}

    botones = ["1", u"2\nabcá", u"3\ndefé", u"4\nghií", u"5\njkl", u"6\nmnoóñ",
               u"7\npqrs", u"8\ntuvúü", u"9\nwxyz", "0", "#\nespacio",
               "Borrar", "Arriba", "Abajo", "Agregar\nPalabra", "Enviar"]

    def __init__(self):
        self.codigo_actual = []
        self.caracter_nuevo = ""
        self.palabras_mensaje = []
        self.palabras_posibles = []
        self.palabra_actual = ""
        self.texto = ""

    def string_to_code(self, string):
        """Devuelve el codigo de teclas de una string"""

        codigo = []
        for char in string:
            codigo.append("".join([str(tecla) for tecla, contenido \
                         in self.teclas.items() \
                         if contenido.__contains__(char)]))
        return codigo

    def code_to_list(self, codigo, nodo):
        """
        Devuelve la lista de palabras posibles para el codigo
        pasado como parametro y sus derivados.
        """

        item = codigo[0]
        codigo = codigo[1:]
        item = int(item)
        if not codigo:
            try:
                palabras = nodo.nodos[item].devolver_palabras()
                if not palabras:
                    palabras = nodo.nodos[item].devolver_palabras(-1)
                return palabras
            except:
                print "no encontre la palabra"
                return None     #["No hay tal palabra"]
        elif nodo.nodos[item]:
            return self.code_to_list(codigo,
                                nodo.nodos[item])
        else:
            return None     #["Algo ha sido malo"]

    def formar_texto(self):
        """Devuelve el texto a imprimir en la ventana del mensaje de gui"""

        if self.caracter_nuevo == "Borrar":
            if not self.texto:
                return ""
            else:
                try:
                    self.palabra_actual = self.palabra_actual[:-1]
                except:
                    pass
                if self.texto[-1] == " ":
                    try:
                        self.palabra_actual = self.palabras_mensaje.pop()
                    except:
                        pass
                self.texto = self.texto[:-1]
                return self.texto
        elif self.caracter_nuevo == "Enviar":
            if not self.texto:
                texto_a_enviar = "No hay texto para enviar"
            else:
                texto_a_enviar = self.texto
                self.palabra_actual = ""
                self.texto = ""
            self.palabras_posibles = []
            return texto_a_enviar
        elif self.caracter_nuevo == " ":
            self.palabras_mensaje.append(self.palabra_actual)
            self.palabra_actual = ""
            self.texto += self.caracter_nuevo
            return self.texto
        else:
            if len(self.palabra_actual) >= 1:
                self.texto = self.texto[:-len(self.palabra_actual)]
            self.palabra_actual = self.caracter_nuevo
            self.texto += self.palabra_actual
            return self.texto

    def procesar_texto(self, tecla):
        """
        Verifica la tecla presionada y, si no es una tecla de comando,
        la agrega a la lista de codigo actual:
            - La lista de palabras posibles para el codigo actual
            - El texto a imprimir en pantalla
        """
        while True:
            if tecla.startswith("#"):
                self.devolver_palabra(" ")
                break
            elif tecla == "Borrar":
                self.devolver_palabra("Borrar")
                break
            elif tecla == "Arriba":
                self.devolver_palabra("Arriba")
                break
            elif tecla == "Abajo":
                self.devolver_palabra("Abajo")
                break
            elif tecla == "Enviar":
                self.devolver_palabra("Enviar")
                break
            if self.palabra_actual:
                self.codigo_actual = self.string_to_code(self.palabra_actual)
                self.codigo_actual.extend([str(tecla)])
            else:
                self.codigo_actual = tecla
            self.palabras_posibles = self.code_to_list(self.codigo_actual,
                                                       self.nodo_madre)
            self.devolver_palabra(self.palabras_posibles)
            break
        return self.palabras_posibles, self.formar_texto()

    def devolver_palabra(self, data):
        """
        Devuelve los primeros caracteres de la primera palabra en la lista de
        palabras posibles.
        La cantidad de caracteres corresponde a la cantidad de elementos en
        la lista de codigo actual. La lista gira, cambiando la primera y la
        ultima palabra por comandos 'Abajo' y 'Arriba'.
        Si data es un espacio u otro comando, no se devuelve nada.

        Por ejemplo:
            si el codigo actual es [2, 2, 2, 3, 3, 6], la palabra devuelta
            sera 'academ' y es la que corresponde a los primeros 6 caracteres
            de la palabra 'academia', correspondiente al index 0 de la lista de
            palabras posibles. Pero si cambio el index 2 veces con el comando
            'Abajo', la palabra devuelta va a ser 'abaden'.
        """

        self.caracter_nuevo = ""
        if data:
            if data == " ":
                self.caracter_nuevo = " "
                return
            elif data == "Borrar":
                self.caracter_nuevo = "Borrar"
                return
            elif data == "Enviar":
                self.caracter_nuevo = "Enviar"
                return
            elif data == "Arriba":
                self.palabras_posibles.append(self.palabras_posibles.pop(0))
            elif data == "Abajo":
                self.palabras_posibles.insert(0, self.palabras_posibles.pop())
            l = len(self.codigo_actual)
            palabra = self.palabras_posibles[0]
            print "agarro la palabra:", palabra
            if len(palabra) >= l:
                self.caracter_nuevo = palabra[:l]
                return
        else:
            print "no hay data"
            tecla_actual = self.codigo_actual[-1]
            try:
                self.caracter_nuevo = choice(self.teclas.get
                                            (int(tecla_actual)))
            except:
                self.caracter_nuevo = self.teclas.get(tecla_actual)

    def list_to_node(self, lista, palabra, nodo):
        """
        Procesa la palabra, crea los nodos necesarios y guarda
        la palabra en el nodo final
        """

        print "tengo lista", list, "palabra", palabra, "y nodo", nodo
        if len(lista) == 0:
            print "soy nodo:", nodo, "Y tengo palabra:", palabra
            if not nodo.palabras.__contains__(palabra):
                nodo.agregar_palabra(palabra)
            print "commiteando"
            transaction.commit()
            print "commitea2"
            return
        item = lista[0]
        try:
            item = int(item)
        except:
            return
        if not nodo.nodos[item]:
            nodo.agregar_nodo(Nodo(), item)
        self.list_to_node(lista[1:], palabra, nodo.nodos[item])
