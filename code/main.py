from Utils import Utils
#import os
import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText


tabelas_bd_vendas = {
    "Categoria": [
        ("idCategoria", "INT"),
        ("Descricao", "VARCHAR")
    ],
    "Produto": [
        ("idProduto", "INT"),
        ("Nome", "VARCHAR"),
        ("Descricao", "VARCHAR"),
        ("Preco", "DECIMAL"),
        ("QuantEstoque", "DECIMAL"),
        ("Categoria_idCategoria", "INT")
    ],
    "TipoCliente": [
        ("idTipoCliente", "INT"),
        ("Descricao", "VARCHAR")
    ],
    "Cliente": [
        ("idCliente", "INT"),
        ("Nome", "VARCHAR"),
        ("Email", "VARCHAR"),
        ("Nascimento", "DATETIME"),
        ("Senha", "VARCHAR"),
        ("TipoCliente_idTipoCliente", "INT"),
        ("DataRegistro", "DATETIME")
    ],
    "TipoEndereco": [
        ("idTipoEndereco", "INT"),
        ("Descricao", "VARCHAR")
    ],
    "Endereco": [
        ("idEndereco", "INT"),
        ("EnderecoPadrao", "INT"),
        ("Logradouro", "VARCHAR"),
        ("Numero", "VARCHAR"),
        ("Complemento", "VARCHAR"),
        ("Bairro", "VARCHAR"),
        ("Cidade", "VARCHAR"),
        ("UF", "VARCHAR"),
        ("CEP", "VARCHAR"),
        ("TipoEndereco_idTipoEndereco", "INT"),
        ("Cliente_idCliente", "INT")
    ],
    "Telefone": [
        ("Numero", "VARCHAR"),
        ("Cliente_idCliente", "INT")
    ],
    "Status": [
        ("idStatus", "INT"),
        ("Descricao", "VARCHAR")
    ],
    "Pedido": [
        ("idPedido", "INT"),
        ("Status_idStatus", "INT"),
        ("DataPedido", "DATETIME"),
        ("ValorTotalPedido", "DECIMAL"),
        ("Cliente_idCliente", "INT")
    ],
    "Pedido_has_Produto": [
        ("idPedidoProduto", "INT"),
        ("Pedido_idPedido", "INT"),
        ("Produto_idProduto", "INT"),
        ("Quantidade", "DECIMAL"),
        ("PrecoUnitario", "DECIMAL")
    ]
}

quantidade = {
    "Categoria": 5,
    "Produto": 120,
    "TipoCliente": 3,
    "Cliente": 75,
    "TipoEndereco": 2,
    "Endereco": 90,
    "Telefone": 80,
    "Status": 4,
    "Pedido": 200,
    "Pedido_has_Produto": 350
}


"""
utils = Utils(tabelas_bd_vendas)

consulta = input("Escreva sua consulta: ")


print("\n\n",Utils.sqlParser(consulta),"\n\n")


try:
    express = utils.sqlParser(consulta)
    utils.validaConsulta(express)
    # os.system('cls' if os.name == 'nt' else 'clear')
    print("===============================")
    print("Consulta realizada com sucesso!")
    print("===============================")

    algebraRelacional = utils.converteAlgebra(express)
    #print("Algebra Relacional:\n", algebraRelacional)

    algebraRelacional = algebraRelacional.split(')(')

    algebraFatiada = []

    for expressao in algebraRelacional:
        expressao = expressao.replace('(','').replace(')','')
        algebraFatiada.append(expressao)

        index = 0
        for expressao in algebraFatiada:
            if ' X ' in expressao:
                algebraFatiada.pop(index)
                algebraFatiada.append(expressao.split(' '))
            index += 1


    algebraOtimizada = utils.otimiza(algebraFatiada, tabelas_bd_vendas)            
    #utils.gerarGrafo(algebraFatiada)
    utils.gerarGrafoOtimizado(algebraOtimizada, tabelas_bd_vendas)
    resultadoOtimiza4 = utils.otimiza_arvore_melhorada_4(algebraFatiada, tabelas_bd_vendas)
    print("Árvore de Consulta Melhorada 4:")
    print(resultadoOtimiza4)

  
except ValueError as erro:
    print("\n\n")
    print("Erro capturado:", erro)
"""
#teste
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Processador de Consultas SQL - Otimização de Árvores")
        self.root.geometry("800x600")

        # Título da aplicação
        title = tk.Label(root, text="Consultas SQL Otimizadas", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        # Caixa de texto para a consulta SQL
        self.text_sql = ScrolledText(root, height=8, width=80)
        self.text_sql.pack(pady=10)

        # Botão para iniciar o processamento
        self.button_process = tk.Button(root, text="Processar Consulta", command=self.processar, bg="#4CAF50", fg="white", font=("Arial", 12))
        self.button_process.pack(pady=10)

        # Área de saída
        self.output_area = ScrolledText(root, height=15, width=80, fg="#333333")
        self.output_area.pack(pady=10)

    def processar(self):
        consulta = self.text_sql.get("1.0", tk.END).strip()
        self.output_area.delete("1.0", tk.END)

        try:
            utils = Utils(tabelas_bd_vendas)
            express = utils.sqlParser(consulta)
            utils.validaConsulta(express)

            algebraRelacional = utils.converteAlgebra(express)
            algebraRelacional = algebraRelacional.split(')(')

            algebraFatiada = []
            for expressao in algebraRelacional:
                expressao = expressao.replace("(", "").replace(")", "")
                algebraFatiada.append(expressao)
                index = 0
                for expressao in algebraFatiada:
                    if ' X ' in expressao:
                        algebraFatiada.pop(index)
                        algebraFatiada.append(expressao.split(' '))
                    index += 1

            # Otimização da álgebra relacional
            algebraOtimizada = utils.otimiza(algebraFatiada, tabelas_bd_vendas)
            algebraOtimizadaPosicao = utils.otimizaPosicao(algebraOtimizada, quantidade)
            utils.gerarGrafoOtimizado(algebraOtimizadaPosicao, tabelas_bd_vendas)

            self.output_area.insert(tk.END, algebraOtimizadaPosicao)

        except ValueError as erro:
            self.output_area.insert(tk.END, f"Erro: {erro}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()



