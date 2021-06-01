#Primero obtener las cadenas de las producciones ya obtenidas de las producciones
# osea el tipo que ya tengo del proyecto 2.
# Pensar como obtener el parrafo de producciones
class Tree():
    def __init__(self, r, f):
        self.expression =  self.add_concat(r) # Regular expression
        self.first = f
        self.values = []
        self.operators = []

        for r in self.expression:
            print('\t->', r[0], r[1])

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

    def operations(self,op,):
        parent = None
        if op[1] == 'concat':
            parent = self.op_concat(va1,val2)
        elif op[1] == 'union': 
            parent = self.ope_union(va1,val2)
        elif op[1] == 'br_open': 
            parent = self.op_kleene(va1,val2)
        elif op[1] == 'br_close': 
            parent = self.op_kleeneClose(va1,val2)
        elif op[1] == 'sq_open': 
            parent = self.op_bracket(va1,val2)
        elif op[1] == 'sq_close': 
            parent = self.op_bracketClose(va1,val2)

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
        self.

prueba = Tree([('=', 'eq'), (' ', 'white'), ('{', 'br_open'), ('Stat', 'ident'), (' ', 'white'), ('";"', 'tok'), ('{', 'br_open'), ('white', 'ident'), ('}', 'br_close'), ('}', 'br_close'), ('{', 'br_open'), ('white', 'ident'), ('}', 'br_close'), ('"."', 'tok'), ('.', 'p_end')],None)
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