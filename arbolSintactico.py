#Primero obtener las cadenas de las producciones ya obtenidas de las producciones
# osea el tipo que ya tengo del proyecto 2.
# Pensar como obtener el parrafo de producciones
import re

#TODO ya realzaste la operacion de concat y or, faltan las demas!!!

class Tree():
    def __init__(self, r, f):
        # print("Esto entre en r", r)
        # print("Esto en f",f)
        self.expression =  self.add_concat(r) # Regular expression
        # print("Lista con concatenacion",self.expression)
        self.first = f
        self.values = []
        self.operators = []
        self.root = None
        self.childs = []
        self.tabs = 0
        self.process_expression()

    def getTree(self):
        return self.root[0]

    #Metodo para agregar la concatenacion
    def add_concat(self,expression):
        new_word = []
        operators = ['{','}','(',')','[',']','|']
        cont = 0

        for cont in range(len(expression)):
            if cont + 1 >= len(expression):
                new_word.append(expression[-1])
                break

            new_word.append(expression[cont])

            if expression[cont][0] == "}" and expression[cont+1][0] in '({[]}':
                new_word.append(('.','concat'))
            elif expression[cont][0] not in operators and expression[cont+1][0] not in operators:
                new_word.append(('.','concat'))
            elif expression[cont][0] not in operators and expression[cont+1][0] in '([':
                new_word.append(('.','concat'))
            elif expression[cont][0] == ')' and expression[cont+1][0] not in operators:
                new_word.append(('.','concat'))
            

        return new_word


    def child_first(self,val1, val2, op):
        if op == 'concat':
            if val1[1] == 'ident':
                if val1[0] in self.first.keys():
                    return self.first[val1[0]]
                else:
                    return [val1[0]]
            elif val2[1] == 'ident':
                if val2[0] in self.first.keys():
                    return self.first[val2[0]]
                else:
                    return [val2[0]]
            else:
                return []
        elif op == 'union':
            if val1[0] in self.first.keys():
                first1 = self.first[val1[0]]
            else:
                first1 = [val1[0]]
            
            if val2[0] in self.first.keys():
                first2 = self.first[val2[0]]
            else:
                first2 = [val2[0]]
            
            return first1 + first2

    def op_concat(self, val1, val2):
        first = []
        if (isinstance(val1, tuple) and isinstance(val1[0],list)) and (isinstance(val2, tuple) and isinstance(val2[0],list)):
            parent = val1[0] + val2[0]
            first = val1[1]
            return (parent, first)

        elif not (isinstance(val1, tuple) and isinstance(val1[0],list)) and not (isinstance(val2, tuple) and isinstance(val2[0],list)):
            parent = []
            first = self.child_first(val1,val2,'concat')
            
            #First child
            if val1[1] == 's_action':
                parent += ['\t'*self.tabs + val1[0][2:-2]]
            elif val1[1] == 'ident' and val1[0] in self.first.keys():
                parent += ['\t'*self.tabs + 'if self.actualToken in '+repr(self.first[val1[0]])+':']
                parent += ['\t'*self.tabs + '\tself.'+val1[0]+'()']
                self.tabs += 1
            elif val1[1] == 'ident' and val1[0] not in self.first.keys():
                parent += ['\t'* self.tabs + 'if self.actualToken == "'+val1[0]+'":']
                parent += ['\t'* self.tabs + '\tself.coincidir("'+val1[0]+'")']
                self.tabs += 1

            #Second child
            if val2[1] == 's_action':
                parent += ['\t'*self.tabs + val2[0][2:-2]]
            elif val2[1] == 'ident' and val2[0] in self.first.keys():
                parent += ['\t'*self.tabs + 'self.'+val2[0]+'()']
                # self.tabs += 1
            elif val2[1] == 'ident' and val2[0] not in self.first.keys():
                parent += ['\t'* self.tabs + 'if self.actualToken == "'+val2[0]+'":']
                parent += ['\t'* self.tabs + '\tself.coincidir("'+val2[0]+'")']
                self.tabs += 1
            elif val2[1] == 'attr':
                pos = parent[-1][:-2].rfind('\t') #TODO Revisa esto
                parent[-1] = parent[-1][:-2][:pos+1] + val2[0][1:-1] + ' = ' + parent[-1][:-2][pos+1:]+'('+val2[0][1:-1]+')'

            return (parent, first)
        
        elif (isinstance(val1,tuple) and isinstance(val1[0],list)) and not (isinstance(val2,tuple) and isinstance(val2[0],list)):
            parent = val1[0]
            first = val1[1]

            #Second Child
            if val2[1] == 's_action':
                parent += ['\t'*self.tabs+val2[0][2:-2]]
            elif val2[1] == 'ident' and val2[0] in self.first.keys():
                parent += ['\t'*self.tabs+'self.'+val2[0]+'()']
            elif val2[1] == 'ident' and val2[0] not in self.first.keys():
                parent += ['\t'*self.tabs+'if self.actualToken == "'+val2[0]+'":']
                parent += ['\t'* self.tabs + '\tself.coincidir("'+val2[0]+'")']
                self.tabs += 1
            elif val2[1] == 'attr':
                pos = parent[-1][:-2].rfind('\t') #TODO Revisa esto
                parent[-1] = parent[-1][:-2][:pos+1] + val2[0][1:-1] + ' = ' + parent[-1][:-2][pos+1:]+'('+val2[0][1:-1]+')'

            return (parent, first)


        elif not (isinstance(val1, tuple) and isinstance(val1[0],list)) and (isinstance(val2, tuple) and isinstance(val2[0],list)):
            parent = val2[0]

            if val1[1] == 's_action':
                parent = ['\t'*self.tabs+val1[0][2:-2]] + parent
                first = val2[1]
            elif val1[1] == 'ident' and val1[0] in self.first.keys():
                parent = ['\t'*self.tabs + 'if self.actualToken in '+repr(self.first[val1[0]])+':']
                parent += ['\t' * self.tabs + '\tself.'+val1[0]+'()']+val2[0]
                self.tabs += 1
                #Calcular first
                if val1[0] in self.first.keys():
                   first = self.first[val1[0]]
                else:
                   first= [val1[0]]
            elif val1[1] == 'ident' and val1[0] not in self.first.keys():
                parent = ['\t'*self.tabs+'if self.actualToken == "'+val1[0]+'":']
                parent += ['\t'*self.tabs + '\tself.coincidir("'+val1[0]+'")']+val2[0]
                first = [val1[0]]
                self.tabs += 1
            
            return (parent, first)


    def op_union(self,val1,val2):
        
        if (isinstance(val1, tuple) and isinstance(val1[0],list)) and (isinstance(val2, tuple) and isinstance(val2[0],list)):
            self.tabs -= 1
            parent = val1[0] + ['else:'] + val2[0]
            self.tabs -= 1
            return (parent, val1[1]+val2[1])

        elif not (isinstance(val1, tuple) and isinstance(val1[0],list)) and not (isinstance(val2, tuple) and isinstance(val2[0],list)):
            parent = []
            first = self.child_first(val1,val2,'union')

            #First child
            if val1[1] == 'ident' and val1[0] in self.first.keys():
                parent += ['\t'*self.tabs + 'if self.actualToken in '+repr(self.first[val1[0]])]
                parent += ['\t'*self.tabs + '\tself.'+val2[0]+'()']
            elif val1[1] == 'ident' and val1[0] not in self.first.keys():
                parent += ['\t'*self.tabs + 'if self.actualToken == "'+val1[0]+'":']
                parent += ['\t'*self.tabs + '\tself.coincidir("'+val1[0]+'")']

            #Second child
            if val2[1] == 'ident' and val2[0] in self.first.keys():
                parent += ['\t'*self.tabs + 'elif self.actualToken in '+repr(self.first[val2[0]])]
                parent += ['\t'*self.tabs + '\tself.'+val2[0]+'()']
            elif val2[1] == 'ident' and val2[0] not in self.first.keys():
                parent += ['\t'*self.tabs + 'elif self.actualToken == "'+val2[0]+'":']
                parent += ['\t'*self.tabs + '\tself.coincidir("'+val2[0]+'")']

            self.tabs -= 1
            
            return (parent, first)
        
        elif (isinstance(val1,tuple) and isinstance(val1[0],list)) and not (isinstance(val2,tuple) and isinstance(val2[0],list)):
            parent = val1[0]+['else:']
            first = val1[1]

            #Second child
            if val2[1] == 'ident' and val2[0] in self.first.keys():
                parent += ['\t'*self.tabs + 'if self.actualToken in '+repr(self.first[val2[0]])]
                parent += ['\t'*self.tabs + '\tself."'+val2[0]+'()']
                first += self.first[val2[0]]
            elif val2[1] == 'ident' and val2[0] not in self.first.keys():
                parent += ['\t'*self.tabs+'if self.actualToken == "'+val2[0]+'":']
                parent += ['\t'*self.tabs + '\tself.coincidir("'+val2[0]+'")']
                first += [val2[0]]

            self.tabs -= 1
            return (parent, first)

        elif not (isinstance(val1, tuple) and isinstance(val1[0],list)) and (isinstance(val2, tuple) and isinstance(val2[0],list)):
            parent = []
            first = val2[1]
            self.tabs -= 1

            #first child
            if val1[1] == 'ident' and val1[0] in self.first.keys():
                parent += ['\t'*self.tabs + 'if self.actualToken in '+repr(self.first[val1[0]])]
                parent += ['\t'*self.tabs + '\tself.'+val2[0]+'()']
                first += self.first[val1[0]]
            elif val1[1] == 'ident' and val1[0] not in self.first.keys():
                parent += ['\t' * self.tabs + 'if self.actualToken == "'+val1[0]+'":']
                parent += ['\t' * self.tabs + '\tself.coincidir("'+val1[0]+'")']
                first += [val1[0]]

            parent += ['else:']+ ['\t'+i for i in val2[0]]

            self.tabs -= 1
            return (parent, first)

    def op_kleene(self,val1,val2):
        parent = []
        first = []

        if isinstance(val1,tuple) and isinstance(val1[0],list):
            parent = val1[0]
        else:
            self.tabs -= 1
            if val1[1] == 's_action':
                parent = ['\t'*self.tabs+val1[0][2:-2]]
            elif val1[1] == 'ident' and val1[0] in self.first.keys():
                parent += ['\t'*self.tabs + 'if self.actualToken in '+repr(self.first[val1[0]])+':']
                parent = ['\t'*self.tabs + '\tself.'+val1[0]+'()']
                self.tabs += 1
            elif val1[1] == 'ident' and val1[0] not in self.first.keys():
                parent += ['\t'*self.tabs+'if self.actualToken == "'+val1[0]+'":']
                parent = ['\t'*self.tabs+'\tself.coincidir("'+val1[0]+'")']
            self.tabs += 1

        if isinstance(val2, tuple) and isinstance(val2[0],list):
            self.tabs -= 2
            parent += ['\t'*self.tabs+'while self.actualToken in '+repr(val2[1])+':']+['\t'+i for i in val2[0]]
            self.tabs += 1
        else:
            parent += ['\t'*self.tabs+'while self.actualToken in ["'+val2[0]+'"]:']+['\t'*self.tabs+'\tself.coincidir("'+val2[0]+'")']
        
        return(parent, first)

    def op_kleeneClose(self, val1, val2):
        first = []
        self.tabs -= 1

        #Second child
        if isinstance(val2,tuple) and isinstance(val2[0],list):
            print("val1",val1)
            print("val2",val2)
            parent = val1[0]+val2[0]
        else:
            parent = val1[0]
            if val2[1] == 's_action':
                parent += ['\t'*self.tabs+val2[0][2:-2]]
            elif val2[1] == 'ident' and val2[0] in self.first.keys():
                parent += ['\t'*self.tabs+'if self.actualToken in '+repr(self.first[val2[0]])]
                parent += ['\t'*self.tabs+'\tself.'+val2[0]+'()']
            elif val2[1] == 'ident' and val2[0] not in self.first.keys():
                parent += ['\t'*self.tabs+'if self.actualToken == "'+val2[0]+'":']
                parent += ['\t'*self.tabs+'\tself.coincidir("'+val2[0]+'")']

        return (parent, first)

    def op_bracket(self,val1,val2):
        parent = []
        first = []

        if isinstance(val1, tuple) and isinstance(val1[0],list):
            parent = val1[0]
        else:
            self.tabs -= 1
            if val1[1] == 's_action':
                parent = ['\t'*self.tabs+val1[2:-2]]
            elif val1[1] == 'ident' and val1[0] in self.first.keys():
                parent += ['\t'*self.tabs+'if self.actualToken in '+repr(self.first[val1[0]])+':']
                parent += ['\t'*self.tabs + '\tself.'+val1[0]+'()']
                self.tabs += 1
            elif val1[1] == 'ident' and val1[0] not in self.first.keys():
                parent += ['\t'*self.tabs+'if self.actualToken == "'+val1[0]+'":']
                parent += ['\t'*self.tabs+'\tself.coincidir("'+val1[0]+'")']

        if isinstance(val2,tuple) and isinstance(val2[0],list):
            self.tabs -= 1
            parent += ['\t'*self.tabs+'if self.actualToken in '+repr(val2[1])+':'] + ['\t' + i for i in val2[0]]
        else:
            parent += ['\t'*self.tabs+'if self.actualToken in ["'+val2[0]+'"]:'] + ['\t'*self.tabs+'\tself.coincidir("'+val2[0]+'")']

        return (parent, first)

    def op_bracketClose(self,val1,val2):
        self.tabs -= 1
        first = []

        #Second child
        if isinstance(val2, tuple) and isinstance(val2[0],list):
            parent = val1[0]+val2[0]
        else:
            parent = val1[0]
            if val2[1] == 'ident' and val2[0] in self.first.keys():
                parent += ['\t'*self.tabs + val2[0][2:-2]]
            elif val2[1] == 'ident' and val2[0] in self.first.keys():
                parent += ['\t'*self.tabs + 'if self.actualToken in '+ repr(self.first[val2[0]])]
                parent += ['\t'*self.tabs + '\tself.'+val2[0]+'()']
            elif val2[1] == 'ident' and val2[0] not in self.first.keys():
                parent += ['\t'*self.tabs+'if self.actualToken == "'+val2[0]+'":']
                parent += ['\t'*self.tabs+'\tself.coincidir("'+val2[0]+'")']

        return (parent,first)

    def operations(self):

        operator = self.operators.pop()

        if len(self.values) == 1 and operator[1] == 'br_close':
            val2 = ([],[])
        else:
            val2 = self.values.pop()

        if len(self.values) == 0:
            val1 = ([],[])
        else:
            val1 = self.values.pop()

        parent = None
        if operator[1] == 'concat':
            parent = self.op_concat(val1,val2)
        elif operator[1] == 'union': 
            parent = self.op_union(val1,val2)
        elif operator[1] == 'br_open': 
            parent = self.op_kleene(val1,val2)
        elif operator[1] == 'br_close': 
            parent = self.op_kleeneClose(val1,val2)
        elif operator[1] == 'sq_open': 
            parent = self.op_bracket(val1,val2)
        elif operator[1] == 'sq_close': 
            parent = self.op_bracketClose(val1,val2)

        # print('Parent =>',parent,' y operator =>',operator[1])

        return parent

        

    def status(self, operator):
        if operator == 'concat': 
            return 3
        elif operator == 'union': 
            return 2
        elif operator == 'br_open' or operator == 'sq_open': 
            return 1
        elif operator == 'br_close' or operator == 'sq_close': 
            return 0

    def process_expression(self):
        symbols = ['ident','attr','s_action','tok','white']
        for element in self.expression:
            value, token = element

            # print("Esto es token",token)
            
            if token in symbols:
                self.values.append(element)

            elif token == 'p_open':
                self.operators.append(element)

            #Revisar si esto puede dar error
            elif token == 'p_close':    
                op = self.operators[-1] if self.operators else None
                while(op is not None and op[1] != 'p_open'):
                    parent = self.operations()
                    self.values.append(parent)
                    op = self.operators[-1] if self.operators else None
                
                self.operators.pop()
                self.tabs -= 1

            else:
                op = self.operators[-1] if self.operators else None
                # print("Esto es op",op)
                # print("Esto es token",token)
                while op is not None and op[1] not in ['p_open','p_close'] and (self.status(op[1]) >= self.status(token)):
                    parent = self.operations()
                    self.values.append(parent)
                    op = self.operators[-1] if self.operators else None
                
                self.operators.append(element)

        while(self.operators):
            parent = self.operations()
            self.values.append(parent)

        self.root = self.values.pop()
        # print("Root =>",self.root)

        # for element in self.root[0]:
        #     print(element)
            
