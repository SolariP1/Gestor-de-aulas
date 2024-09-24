from tkinter import *
from tkinter import ttk, messagebox

class Aula:
    def __init__(self, master=None):
        self.master = master
        self.master.title("Cadastro de aulas")

        self.janela1 = Frame(master)
        self.janela1.pack(padx=10, pady=10)
        self.msg1 = Label(self.janela1, text="Cadastro de aulas:")
        self.msg1["font"] = ("Verdana", "14", "bold")
        self.msg1.pack()

        self.janela2 = Frame(master)
        self.janela2["padx"] = 20
        self.janela2.pack()
        self.horario_label = Label(self.janela2, text="Horário da aula:")
        self.horario_label.pack(side="left")
        self.horario = Entry(self.janela2, width=30)
        self.horario.pack(side="left")

        self.janela2 = Frame(master)
        self.janela2["padx"] = 20
        self.janela2.pack()
        self.sala_label = Label(self.janela2, text="Sala:")
        self.sala_label.pack(side="left")
        self.sala = Entry(self.janela2, width=30)
        self.sala.pack(side="left")

