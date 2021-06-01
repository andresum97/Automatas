class Process:
    def __init__(self, prod):
        self.productions = prod
        self.newProd = {}
        self.tokens = {}
        self.noterminals = []
        self.firsts = {}
        self.results = []
        self.contTokens = 0
        self.getTokens()
        self.getNoTerminals()
        print("Nuevas producciones",self.newProd)
        print("Nuevos tokens",self.tokens)
        print("No terminales",self.noterminals)


    #Metodo para guardar los tokens y transformar los strings de producciones
    #en tokens
    def getTokens(self):
        for key,value in self.productions.items():
            temp = []
            for element in value:
                if element[1] == 'tok':
                    val = element[0]
                    tempTok = 'ident'+str(self.contTokens)
                    temp.append((tempTok,'ident'))
                    self.tokens[tempTok] = val
                    self.contTokens += 1
                else:
                    temp.append(element)

            self.newProd[key] = temp

    
    def getNoTerminals(self):
        self.noterminals = [key for key in self.productions.keys()]