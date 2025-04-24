from datetime import datetime

class Utils:

    def __init__(self, db):
        self.db = db
    
    @staticmethod
    def sqlParser(consulta):

        operadores = {'=', '>', '<', '<=', '>=', '<>', '(', ')', ',', '*', '.'}
        operadores_alfa = {'AND'}
        palavras_chaves = {'SELECT', 'FROM', 'WHERE', 'JOIN', 'ON'}

        tokens = []
        express_atual = ""
        i = 0
        n = len(consulta)

        while i < n:
            char = consulta[i]

            # 1) Literal DATETIME entre aspas: 'YYYY-MM-DD HH:MI:SS'
            #    comprimento total 21: 1 aspa + 19 chars + 1 aspa
            qt = consulta[i:i+21]
            if (len(qt) == 21
                and qt[0] == "'" and qt[-1] == "'"
                # verifica padrão interno YYYY-MM-DD HH:MI:SS
                and qt[1:5].isdigit() and qt[5] == '-' 
                and qt[6:8].isdigit() and qt[8] == '-' 
                and qt[9:11].isdigit() and qt[11] == ' ' 
                and qt[12:14].isdigit() and qt[14] == ':' 
                and qt[15:17].isdigit() and qt[17] == ':' 
                and qt[18:20].isdigit()):
                if express_atual:
                    tokens.append(express_atual)
                    express_atual = ""
                tokens.append(qt)
                i += 21
                continue

            # 2) String literal genérico entre aspas simples
            if char == "'":
                if express_atual:
                    tokens.append(express_atual)
                    express_atual = ""
                literal = char
                i += 1
                while i < n and consulta[i] != "'":
                    literal += consulta[i]
                    i += 1
                if i < n:
                    literal += consulta[i]
                    i += 1
                tokens.append(literal)
                continue

            # 3) Espaço em branco
            if char.isspace():
                if express_atual:
                    tokens.append(express_atual)
                    express_atual = ""
                i += 1
                continue

            # 4) Operador composto (2 caracteres)
            if i + 1 < n:
                duo = consulta[i:i+2]
                if duo in operadores or duo in operadores_alfa:
                    if express_atual:
                        tokens.append(express_atual)
                        express_atual = ""
                    tokens.append(duo)
                    i += 2
                    continue

            # 5a) Número (inteiro ou decimal, com sinal opcional)
            #    Aceita: 123   -45   3.14   -3.5   .5   10.
            if (char.isdigit()                                   # começa com dígito
                or (char == '-' and i + 1 < n and consulta[i+1].isdigit())  # número negativo
                or (char == '+' and i + 1 < n and consulta[i+1].isdigit())  # número positivo
                or (char == '.' and i + 1 < n and consulta[i+1].isdigit())):  # começa com ponto
                express_atual += char
                i += 1

                # dígitos antes do ponto
                while i < n and consulta[i].isdigit():
                    express_atual += consulta[i]
                    i += 1

                # ponto decimal opcional
                if i < n and consulta[i] == '.':
                    express_atual += '.'
                    i += 1
                    # dígitos depois do ponto (podem ser zero ou mais)
                    while i < n and consulta[i].isdigit():
                        express_atual += consulta[i]
                        i += 1

                tokens.append(express_atual)
                express_atual = ""
                continue


            # 5b) Operador simples ou parêntese
            if char in operadores:
                if express_atual:
                    tokens.append(express_atual)
                    express_atual = ""
                tokens.append(char)
                i += 1
                continue

            # 6) Acumula identificador/número/etc.
            express_atual += char
            i += 1

        # Se sobrou algo no buffer, adiciona
        if express_atual:
            tokens.append(express_atual)

        # Normaliza apenas palavras-chave e AND para uppercase
        final = []
        for tok in tokens:
            up = tok.upper()
            if up in palavras_chaves or up in operadores_alfa:
                final.append(up)
            else:
                final.append(tok)
        return final


    @staticmethod
    def verificaNum(s):
        try:
            float(s)
            return True
        except ValueError:
            return False



    @staticmethod
    def existePalavraDepois(lista, palavra, indice):
        for i in range(indice + 1, len(lista)):
            if lista[i] == palavra:
                return True
        return False
    
    @staticmethod
    def checaParenteses(express):
        pilha = []
        for e in express:
            if e == '(':
                pilha.append(e)
            elif e == ')':
                if not pilha:
                    return False
                pilha.pop()
        return not pilha
    
    def validaConsulta(self, express):

        if not self.checaParenteses(express):
            raise ValueError('Parênteses não balanceados na consulta')

        i = 0
        tabelas = []
        operadores = {'=', '>', '<', '<=', '>=', '<>'}
        composto = False
        idx_from = express.index('FROM')

        if express[i] != 'SELECT':
            raise ValueError('Primeiro operador deve ser SELECT')
            
        while i < len(express)-1:

            if express[i] == 'SELECT':
                colunas_vistas = set()
                i+=1
                if express[i+1] == '.':
                    composto = True                   
                while express[i] != 'FROM':
                    if i == 1 and express[i] == ',':
                        raise ValueError('Após o Select, deve ser digitado um nome válido de uma coluna')
                    if express[i] != ',':
                        if composto:
                            nome_col = f"{express[i]}.{express[i+2]}"
                            if nome_col in colunas_vistas:
                                raise ValueError(f"Coluna repetida no SELECT: {nome_col}")
                            colunas_vistas.add(nome_col)
                            if self.existePalavraDepois(express,express[i],idx_from):
                                if self.verificaTabela(express[i]):
                                    i+=1
                                    if express[i] == '.':
                                        if self.verificaColuna(express[i-1],express[i+1]):
                                            i+=2
                                        else:
                                            raise ValueError(f"Coluna {express[i+1]} inexistente na tabela {express[i-1]}")
                                    else:
                                        raise ValueError("Formato não identificado, formato correto: 'TABELA.COLUNA'")
                                else:
                                    raise ValueError(f"Tabela não existente no banco de dados: {express[i]}")
                            else:
                                raise ValueError(f"Tabela não declarada na expressão: {express[i]}")
                        else:
                            nome_col = express[i]
                            if nome_col in colunas_vistas:
                                raise ValueError(f"Coluna repetida no SELECT: {nome_col}")
                            colunas_vistas.add(nome_col)
                            if self.verificaColuna(express[idx_from+1], express[i]):
                                i+=1
                            else:
                                raise ValueError(f"Coluna {express[i]} inexistente em {express[idx_from+1]}")
                    elif express[i] == ',' and express[i-1] ==',':
                        raise ValueError('Erro ao colocar 2 vírgulas consecutivas após o Select')
                    # Perguntar pro professor se a coluna pode ter nome com caractere especial
                    elif express[i] == ',':
                        i+=1



            if express[i] == 'FROM':
                i+=1
                if not self.verificaTabela(express[i]):
                    raise ValueError('Após o From, deve ser digitado um nome válido de uma tabela')
                
                if len(express)-1> i:
                    tabelas.append(express[i])
            
            elif i < len(express)-1:
                while True:
                    if express[i] == 'JOIN':
                        i+=1
                        if not self.verificaTabela(express[i]):
                            raise ValueError('Após o Join, deve ser digitado um nome válido de uma tabela')
                        tabelas.append(express[i])
                        i+=1

                        if express[i] == 'ON':
                            i+=1
                            if self.verificaTabelaColuna(express,i,tabelas):
                                i+=3
                                if express[i] in operadores:
                                    i+=1
                                    if self.verificaTabelaColuna(express,i,tabelas):
                                        i+=2
                                        if i >= len(express)-1:
                                            break
                                        i+=1
                                    else:
                                        raise ValueError("Formato não identificado, formato correto: 'TABELA.COLUNA'")
                                else:
                                    raise ValueError("Operador esperado")
                            else:
                                raise ValueError("Formato não identificado, formato correto: 'TABELA.COLUNA'")
                        else:
                            raise ValueError('Após digitar a ultima tabela do Join, deve-se digitar ON')
                    else:
                        break
                if express[i] == 'WHERE':
                    i+=1
                    while True:
                        if express[i] == 'AND':
                            if express[i-1] == 'WHERE':
                                raise ValueError("Após WHERE deve-se colocar uma condição")
                            if i < len(express)-1:
                                i+=1
                            else:
                                raise ValueError("Após AND deve-se colocar uma condição")
                        while express[i] == '(':          # permite '(' repetidos
                            i += 1

                        if len(tabelas) > 1:
                            if self.verificaTabelaColuna(express, i, tabelas):
                                i+=2
                                tipo = self.verificaTipo(express[i-2],express[i])
                                i+=1
                                if express[i] in operadores:
                                    i+=1
                                    if i < len(express)-1 and express[i+1] != 'AND':
                                        if self.verificaTabelaColuna(express,i,tabelas):
                                            i+=2
                                            tipo2 = self.verificaTipo(express[i-2],express[i])
                                            if tipo == tipo2:
                                                while i < len(express) -1 and express[i+1] == ')':
                                                    i += 1
                                                if i < len(express)-1:
                                                    if express[i+1] == 'AND':
                                                        i+=1
                                                        continue
                                                    elif i >= len(express)-1 or express[i+1] == ')':
                                                        break
                                                    else:
                                                        raise ValueError("Finalização ou AND esperada")
                                                else:
                                                    break
                                            else:
                                                raise ValueError("Formatos incompatíveis no WHERE")
                                        else:
                                            tipo2 = self.verificaNum(express[i])
                                            if (tipo2 and tipo == 'num') or (not tipo2 and tipo == 'str') or (tipo == 'data' and (False if tipo2 else self.verificaDatetime(express[i]))):
                                                while i < len(express) -1 and express[i+1] == ')':
                                                    i += 1
                                                if i < len(express)-1:
                                                    if express[i+1] == 'AND':
                                                        i+=1
                                                        continue
                                                    elif i >= len(express)-1 or express[i+1] == ')':
                                                        break
                                                    else:
                                                        raise ValueError("Finalização ou AND esperada")
                                                else:
                                                    break
                                            else:
                                                raise ValueError("Formatos incompatíveis no WHERE")
                                    else:
                                        tipo2 = self.verificaNum(express[i])
                                        if (tipo2 and tipo == 'num') or (not tipo2 and tipo == 'str') or (tipo == 'data' and (False if tipo2 else self.verificaDatetime(express[i]))):
                                            while i < len(express) -1 and express[i+1] == ')':
                                                i += 1
                                            if i < len(express)-1:
                                                if express[i+1] == 'AND':
                                                    i+=1
                                                    continue
                                                elif i >= len(express)-1 or express[i+1] == ')':
                                                    break
                                                else:
                                                    raise ValueError("Finalização ou AND esperada")
                                            else:
                                                break
                                        else:
                                            raise ValueError("Formatos incompatíveis no WHERE")

                                else:
                                    raise ValueError("Operador esperado")
                            else:
                                tipo = self.verificaNum(express[i])
                                i+=1
                                if express[i] in operadores:
                                    i+=1
                                    if i < len(express)-1 and express[i+1] != 'AND':
                                        if self.verificaTabelaColuna(express,i,tabelas):
                                            i+=2
                                            tipo2 = self.verificaTipo(express[i-2],express[i])
                                            if (tipo and tipo2 == 'num') or (not tipo and tipo2 == 'str') or (tipo2 == 'data' and (False if tipo else self.verificaDatetime(express[i-4]))):
                                                while i < len(express) -1 and express[i+1] == ')':
                                                    i += 1
                                                if i < len(express)-1:
                                                    if express[i+1] == 'AND':
                                                        i+=1
                                                        continue
                                                    elif i >= len(express)-1 or express[i+1] == ')':
                                                        break
                                                    else:
                                                        raise ValueError("Finalização ou AND esperada")
                                                else:
                                                    break
                                            else:
                                                raise ValueError("Formatos incompatíveis no WHERE")
                                        else:
                                            raise ValueError("Formatos incompatíveis no WHERE")
                                    else:
                                        raise ValueError("Formatos incompatíveis no WHERE")
                                else:
                                    raise ValueError("Operador esperado")
                                
                        else:
                            if self.verificaColuna(tabelas[0],express[i]):
                                tipo = self.verificaTipo(tabelas[0],express[i])
                                i+=1
                                if express[i] in operadores:
                                    i+=1
                                    if self.verificaColuna(tabelas[0],express[i]):
                                        tipo2 = self.verificaTipo(tabelas[0],express[i])
                                        if tipo == tipo2:
                                            while i < len(express) -1 and express[i+1] == ')':
                                                i += 1
                                            if i < len(express)-1:
                                                if express[i+1] == 'AND':
                                                    i+=1
                                                    continue
                                                elif i >= len(express)-1 or express[i+1] == ')':
                                                    break
                                                else:
                                                    raise ValueError("Finalização ou AND esperada")
                                            else:
                                                break
                                        else:
                                            raise ValueError("Formatos incompatíveis no WHERE")
                                    else:
                                        tipo2 = self.verificaNum(express[i])
                                        if (tipo2 and tipo == 'num') or (not tipo2 and tipo == 'str') or (tipo == 'data' and (False if tipo2 else self.verificaDatetime(express[i]))):
                                            while i < len(express) -1 and express[i+1] == ')':
                                                i += 1
                                            if i < len(express)-1:
                                                if express[i+1] == 'AND':
                                                    i+=1
                                                    continue
                                                elif i >= len(express)-1 or express[i+1] == ')':
                                                    break
                                                else:
                                                    raise ValueError("Finalização ou AND esperada")
                                            else:
                                                break
                                        else:
                                            raise ValueError("Formatos incompatíveis no WHERE")
                                else:
                                    raise ValueError("Operador esperado")
                            else:
                                tipo = self.verificaNum(express[i])
                                i+=1
                                if express[i] in operadores:
                                    i+=1
                                    if self.verificaColuna(tabelas[0],express[i]):
                                        tipo2 = self.verificaTipo(tabelas[0],express[i])

                                        if (tipo and tipo2 == 'num') or (not tipo and tipo2 == 'str') or (tipo2 == 'data' and (False if tipo else self.verificaDatetime(express[i-2]))):
                                            while i < len(express) -1 and express[i+1] == ')':
                                                i += 1
                                            if i < len(express)-1:
                                                if express[i+1] == 'AND':
                                                    i+=1
                                                    continue
                                                elif i >= len(express)-1 or express[i+1] == ')':
                                                    break
                                                else:
                                                    raise ValueError("Finalização ou AND esperada")
                                            else:
                                                break
                                        else:
                                            raise ValueError("Formatos incompatíveis no WHERE")
                                    else:
                                        raise ValueError(f"Coluna {express[i]} não existe na tabela {tabelas[0]}")
                                else:
                                    raise ValueError("Operador esperado")
                                
            i+=1

                    

                    

                        

                    

            
        return True 

    @staticmethod
    def converteAlgebra(express):
        express[:] = [elem for elem in express if elem not in ('(', ')')]
        algb = ''
        i = 0
        if express[i] == 'SELECT':
            idx = express.index("FROM")
            antes = express[:idx]
            resultado = "".join(antes)
            algb += f'π({resultado})'
            i = idx
        if express[i] == 'FROM':
            i+=1
            tab = express[i]
            algb += f'('
            if i < len(express)-1:
                i+=1
                if express[i] == 'JOIN':
                    algb += Utils.verficaJoin(express, i)
                elif express[i] == 'WHERE':
                    algb += Utils.verificaWhere(express,i)
            algb += f'{tab})'
                
                
            
            
        return algb
    
    def verficaJoin(self,express, i, comp = ''):
        if self.verificaTabela(express[i-1]):
            aux = f'{express[i-1]} X {express[i+1]}'
            i+=3
            comp = f'Sigma({''.join(express[i:i+8])})'
            comp = f'{comp}({aux})'
            i+=8  
        else:
            aux = f'{comp} X {express[i+1]}'
            i+=3
            comp = f'Sigma({''.join(express[i:i+8])})({aux})'
            i+=8
        if i < len(express)-1:
            if express[i] == 'JOIN':
                i, comp = self.verificaJoin(express, i, comp)
            elif express[i] == 'WHERE':
                i, comp = self.verificaWhere()
            return i, comp
        else:
            return i, comp
        
    def verificaWhere(self,express, i, comp = ''):
        if express[i] == 'WHERE':
            aux = 'Sigma('
            comp = f'{Utils.verificaWhere(express,i,aux)})({comp})'
        else:
            i+=1
            if i < len(express)-1:
                if self.verificaTabela(express[i]):
                    if express[i+1] == '.':
                        i+=1
                        aux = f'{express[i-1]+express[i]+express[i+1]+express[i+2]}'
                        i+=3
                        if self.verificaTabela(express[i]):
                            i+=1
                            aux = f'{aux+express[i-1]+express[i]+express[i+1]} '
                        else:
                            aux = f'{aux+express[i]} '
                    else:
                        i+=1
                        aux = f'{express[i-1] + express[i]+ express[i+1]} '         
                else:
                    i+=1
                    aux = f'{express[i-1] + express[i]+ express[i+1]}'
                    i+=2
                    if i < len(express)-1:
                        
                        
                
                
        
        return
        
    
    def verificaColuna(self,tabela,coluna):
        if coluna == '*':
            return True
        elif coluna in dict(self.db[tabela]):
            return True
        else:
            return False
        
    

    def verificaTabela(self,tabela):
        if tabela in self.db:
            return True
        else:
            return False
        
    
    def verificaTabelaColuna(self,express,i,tabelas):
        if express[i+1] == '.':
            if express[i] not in tabelas:
                raise ValueError("Tabela não mencionada anteriormente")
            if self.verificaColuna(express[i],express[i+2]):
                return True
            else:
                return False
        else:
            return False
    
    def verificaTipo(self,tabela,coluna):
        colunas = dict(self.db[tabela])
        tipo = colunas[coluna]
        if tipo == 'DECIMAL' or tipo == 'INT':
            return 'num'
        elif tipo == 'VARCHAR':
            return 'str'
        elif tipo == 'DATETIME':
            return 'data'
        else:
            raise ValueError(f"Tipo não identificado: {tipo}")
    

    def verificaDatetime(self,s):
        if len(s) >= 2 and s[0] == "'" and s[-1] == "'":
            s = s[1:-1]
        try:
            datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
            return True
        except ValueError:
            return False
    
    


