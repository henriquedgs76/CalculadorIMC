import tkinter as tk
from tkinter import ttk
import sqlite3

class CalculadoraIMC:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de IMC")
        self.root.geometry("600x400")
        self.root.configure(bg="#2E2E2E")

        self.logo_label = tk.Label(self.root, text="Calculadora de IMC (Henrique)", font=("Helvetica", 16, "bold"), bg="#2E2E2E", fg="white")
        self.logo_label.pack(pady=10)

        self.nome_label = tk.Label(self.root, text="Nome:", font=("Helvetica", 12), bg="#2E2E2E", fg="white")
        self.nome_label.pack(pady=5)

        self.nome_entry = tk.Entry(self.root, font=("Helvetica", 12))
        self.nome_entry.pack(pady=5)

        self.peso_label = tk.Label(self.root, text="Peso (kg):", font=("Helvetica", 12), bg="#2E2E2E", fg="white")
        self.peso_label.pack(pady=5)

        self.peso_entry = tk.Entry(self.root, font=("Helvetica", 12))
        self.peso_entry.pack(pady=5)

        self.altura_label = tk.Label(self.root, text="Altura (m):", font=("Helvetica", 12), bg="#2E2E2E", fg="white")
        self.altura_label.pack(pady=5)

        self.altura_entry = tk.Entry(self.root, font=("Helvetica", 12))
        self.altura_entry.pack(pady=5)

        self.calcular_button = tk.Button(self.root, text="Calcular IMC", command=self.calcular_imc, font=("Helvetica", 12), bg="#4CAF50", fg="white")
        self.calcular_button.pack(pady=10)

        self.resultado_label = tk.Label(self.root, text="", font=("Helvetica", 12), bg="#2E2E2E", fg="white")
        self.resultado_label.pack(pady=10)

        # Configuração da tabela
        self.tree = ttk.Treeview(self.root, columns=("ID", "Nome", "Peso", "Altura", "IMC", "Classificação"), show="headings", height=5)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Peso", text="Peso")
        self.tree.heading("Altura", text="Altura")
        self.tree.heading("IMC", text="IMC")
        self.tree.heading("Classificação", text="Classificação")
        self.tree.pack(pady=20)

        # Botão para exibir usuários
        self.exibir_button = tk.Button(self.root, text="Exibir Usuários", command=self.exibir_usuarios, font=("Helvetica", 12), bg="#2196F3", fg="white")
        self.exibir_button.pack(pady=5)

        # Botão para excluir usuário
        self.excluir_button = tk.Button(self.root, text="Excluir Usuário", command=self.excluir_usuario, font=("Helvetica", 12), bg="#FF5722", fg="white")
        self.excluir_button.pack(pady=5)

        # Conectar ao banco de dados SQLite
        self.conexao = sqlite3.connect("calculador.db")
        self.cursor = self.conexao.cursor()

        # Criar tabela se não existir
        self.cursor.execute("CREATE TABLE IF NOT EXISTS calculador (id INTEGER PRIMARY KEY, nome TEXT, peso REAL, altura REAL)")
        self.conexao.commit()

    def calcular_imc(self):
        try:
            peso = float(self.peso_entry.get())
            altura = float(self.altura_entry.get())
            imc = peso / (altura ** 2)
            classificacao = self.obter_classificacao(imc)

            nome = self.nome_entry.get()

            # Inserir dados no banco de dados
            self.cursor.execute("INSERT INTO calculador (nome, peso, altura) VALUES (?, ?, ?)", (nome, peso, altura))
            self.conexao.commit()

            # Atualizar a tabela na interface gráfica
            self.atualizar_tabela()

            resultado_texto = f"IMC: {imc:.2f} - {classificacao}"
            self.resultado_label.config(text=resultado_texto)

            # Agendar a limpeza da tela após 10 segundos
            self.root.after(10000, self.limpar_tela)

        except ValueError:
            self.resultado_label.config(text="Por favor, insira valores válidos para peso e altura.")

    def obter_classificacao(self, imc):
        if imc < 18.5:
            return "Abaixo do peso"
        elif 18.5 <= imc < 24.9:
            return "Peso normal"
        elif 25 <= imc < 29.9:
            return "Sobrepeso"
        else:
            return "Obeso"

    def atualizar_tabela(self):
        # Limpar dados existentes na tabela
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Selecionar todos os dados da tabela no banco de dados
        self.cursor.execute("SELECT * FROM calculador")
        rows = self.cursor.fetchall()

        # Inserir dados na tabela na interface gráfica
        for row in rows:
            self.tree.insert("", "end", values=row)

    def exibir_usuarios(self):
        # Atualizar a tabela na interface gráfica
        self.atualizar_tabela()

    def excluir_usuario(self):
        # Obter ID do item selecionado na tabela
        selected_item = self.tree.selection()
        if not selected_item:
            return

        # Obter ID do usuário selecionado
        user_id = self.tree.item(selected_item, "values")[0]

        # Excluir usuário do banco de dados
        self.cursor.execute("DELETE FROM calculador WHERE id=?", (user_id,))
        self.conexao.commit()

        # Atualizar a tabela na interface gráfica após exclusão
        self.atualizar_tabela()

    def limpar_tela(self):
        # Limpar os campos após 10 segundos
        self.nome_entry.delete(0, tk.END)
        self.peso_entry.delete(0, tk.END)
        self.altura_entry.delete(0, tk.END)
        self.resultado_label.config(text="")

    def ao_fechar(self):
        self.conexao.close()
        self.root.destroy()

        

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraIMC(root)
    root.protocol("WM_DELETE_WINDOW", app.ao_fechar)
    root.mainloop()
