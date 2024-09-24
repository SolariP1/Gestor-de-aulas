import tkinter as tk
from tkinter import messagebox
from usuario import UsuarioApp as UserForm
from curso import Curso as Curform
from cidade import Cidade as Cidform
from professor import Professor as Profform
from aluno import aluno as Alunoform
from aulas import Aula as Aulaform
from tkinter import filedialog
from tkinter import *

class MainMenu:
    def __init__(self, master=None):
        self.master = master
        self.master.title("Menu Principal")
        self.master.state("zoomed")

        menubar = Menu(self.master)
        self.master.config(menu=menubar)

        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)
        filemenu3 = Menu(menubar)

        menubar.add_cascade(label='Arquivo', menu=filemenu)
        menubar.add_cascade(label='Cadastros', menu=filemenu2)
        menubar.add_cascade(label='Ajuda', menu=filemenu3)

        def Open():
            filedialog.askopenfilename()

        def Save():
            filedialog.asksaveasfilename()

        def Quit():
            self.master.quit()

        def Help():
            text = Text(self.master)
            text.pack()
            text.insert('insert', 'Ao clicar no botão da\n'
                                  'respectiva cor, o fundo da tela\n'
                                  'aparecerá na cor escolhida.')

        filemenu.add_command(label='Abrir...', command=Open)
        filemenu.add_command(label='Salvar como...', command=Save)
        filemenu.add_separator()
        filemenu.add_command(label='Sair', command=Quit)
        filemenu2.add_command(label='Usuários', command=self.open_user_screen)
        filemenu2.add_command(label='Professor', command=self.open_professor_screen)
        filemenu2.add_command(label='Aluno', command=self.open_aluno_screen)
        filemenu2.add_command(label='Curso', command=self.open_curso_screen)
        filemenu2.add_command(label='Cidade', command=self.open_cidade_screen)
        filemenu2.add_command(label='Aula', command=self.open_aula_screen)
        filemenu3.add_command(label='Ajuda', command=Help)

    def open_user_screen(self):
        self.new_window = tk.Toplevel(self.master)
        self.app = UserForm(self.new_window)

    def open_aula_screen(self):
        self.new_window = tk.Toplevel(self.master)
        self.app = Aulaform(self.new_window)

    def open_professor_screen(self):
        self.new_window = tk.Toplevel(self.master)
        self.app = Profform(self.new_window)

    def open_aluno_screen(self):
        self.new_window = tk.Toplevel(self.master)
        self.app = Alunoform(self.new_window)

    def open_curso_screen(self):
        self.new_window = tk.Toplevel(self.master)
        self.app = Curform(self.new_window)

    def open_cidade_screen(self):
        self.new_window = tk.Toplevel(self.master)
        self.app = Cidform(self.new_window)
