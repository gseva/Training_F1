# -*- coding: latin-1 -*-
'''
Created on 22/03/2013

**TECLADO   [ASISTENTE/DICCIONARIO]**

Una máquina inyectora de plástico, por tareas de mantenimiento y otros, puede
establecer comunicación con su filial mediante mensajes de texto. La mecánica
básica es, en principio, la misma que utilizaban los dispositivos móviles en
sus comienzos.
De este modo, un operador puede a manera de ejemplo, enviar un mensaje a la
casa matriz y solicitar ayuda sobre una tarea determinada (Ej. "Hola Juan,
tenemos un problema con el cilindro A45 que aparentemente se ha contaminado
con restos de ABS y no pudimos terminar de limpiarlo")
La máquina, cuenta con un teclado que entre otras tareas complementarias
permite la gestión de estos mensajes.
El objetivo es representar el comportamiento predictivo de los mensajes de
texto que enviaría la máquina.  Esta, dispone de un diccionario de palabras,
establecido de fábrica y de un algoritmo que va restringiendo las posibles
palabras que pueden ser resultado de la presión de una serie de teclas.
El mapeo de las teclas es el siguiente:

<1> 1

<2>    2,a,b,c

<3>    3,d,e,f

<4>    4,g,h,i

<5>    5,j,k,l

<6>    6,m,n,o

<7>    7,p,q,r,s

<8>    8,t,u,v

<9>    9,w,x,y,z

<0>    0

<#>    espacio

<*> -


De este modo, los caracteres se representan por medio de un átomo o de un
número entero.

*Es necesario realizar un sistema que*
1-    Definir el diccionario con la mayor cantidad de palabras conocidas
      (será de solo lectura)

2-    El usuario puede agregar nuevas palabras al diccionario y modificar
      las existentes

3-    El usuario solo puede listar las palabras que se incorporaron al
      diccionario

4-    Las teclas presionadas puede mostrar una palabra del diccionario y
      ser seleccionada o bien predecir una palabra por prefijos de la misma.

5-    La teclas presionadas pueden mostrar una palabra nueva a incorporar

6-    Las teclas presionadas generan una lista de caracteres que pueden
      representar palabras del diccionario o prefijo de las mismas (ej.
      A través, por qué, etc.)

7-    Todo mensaje puede ser modificado, antes de ser enviado

La solución debe ser vista como un conjunto. O sea, soluciones con las
mismas palabras pero en distinto orden deben ser consideradas como iguales
(no deben devolverse repetidos).


@author: sebastiang
'''

from Tkinter import *

from key_handler import key_handler
import tkMessageBox


class popup_word:
    """
    Una ventana emergente personalizada que pregunta al usuario la palabra
    que desea agregar al diccionario y la guarda en la base de datos
    """

    def __init__(self, parent):
        top = self.top = Toplevel(parent)
        Label(top, text="Ingrese palabra nueva").pack()
        self.e = Entry(top)
        self.e.pack(padx=5)

        b = Button(top, text="OK", command=self.ok)
        b.pack(pady=5)

    def ok(self):
        print "agregando palabra", self.e.get()
        k.list_to_node(k.string_to_code(self.e.get()), self.e.get(),
                     k.nodo_madre)
        self.top.destroy()


class Application(Frame):
    """
    La ventana principal, compuesta por una lista de botones especificada
    en key_handler y 2 ventanas de texto para el mensaje y la lista de palabras
    posibles. La interfaz gráfica utilizada es Tkinter, los elementos se
    posicionan con el sistema de columnas y filas.
    """

    def create_widgets(self, key_handler):
        """Agrega elementos a la ventana y los posiciona"""

        self.text = Text(self, height=5, width=50, bg="yellow",
                         wrap=WORD, state=DISABLED)
        self.text.grid(row=0, column=0, columnspan=2, rowspan=4,
                       sticky=E + W + S + N, padx=10)

        r = 0
        c = 2
        for index in range(0, (len(key_handler.botones) - 2)):
            rel = 'ridge'
            Button(self, text=key_handler.botones[index], height=2,
                   width=5, relief=rel).grid(row=r, column=c, sticky=E)
            c += 1
            if c > 4:
                c = 2
                r += 1
        b = Button(self, text=key_handler.botones[14], height=2, width=10)
        b.grid(row=6, column=3, columnspan=2, sticky=E + S)
        b = Button(self, text=key_handler.botones[15], height=2, width=10)
        b.grid(row=7, column=3, columnspan=2, sticky=E + S)
        self.label = Label(self, text="Posibles palabras")
        self.label.grid(row=5, column=0, sticky=W)
        self.text_palabras = Text(self, height=7, width=50, state=DISABLED)
        self.text_palabras.grid(row=6, column=0, columnspan=2, rowspan=2,
                                sticky=E + W + S + N, padx=10)

    def __init__(self, master=None, key_handler=None):
        Frame.__init__(self, master)
        self.pack()
        self.create_widgets(key_handler)

    def agregar_palabras(self, lista_palabras):
        """
        Agrega la lista de palabras posibles a la ventana de palabras
        posibles
        """

        self.text_palabras.configure(state='normal')
        self.text_palabras.delete(1.0, END)
        if lista_palabras:
            for palabra in lista_palabras:
                self.text_palabras.insert(END, palabra)
                self.text_palabras.insert(END, "\n")
        self.text_palabras.configure(state='disabled')

    def agregar_texto(self, texto):
        """
        Reemplaza el texto contenido en la ventana de mensaje por el
        pasado como parametro
        """
        self.text.configure(state='normal')
        self.text.delete(1.0, END)
        self.text.insert(END, texto)
        self.text.configure(state='disabled')

root = Tk()
k = key_handler()
app = Application(master=root, key_handler=k)


def callback(event):
    """
    Funcion disparada cada vez que se apreta el boton izquierdo del
    mouse dentro de la ventana. Verifica el texto del boton y procesa
    el evento.
    """

    if isinstance(event.widget, Button):
        if event.widget['text'].split("\n")[0] == "Agregar":
            d = popup_word(app)
            app.wait_window(d.top)
            return
        print event.widget["text"].split("\n")[0]
        lista_palabras, texto = k.procesar_texto(event.widget["text"]
                                                      .split("\n")[0])
        if event.widget['text'] == "Enviar":
            msg = tkMessageBox.showinfo("Enviado!", texto)
            texto = ""
        app.agregar_palabras(lista_palabras)
        app.agregar_texto(texto)


app.master.maxsize(630, 370)
app.master.minsize(630, 370)
app.master.bind("<Button-1>", callback)
root.mainloop()
root.destroy()
