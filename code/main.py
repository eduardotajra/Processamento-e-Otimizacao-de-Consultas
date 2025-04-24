from Utils import Utils
import os

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
    print("Algebra Linear:\n",utils.converteAlgebra(express))
    
except ValueError as erro:
    print("\n\n")
    print("Erro capturado:", erro)

