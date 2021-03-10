import node

class Thompson:
    def __init__(self,r,w):
        self.expression = r
        self.word = w
        self.values = []
        self.operators = []
        self.cont_nodes = 0
        self.nodes_rutes = {}
        self.all_nodes = []
        self.first_actual = 0
        self.last_actual = 0
        self.inter_actual1 = 0
        self.inter_actual2 = 0
        self.process_expression()

    def nodes_or(self,val1,val2):
        temp_val = [val1,val2]
        if val1 != None and val2 != None:    #En caso es inicio haciendo un |
            #Creo el primer y el ultimo nodo
            primer = node.Node(self.cont_nodes,[('ε',self.cont_nodes+1),('ε',self.cont_nodes+3)])
            ultimo = node.Node(self.cont_nodes+5,[('ε','')])
            self.first_actual = self.cont_nodes
            self.last_actual = self.cont_nodes+5
            self.inter_actual1 = self.cont_nodes
            self.inter_actual2 = self.cont_nodes+5
            self.all_nodes.append(primer)
            self.cont_nodes += 1
            first_l = True #Bandera que servira para determinar si es primera vuelta
            cont_l = 4 #Valor de nodos a sumar para el |
            for val in temp_val:
                #Si es la primera vuelta suma 4 para la ruta del ultimo nodo sino 1
                if not(first_l):
                   cont_l = 2
                #Crea nodo con transicion de valor y su llave
                temp_nodeval = node.Node(self.cont_nodes,[(val,self.cont_nodes+1)])
                temp_node = node.Node(self.cont_nodes+1,[('ε',self.cont_nodes+cont_l)])
                #Guarda los nodos temporales creados
                self.all_nodes.append(temp_nodeval)
                self.all_nodes.append(temp_node)
                self.cont_nodes += 2 #Para cambiar empezar en el nodo "3" del |, o llevarlo al "ultimo"
                first_l = False
            self.all_nodes.append(ultimo)
    

    def operations(self,op,val1,val2=None):
        if op == "|":
            self.nodes_or(val1,val2)




    def status(self,operator):
        if operator == '*':
            return 3
        if operator == '.':
            return 2
        if operator == '|':
            return 1
        return 0

    #Metodo para procesar la expresion ingresada e iniciar la creacion de nodos y sus transiciones
    def process_expression(self):
        cont = 0
        nodes = []
        print(self.expression)
        operadores = ['.','*',')','(','|']
        # try:
        while cont < len(self.expression):
            #En el caso del | se generan 6 nodos diferentes
            print("Caracter: ",self.expression[cont])
            if self.expression[cont] == '(':
                self.operators.append(self.expression[cont])
            elif self.expression[cont] == ')':
                while((self.operators) and self.operators[-1] != '('):
                    op = self.operators.pop()
                    if op != '*':
                        val2 = self.values.pop()
                        val1 = self.values.pop()
                        print('Valor 1: ',val1)
                        print('Valor 2: ',val2)
                        print("La expresion: ",val1+op+val2)
                        self.operations(op,val1,val2)
                        #self.nodes_or(val1,val2,True)
                        print("Nodos")

                        self.values.append(val1+op+val2)
                        nodes.append(val1+op+val2)

                self.operators.pop()

            elif not(self.expression[cont] in operadores):
                self.values.append(self.expression[cont])
                nodes.append(self.expression[cont])
                
            else:
                if(self.expression[cont] != '*'):
                    # print('Operators',self.operators)
                    # print('Operators[-1]',self.operators[-1])
                    # print('cont',cont)
                    # print('Operators[cont]',self.expression[cont])
                    while((self.operators) and self.status(self.operators[-1])>= self.status(self.expression[cont])):
                        # print('Empieza a ver el while')
                        val2 = self.values.pop()
                        val1 = self.values.pop()
                        op = self.operators.pop()
                        print('Valor 1: ',val1)
                        print('Valor 2: ',val2)
                        print("La expresion: ",val1+op+val2)
                        self.values.append(val1+op+val2)
                        self.operations(op,val1,val2)
                        #self.nodes_or(val1,val2,True)
                        print("Nodos",self.all_nodes)
                        nodes.append(self.expression[cont]) 

                    self.operators.append(self.expression[cont])
                else:
                    # print("Entro que es una cadena")
                    val = self.values.pop()
                    op = self.expression[cont]
                    print("La expresion: ",val+op)
                    nodes.append(val+op)
                    self.values.append(val+op)
                    
                    # self.operators.append(self.expression[cont])

            cont += 1


        while(self.operators):
            print("ultimo while")
            print("Valores",self.values)
            print("Operadores",self.operators)
            val2 = self.values.pop()
            val1 = self.values.pop()
            op = self.operators.pop()

            print('Valor 1: ',val1)
            print('Valor 2: ',val2)
            print("La expresion: ",val1+op+val2)

            self.values.append(val2+op+val1)

        for e in self.all_nodes:
            print(e.get_id(),"->",e.get_transitions(),"\n")

            # elif r[cont] == '(':

            # elif r[cont] == ')':

            # elif r[cont] == '.':

            # elif r[cont] == '?':

            # elif r[cont] == '*' or (r[cont] == '*' and r[cont+1] == '*'):


            # else:
            #     if r[cont+1] == '*':

        # except:
        #     print("Algo salio mal con la expresion")

        # print(self.values)
        # print(nodes)