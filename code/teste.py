tokens = ["col1", ",", "col2", "FROM", "tabela", "WHERE", "id=1"]

# Método 1: usando index() + slicing

idx = tokens.index("FROM")        # 1) encontra o índice de "FROM"
antes = tokens[:idx]              # 2) fatia até (mas não incluindo) "FROM"
resultado = "".join(antes)       # 3) concatena com espaço
print("Usando index+slicing:", resultado)