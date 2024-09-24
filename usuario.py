from tkinter import *
from tkinter import ttk, messagebox
from banco import conectar, close_connection

class UsuarioApp:
    def __init__(self, master=None):
        self.master = master
        self.master.title("Inserir Usuários")

        self.janela1 = Frame(master)
        self.janela1.pack(padx=10, pady=10)
        self.msg1 = Label(self.janela1, text="Informe os dados para o novo usuário:")
        self.msg1["font"] = ("Verdana", "14", "bold")
        self.msg1.pack()

        self.janela2 = Frame(master)
        self.janela2["padx"] = 20
        self.janela2.pack()
        self.nome_label = Label(self.janela2, text="Nome completo:")
        self.nome_label.pack(side="left")
        self.nome = Entry(self.janela2, width=30)
        self.nome.pack(side="left")

        self.janela3 = Frame(master)
        self.janela3["padx"] = 20
        self.janela3.pack(pady=5)
        self.username_label = Label(self.janela3, text="Usuário:")
        self.username_label.pack(side="left")
        self.username = Entry(self.janela3, width=30)
        self.username.pack(side="left")

        self.janela4 = Frame(master)
        self.janela4["padx"] = 20
        self.janela4.pack(pady=5)
        self.senha_label = Label(self.janela4, text="Senha:")
        self.senha_label.pack(side="left")
        self.senha = Entry(self.janela4, width=30, show="*")
        self.senha.pack(side="left")

        # Janela de botões para Cadastrar, Alterar e Excluir
        self.janela5 = Frame(master)
        self.janela5["padx"] = 20
        self.janela5.pack(pady=10)
        self.botao1 = Button(self.janela5, width=10, text="Cadastrar", command=self.inserir_usuario)
        self.botao1.pack(side="left")
        self.botao2 = Button(self.janela5, width=10, text="Alterar", command=self.alterarUsuario)
        self.botao2.pack(side="left")
        self.botao3 = Button(self.janela5, width=10, text="Excluir", command=self.excluirUsuario)
        self.botao3.pack(side="left")

        self.janela6 = Frame(master)
        self.janela6["padx"] = 20
        self.janela6.pack(pady=10)
        self.mensagem = Label(self.janela6, text="")
        self.mensagem["font"] = ("Verdana", "10", "italic", "bold")
        self.mensagem.pack()

        self.janela12 = Frame(master)
        self.janela12["padx"] = 20
        self.janela12.pack(pady=10)
        self.tree = ttk.Treeview(self.janela12, columns=("ID", "Nome", "Usuário", "Senha"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Usuário", text="Usuário")
        self.tree.heading("Senha", text="Senha")
        self.tree.pack()

        self.tree.bind("<ButtonRelease-1>", self.selecionar_linha)

        self.db = conectar()
        self.idusuario = None  # Atributo para armazenar o ID do usuário selecionado
        self.atualizarTabela()

    def inserir_usuario(self):
        nome = self.nome.get()
        username = self.username.get()
        senha = self.senha.get()

        if not nome or not username or not senha:
            self.mensagem.config(text="Preencha todos os campos!", fg="red")
            return

        if not self.db:
            self.mensagem.config(text="Erro: Sem conexão com o banco de dados", fg="red")
            return

        try:
            cursor = self.db.cursor()
            query = "INSERT INTO tbl_usuario (usu_nome, usu_username, usu_senha) VALUES (%s, %s, %s)"
            cursor.execute(query, (nome, username, senha))
            self.db.commit()
            self.mensagem.config(text="Usuário cadastrado com sucesso!", fg="green")
            self.atualizarTabela()  # Atualiza a tabela após a inserção

        except Exception as e:
            self.mensagem.config(text=f"Erro: {e}", fg="red")

        finally:
            cursor.close()

    def alterarUsuario(self):
        if self.idusuario:
            nome = self.nome.get()
            username = self.username.get()
            senha = self.senha.get()

            if not nome or not username or not senha:
                self.mensagem.config(text="Preencha todos os campos!", fg="red")
                return

            try:
                cursor = self.db.cursor()
                query = "UPDATE tbl_usuario SET usu_nome=%s, usu_username=%s, usu_senha=%s WHERE usu_codigo=%s"
                cursor.execute(query, (nome, username, senha, self.idusuario))
                self.db.commit()
                self.mensagem.config(text="Usuário alterado com sucesso!", fg="green")
                self.atualizarTabela()
            except Exception as e:
                self.mensagem.config(text=f"Erro: {e}", fg="red")
            finally:
                cursor.close()
        else:
            self.mensagem.config(text="Selecione um usuário para alterar", fg="red")

    def excluirUsuario(self):
        if self.idusuario:
            try:
                cursor = self.db.cursor()
                query = "DELETE FROM tbl_usuario WHERE usu_codigo=%s"
                cursor.execute(query, (self.idusuario,))
                self.db.commit()
                self.mensagem.config(text="Usuário excluído com sucesso!", fg="green")
                self.atualizarTabela()

            except Exception as e:
                self.mensagem.config(text=f"Erro: {e}", fg="red")

            finally:
                cursor.close()
        else:
            self.mensagem.config(text="Selecione um usuário para excluir", fg="red")

    def fechar(self):
        close_connection(self.db)
        self.master.destroy()

    def atualizarTabela(self):
        usuarios = self.selectAllUsers()
        self.tree.delete(*self.tree.get_children())
        for u in usuarios:
            self.tree.insert("", "end", values=(u[0], u[1], u[2], u[3]))

    def selecionar_linha(self, event):
        item_selecionado = self.tree.selection()
        if item_selecionado:
            valores = self.tree.item(item_selecionado[0], 'values')
            self.idusuario = valores[0]  # Armazena o ID do usuário selecionado
            self.nome.delete(0, END)
            self.nome.insert(END, valores[1])
            self.username.delete(0, END)
            self.username.insert(END, valores[2])
            self.senha.delete(0, END)
            self.senha.insert(END, valores[3])

    def selectAllUsers(self):
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT * FROM tbl_usuario")
            linhas = cursor.fetchall()
            cursor.close()
            return linhas
        except Exception as e:
            self.mensagem.config(text=f"Erro na recuperação dos usuários: {e}", fg="red")
            return []
