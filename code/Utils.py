
class Utils:

    def __init__(self, nome):
        self.nome = nome
        
    def sqlParser(consulta):

        operadores = {'=', '>', '<', '<=', '>=', '<>', 'AND', '(', ')', ',', '*','.'}
        palavrasChaves = {'SELECT', 'FROM', 'WHERE', 'JOIN', 'ON'}

        express = []
        express_atual = ""
        i = 0

        while i < len(consulta):
            char = consulta[i]
            
            # Espaço vazio
            if char.isspace():
                if express_atual:
                    express.append(express_atual)
                    express_atual = ""
                i += 1
                continue

            # Operador composto (2 caracteres)
            if i + 1 < len(consulta):
                candidate = consulta[i:i+2]
                if candidate in operadores:
                    if express_atual:
                        express.append(express_atual)
                        express_atual = ""
                    express.append(candidate)
                    i += 2
                    continue

            # Operador Simples (só 1)
            if char in operadores:
                if express_atual:
                    express.append(express_atual)
                    express_atual = ""
                express.append(char)
                i += 1
                continue

            # Acumula
            express_atual += char
            i += 1

        # Se sobrar alguma expressão qeu não acabou, adiciona ela
        if express_atual:
            express.append(express_atual)

        # Se a expressão está em palavrasChaves, coloca ela maiuscula
        final_express = []
        for token in express:
            if token.upper() in palavrasChaves:
                final_express.append(token.upper())
            else:
                final_express.append(token)

        return final_express
    
    def validaConsulta(express):

        i = 0

        if express[i] != 'SELECT':
            raise ValueError('Primeiro operador deve ser SELECT')
            
        while i < len(express):
            
            if express[i] == 'SELECT':
                i+=1
                while express[i] != 'FROM':
                    if i == 1 and express[i] == ',':
                        raise ValueError('Após o Select, deve ser digitado um nome válido de uma coluna')
                    if express[i] != ',':
                        Utils.verificaColuna(express[i])
                    # Perguntar pro professor se a coluna pode ter nome com caractere especial
                    i +=1

            if express[i] == 'FROM':
                i+=1
                if not Utils.verificaTabela(express[i]):
                    raise ValueError('Após o From, deve ser digitado um nome válido de uma tabela')

            if express[i] == 'JOIN':
                i+=1
                if not Utils.verificaTabela(express[i]):
                    raise ValueError('Após o Join, deve ser digitado um nome válido de uma tabela')
            

            i+=1

                    

                    

                        

                    

            
        return True 

    def converteAlgebra(express):
        # Transforma em algebra relacional
        return

    @staticmethod
    def verificaColuna(express):
        # Função para verificar se contém coluna no banco de dados
        return
    
    @staticmethod
    def verificaTabela(express):
        # Função para verificar se contém a tabela no banco de dados
        return
    
    


