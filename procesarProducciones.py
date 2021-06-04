from arbolSintactico import Tree
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
        self.createTree()
        # print("Nuevas producciones",self.newProd)
        print("Nuevos tokens",self.tokens)
        print("No terminales",self.noterminals)
        # res = self.first([('\t', 'white'), ('(', 'p_open'), ('number', 'ident'), ('\t', 'white'), ('|', 'union'), ('decnumber', 'ident'), (')', 'p_close'), ('(.result = float(self.lastvalue).)', 's_action'), ('\t', 'white'), ('(.return result.)', 's_action'), ('\t', 'white'), ('.', 'p_end')])
        # print("First primero",res)

    #Metodo que obtiene los no terminales, los valores de los tokens y los first de cada produccion
    def processProductions(self):
        self.getTokens()
        self.getNoTerminals()
        print("Solo values",self.newProdValues)

        for key in reversed(self.productions.keys()):
            # print("Esto es first",self.firsts, "Llave que estoy viendo ",key)
            self.firsts[key] = self.first(self.newProdValues[key])

        print("Dictoario de first",self.firsts)


    def createTree(self):
        program = ''' 
class Parser():
    def __init__(self, tokens):
        self.tokens = tokens
        self.actualToken = None
        self.posToken = 0
        self.lookAheadToken = self.tokens[self.posToken]
        self.next()
        self.lastToken = None
        self.principal()

    def next(self):
        if self.posToken - 1 < 0:
            self.lastToken == None
        else:
            self.lastToken = self.tokens[self.posToken - 1][0]
        
        if self.lookAheadToken == None:
            self.actualToken = None
        else:
            self.actualToken = self.lookAheadToken[1]
        
        self.posToken += 1

        if self.posToken >= len(self.tokens):
            self.lookAheadToken = None
        else:
            self.lookAheadToken = self.tokens[self.posToken]

    def principal(self):
        '''
        for key, value in self.newProdValues.items():
            print("Ingreso este item ",key)
            tree = Tree(value,self.firsts)

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
                    if element[1]!='white' and element[1]!='p_end':   
                        temp.append(element)
                    if isValue and element[1]!='white' and element[1]!='p_end':
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