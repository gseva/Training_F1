'''
Created on 22/03/2013

@author: sebastiang
'''

from Tkinter import *
from key_handler import key_handler


class Application(Frame):

    def create_widgets(self, key_handler):
        self.text = Text(self, height=5, width=50,
                         bg="yellow", wrap=WORD, state=DISABLED)
        self.text.grid(row=0, column=0, columnspan=5)
        r = 1
        c = 0
        for b in key_handler.botones:
            rel = 'ridge'
            Button(self, text=b, height=2, width=5, relief=rel).grid(row=r,
                                                                     column=c)
            c += 1
            if c > 2:
                c = 0
                r += 1
        r += 1
        self.label = Label(self, text="Posibles palabras", padx=5, pady=5)
        self.label.grid(row=10, column=0, columnspan=5)
        r += 1
        self.text_palabras = Text(self, height=5, width=50, state=DISABLED)
        self.text_palabras.grid(row=11, column=0, columnspan=5)

    def __init__(self, master=None, key_handler=None):
        Frame.__init__(self, master)
        self.pack()
        self.create_widgets(key_handler)

    def agregar_palabras(self, lista_palabras):
        self.text_palabras.configure(state='normal')
        self.text_palabras.delete(1.0, END)
        if lista_palabras:
            for palabra in lista_palabras:
                self.text_palabras.insert(END, palabra)
                self.text_palabras.insert(END, "\n")
        self.text_palabras.configure(state='disabled')

    def agregar_texto(self, texto):
        self.text.configure(state='normal')
        self.text.delete(1.0, END)
        self.text.insert(END, texto)
        self.text.configure(state='disabled')

root = Tk()
k = key_handler()
app = Application(master=root, key_handler=k)


def callback(event):
    if isinstance(event.widget, Button):
        print event.widget["text"].split("\n")[0]
        print "hola soy callback"
        lista_palabras, texto = k.procesar_texto(event.widget["text"].split("\n")[0])
        app.agregar_palabras(lista_palabras)
        app.agregar_texto(texto)


app.master.geometry("500x500")
app.master.maxsize(500, 500)
app.master.bind("<Button-1>", callback)
root.mainloop()
root.destroy()
