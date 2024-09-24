from tkinter import *
from tkinter import ttk, messagebox
from banco import conectar, close_connection


class Cidade:
    def __init__(self, master=None):
        self.master = master
        self.master.title("Gerenciamento de Cidades")

        self.janela1 = Frame(master)
        self.janela1.pack(padx=10, pady=10)
        self.msg1 = Label(self.janela1, text="Cadastre uma cidade:")
        self.msg1["font"] = ("Verdana", "14", "bold")
        self.msg1.pack()

        self.janela2 = Frame(master)
        self.janela2["padx"] = 20
        self.janela2.pack()
        self.cidade_label = Label(self.janela2, text="Cidade:")
        self.cidade_label.pack(side="left")
        self.cidade = Entry(self.janela2, width=30)
        self.cidade.pack(side="left")

        self.janela3 = Frame(master)
        self.janela3["padx"] = 20
        self.janela3.pack(pady=5)
        self.uf_label = Label(self.janela3, text="UF:")
        self.uf_label.pack(side="left")
        self.uf = Entry(self.janela3, width=28)
        self.uf.pack(side="left")

        self.janela4 = Frame(master)
        self.janela4["padx"] = 20
        self.janela4.pack(pady=5)
        self.botao = Button(self.janela4, width=10, text="Inserir", command=self.inserir_cidade)
        self.botao.pack(side="left")
        self.botao2 = Button(self.janela4, width=10, text="Alterar", command=self.alterarCidade)
        self.botao2.pack(side="left")
        self.botao3 = Button(self.janela4, width=10, text="Excluir", command=self.excluirCidade)
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
        self.tree = ttk.Treeview(self.janela12, columns=("ID", "Cidade", "UF"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Cidade", text="Cidade")
        self.tree.heading("UF", text="UF")
        self.tree.pack()

        self.tree.bind("<ButtonRelease-1>", self.selecionar_linha)

        self.db = conectar()
        self.idcidade = None  # Atributo para armazenar o ID da cidade selecionada
        self.atualizarTabela()

    def inserir_cidade(self):
        cidade_nome = self.cidade.get()
        uf = self.uf.get()

        if not cidade_nome or not uf:
            self.mensagem.config(text="Preencha todos os campos!", fg="red")
            return

        if not self.db:
            self.mensagem.config(text="Erro: Sem conexão com o banco de dados", fg="red")
            return

        try:
            cursor = self.db.cursor()
            query = "INSERT INTO tbl_cidade (cid_nome, cid_uf) VALUES (%s, %s)"
            cursor.execute(query, (cidade_nome, uf))
            self.db.commit()
            self.mensagem.config(text="Cidade cadastrada com sucesso!", fg="green")
            self.atualizarTabela()  # Atualiza a tabela após a inserção

        except Exception as e:
            self.mensagem.config(text=f"Erro: {e}", fg="red")

        finally:
            cursor.close()

    def fechar(self):
        close_connection(self.db)
        self.master.destroy()

    def atualizarTabela(self):
        cidades = self.selectAllCidades()
        self.tree.delete(*self.tree.get_children())
        for c in cidades:
            self.tree.insert("", "end", values=(c[0], c[1], c[2]))

    def selecionar_linha(self, event):
        item_selecionado = self.tree.selection()
        if item_selecionado:
            valores = self.tree.item(item_selecionado[0], 'values')
            self.idcidade = valores[0]  # Armazena o ID da cidade selecionada
            self.cidade.delete(0, END)
            self.cidade.insert(END, valores[1])
            self.uf.delete(0, END)
            self.uf.insert(END, valores[2])

    def selectAllCidades(self):
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT cid_codigo, cid_nome, cid_uf FROM tbl_cidade")
            linhas = cursor.fetchall()
            cursor.close()
            return linhas
        except Exception as e:
            self.mensagem.config(text=f"Erro na recuperação das cidades: {e}", fg="red")
            return []

    def alterarCidade(self):
        if self.idcidade:
            cidade_nome = self.cidade.get()
            uf = self.uf.get()

            if not cidade_nome or not uf:
                self.mensagem.config(text="Preencha todos os campos!", fg="red")
                return

            try:
                cursor = self.db.cursor()
                query = "UPDATE tbl_cidade SET cid_nome=%s, cid_uf=%s WHERE cid_codigo=%s"
                cursor.execute(query, (cidade_nome, uf, self.idcidade))
                self.db.commit()
                self.mensagem.config(text="Cidade alterada com sucesso!", fg="green")
                self.atualizarTabela()
            except Exception as e:
                self.mensagem.config(text=f"Erro: {e}", fg="red")
            finally:
                cursor.close()
        else:
            self.mensagem.config(text="Selecione uma cidade para alterar", fg="red")

    def excluirCidade(self):
        if self.idcidade:
            try:
                cursor = self.db.cursor()

                # Verifica se a cidade está cadastrada em clientes
                cursor.execute("SELECT * FROM tbl_professores, tbl_alunos WHERE cid_codigo=%s ", (self.idcidade,))
                cadastrada = cursor.fetchone()

                if cadastrada:
                    messagebox.showerror("Erro", "Cidade não pode ser excluída porque está cadastrada em clientes!")
                else:
                    query = "DELETE FROM tbl_cidade WHERE cid_codigo=%s"
                    cursor.execute(query, (self.idcidade,))
                    self.db.commit()
                    self.mensagem.config(text="Cidade excluída com sucesso!", fg="green")
                    self.atualizarTabela()
            except Exception as e:
                self.mensagem.config(text=f"Erro: {e}", fg="red")
            finally:
                cursor.close()
        else:
            self.mensagem.config(text="Selecione uma cidade para excluir", fg="red")
