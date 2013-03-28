'''
Created on 25/03/2013

@author: sebastiang
'''
from random import choice
from ZODB import FileStorage, DB
from nodo import Nodo
import transaction


class key_handler():

    storage = FileStorage.FileStorage('/tmp/test-filestorage10.fs')
    db = DB(storage)
    conn = db.open()
    root = conn.root()

    nodo_madre = root['madre']

    teclas = {1: "1", 2: ("2", "a", "b", "c"), 3: ("3", "d", "e", "f"),
              4: ("4", "g", "h", "i"), 5: ("5", "j", "k", "l"),
              6: ("6", "m", "n", "o"), 7: ("7", "p", "q", "r", "s"),
              8: ("8", "t", "u", "v"), 9: ("9", "w", "x", "y", "z"),
              0: "0"}

    botones = ["1", "2\nabc", "3\ndef", "4\nghi", "5\njkl", "6\nmno",
               "7\npqrs", "8\ntuv", "9\nwxyz", "0", "#\nespacio", "Enviar",
               "Borrar", "Arriba", "Abajo", "Agregar\nPalabra"]

    def __init__(self):
        self.codigo_actual = []
        self.texto = ""
        self.palabras_mensaje = []
        self.palabras_posibles = []
        self.palabra_actual = ""
        self.caracter_nuevo = ""

    def string_to_code(self, string):
        codigo = []
        for char in string:
            codigo.append("".join([str(tecla) for tecla, contenido \
                         in self.teclas.items() \
                         if contenido.__contains__(char)]))
        return codigo

    def code_to_list(self, codigo, nodo):
        item = codigo[0]
        codigo = codigo[1:]
        item = int(item)
        if not codigo:
            try:
                return nodo.nodos[item].devolver_palabras()
            except:
                print "no encontre la palabra"
                return None  #["No hay tal palabra"]
        elif nodo.nodos[item]:
            return self.code_to_list(codigo,
                                nodo.nodos[item])
        else:
            return None  #["Algo ha sido malo"]

    def formar_texto(self):
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
        elif self.caracter_nuevo == " ":
            self.palabras_mensaje.append(self.palabra_actual)
            self.palabra_actual = ""
            self.texto += self.caracter_nuevo
            return self.texto
#        elif len(self.caracter_nuevo) == 1:
#            self.palabra_actual += self.caracter_nuevo
#            self.texto += self.caracter_nuevo
#            return self.texto
        else:
            if len(self.palabra_actual) >= 1:
                self.texto = self.texto[:-len(self.palabra_actual)]
            self.palabra_actual = self.caracter_nuevo
            self.texto += self.palabra_actual
            return self.texto

    def procesar_texto(self, tecla):
        while True:
            if tecla.startswith("#"):
                self.devolver_caracter(" ")
                break
            elif tecla == "Borrar":
                self.devolver_caracter("Borrar")
                break
            if self.palabra_actual:
                self.codigo_actual = self.string_to_code(self.palabra_actual)
                self.codigo_actual.extend([str(tecla)])
            else:
                self.codigo_actual = tecla
            self.palabras_posibles = self.code_to_list(self.codigo_actual,
                                                       self.nodo_madre)
            self.devolver_caracter(self.palabras_posibles)
            break
        return self.palabras_posibles, self.formar_texto()

    def devolver_caracter(self, data):
        self.caracter_nuevo = ""
        if data:
            if data == " ":
                self.caracter_nuevo = " "
            elif data == "Borrar":
                self.caracter_nuevo = "Borrar"
            else:
                l = len(self.codigo_actual)
                for palabra in data:
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

    def devolver_texto(self):
        pass
