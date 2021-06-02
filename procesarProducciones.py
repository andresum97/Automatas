class Process:
    def __init__(self, prod):
        self.productions = prod
        self.newProd = {}
        self.newProdValues = {}
        self.tokens = {}
        self.noterminals = []
        self.firsts = {}
        self.results = []
        self.contTokens = 0
        self.processProductions()
        # print("Nuevas producciones",self.newProd)
        print("Nuevos tokens",self.tokens)
        print("No terminales",self.noterminals)
        # res = self.first([('\t', 'white'), ('(', 'p_open'), ('number', 'ident'), ('\t', 'white'), ('|', 'union'), ('decnumber', 'ident'), (')', 'p_close'), ('(.result = float(self.lastvalue).)', 's_action'), ('\t', 'white'), ('(.return result.)', 's_action'), ('\t', 'white'), ('.', 'p_end')])
        # print("First primero",res)


    def processProductions(self):
        self.getTokens()
        self.getNoTerminals()
        print("Solo values",self.newProdValues)

        for key in reversed(self.productions.keys()):
            print("Esto es first",self.firsts, "Llave que estoy viendo ",key)
            self.firsts[key] = self.first(self.newProdValues[key])

        print("Dictoario de first",self.firsts)


    #Metodo para guardar los tokens y transformar los strings de producciones
    #en tokens
    def getTokens(self):
        for key,value in self.productions.items():
            temp = []
            tempValues = []
            isValue = False
            for element in value:
                if element[1] == 'tok' and isValue:
                    val = element[0]
                    tempTok = 'ident'+str(self.contTokens)
                    temp.append((tempTok,'ident'))
                    tempValues.append((tempTok,'ident'))
                    self.tokens[val] = tempTok
                    self.contTokens += 1
                elif element[1] == 'eq':
                    print("Entro a este if")
                    isValue = True
                else:
                    if element[1]!='white':   
                        temp.append(element)
                    if isValue and element[1]!='white':
                        tempValues.append(element)

            self.newProd[key] = temp
            self.newProdValues[key] = tempValues
    
    def getNoTerminals(self):
        self.noterminals = [key for key in self.productions.keys()]

    
    def first(self, production):
        result = []
        beginParenthesis = False
        beginBracket = False
        flag = False

        for element in production:
            val, type = element #tupla
            if type == 'p_close':
                beginParenthesis = False
            elif type == 'sq_close':
                beginBracket = False

            if beginParenthesis:
                if flag:
                    if type == 'union':
                        flag = False
                else:
                    if type == 'ident' and val in self.noterminals:
                        flag = True
                        result += self.firsts[val]
                    elif type == 'ident' and val not in self.noterminals:
                        flag = True
                        result.append(val)
                    elif type == 'tok':
                        flag = True
                        result.append(val.replace('"',''))
            elif beginBracket:
                if type == 'ident' and val in self.noterminals:
                    result += self.firsts[val]
                elif type == 'ident' and val not in self.noterminals:
                    result.append(val)
                elif type == 'tok':
                    result.append(val.replace('"',''))
            elif type == 'ident' and val in self.noterminals:
                result += self.firsts[val]
                break
            elif type == 'ident' and val not in self.noterminals:
                result.append(val)
                break
            elif type == 'tok':
                result.append(val.replace('"',''))
                break

            if type == 'p_open':
                beginParenthesis = True
            elif type == 'sq_open':
                beginBracket = True

        return result