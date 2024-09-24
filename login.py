import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
from banco import conectar, close_connection
from principal import MainMenu as Mainform

class Login:
    def __init__(self, master=None):
        self.master = master
        self.master.title("Login")

        img = Image.open("imagem.jpg")
        img = img.resize((200, 200))
        self.photo = ImageTk.PhotoImage(img)

        self.image_label = tk.Label(self.master, image=self.photo)
        self.image_label.pack(pady=20, padx=20)

        self.janela1 = tk.Frame(master)
        self.janela1["padx"] = 20
        self.janela1.pack()
        self.usuario_label = tk.Label(self.janela1, text="Usuário:")
        self.usuario_label.pack(side="left")
        self.usuario = tk.Entry(self.janela1, width=20)
        self.usuario.pack(side="left")

        self.janela2 = tk.Frame(master)
        self.janela2["padx"] = 20
        self.janela2.pack()
        self.senha_label = tk.Label(self.janela2, text="Senha:")
        self.senha_label.pack(side="left")
        self.senha = tk.Entry(self.janela2, width=20, show="*")  # Oculta o texto da senha
        self.senha.pack(side="left")

        self.janela42 = tk.Frame(master)
        self.janela42["padx"] = 20
        self.janela42.pack()

        self.botao10 = tk.Button(self.janela42, width=10, text="Login", command=self.entrar)
        self.botao10.pack(side="left")

        self.janela6 = tk.Frame(master)
        self.janela6["padx"] = 20
        self.janela6.pack(pady=10)
        self.mensagem = tk.Label(self.janela6, text="")
        self.mensagem["font"] = ("Verdana", "10", "italic", "bold")
        self.mensagem.pack()

        self.db = conectar()

    def entrar(self):
        username = self.usuario.get()
        senha = self.senha.get()

        if not self.db:
            self.mensagem.config(text="Erro: Sem conexão com o banco de dados", fg="red")
            return

        try:
            cursor = self.db.cursor()
            query = "SELECT usu_senha FROM tbl_usuario WHERE usu_username = %s"
            cursor.execute(query, (username,))
            resultado = cursor.fetchone()

            if resultado and resultado[0] == senha:  # O índice 0 é a senha
                self.mensagem.config(text="Login bem-sucedido!", fg="green")
                self.abrir()

            else:
                self.mensagem.config(text="Erro na autenticação", fg="red")

        except mysql.connector.Error as err:
            self.mensagem.config(text=f"Erro: {err}", fg="red")

        finally:
            cursor.close()

    def fechar(self):
        if self.db:
            self.db.close()
        self.master.destroy()

    def abrir(self):
        self.master.withdraw()
        self.new_window = tk.Toplevel(self.master)
        self.app = Mainform(self.new_window)

root = tk.Tk()
app = Login(root)
root.mainloop()