# prueba = Tree([('=', 'eq'), (' ', 'white'), ('{', 'br_open'), ('Stat', 'ident'), (' ', 'white'), ('";"', 'tok'), ('{', 'br_open'), ('white', 'ident'), ('}', 'br_close'), ('}', 'br_close'), ('{', 'br_open'), ('white', 'ident'), ('}', 'br_close'), ('"."', 'tok'), ('.', 'p_end')],None)
    # def __init__(self, value, first=[]):
    #     self.value = value
    #     self.left = None
    #     self.right = None
    #     self.first = first
    #     self.isInLeft = True

    # #False indica izquierda, True que va a la derecha
    # def insert(self,value,first):
    #     if self.value:
    #         if self.isInLeft:
    #             if self.left is None:
    #                 self.left = Tree(value,first)
    #             else:
    #                 self.left.insert(value,first)
                
    #             self.isInLeft = False
    #         elif not(self.isInLeft):
    #             if self.right is None:
    #                 self.right = Tree(value,first)
    #             else:
    #                 self.right.insert(value,first)
    #             self.isInLeft = True
    
    # # Print the tree
    # def PrintTree(self):
    #     if self.left:
    #         self.left.PrintTree()
    #     print( self.value),
    #     if self.right:
    #         self.right.PrintTree()

    # # def __str__(self):
    # #     return str(self.value)