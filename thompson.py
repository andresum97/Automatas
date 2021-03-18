import node
from graphviz import Digraph

class Thompson:
    def __init__(self,r,w):
        self.expression = r
        self.word = w
        self.values = []
        self.operators = []
        self.cont_nodes = 0
        self.all_nodes = []
        self.alphabet = []
        self.last_final = None
        self.first_final = None
        self.process_expression()

    def nodes_or(self,val1,val2):
        temp_val = [val1,val2]
        if len(self.all_nodes) == 0:    #En caso es inicio haciendo un |
            #Creo el primer y el ultimo nodo
            primer = node.Node(self.cont_nodes,[('ε',self.cont_nodes+1),('ε',self.cont_nodes+3)])
            ultimo = node.Node(self.cont_nodes+5,[])
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
                self.all_nodes.append(temp_nodeval)
                self.all_nodes.append(temp_node)
                self.cont_nodes += 2 #Para cambiar empezar en el nodo "3" del |, o llevarlo al "ultimo"
                first_l = False
            self.all_nodes.append(ultimo)

            return primer,ultimo
        else:
            if not(type(val1) == tuple) and not(type(val2) == tuple):
                self.cont_nodes += 1
                primer = node.Node(self.cont_nodes,[('ε',self.cont_nodes+1),('ε',self.cont_nodes+3)])
                ultimo = node.Node(self.cont_nodes+5,[])
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
                    self.all_nodes.append(temp_nodeval)
                    self.all_nodes.append(temp_node)
                    self.cont_nodes += 2 #Para cambiar empezar en el nodo "3" del |, o llevarlo al "ultimo"
                    first_l = False
                self.all_nodes.append(ultimo)

                return primer,ultimo
            if type(val1) == tuple and not(type(val2) == tuple):
                self.cont_nodes += 1
                primer = node.Node(self.cont_nodes,[('ε',val1[0].get_id()),('ε',self.cont_nodes+1)])
                self.all_nodes.append(primer)
                ultimo = node.Node(self.cont_nodes+3,[])
                val1[1].set_transitions(('ε',ultimo.get_id()))
                temp_node2 = node.Node(self.cont_nodes+1,[(val2,self.cont_nodes+2)])
                self.all_nodes.append(temp_node2)
                temp_node3 = node.Node(self.cont_nodes+2,[('ε',ultimo.get_id())])
                self.all_nodes.append(temp_node3)
                self.cont_nodes += 3
                self.all_nodes.append(ultimo)

                return primer,ultimo

            elif not(type(val1) == tuple) and type(val2) == tuple:
                self.cont_nodes += 1
                primer = node.Node(self.cont_nodes,[('ε',val2[0].get_id()),('ε',self.cont_nodes+1)])
                self.all_nodes.append(primer)
                ultimo = node.Node(self.cont_nodes+3,[])
                val2[1].set_transitions(('ε',ultimo.get_id()))
                temp_node2 = node.Node(self.cont_nodes+1,[(val1,self.cont_nodes+2)])
                self.all_nodes.append(temp_node2)
                temp_node3 = node.Node(self.cont_nodes+2,[('ε',ultimo.get_id())])
                self.all_nodes.append(temp_node3)
                self.cont_nodes += 3
                self.all_nodes.append(ultimo)

                return primer,ultimo

            elif type(val1) == tuple and type(val2) == tuple:
                primer = node.Node(self.cont_nodes+1,[('ε',val1[0].get_id()),('ε',val2[0].get_id())])
                ultimo = node.Node(self.cont_nodes+2,[])
                val1[1].set_transitions(('ε',ultimo.get_id()))
                val2[1].set_transitions(('ε',ultimo.get_id()))
                self.all_nodes.append(primer)
                self.all_nodes.append(ultimo)
                self.cont_nodes += 2

                return primer,ultimo

    def nodes_cat(self,val1,val2):
        if len(self.all_nodes) == 0:
            primer = node.Node(self.cont_nodes,[(val1,self.cont_nodes+1)])
            medio = node.Node(self.cont_nodes+1,[(val2,self.cont_nodes+2)])
            ultimo = node.Node(self.cont_nodes+2,[])
            self.all_nodes.append(primer)
            self.all_nodes.append(medio)
            self.all_nodes.append(ultimo)
            self.cont_nodes += 2

            return primer,ultimo

        else:
            if not(type(val1) == tuple) and not(type(val2) == tuple):
                self.cont_nodes += 1
                primer = node.Node(self.cont_nodes,[(val1,self.cont_nodes+1)])
                medio = node.Node(self.cont_nodes+1,[(val2,self.cont_nodes+2)])
                ultimo = node.Node(self.cont_nodes+2,[])
                self.all_nodes.append(primer)
                self.all_nodes.append(medio)
                self.all_nodes.append(ultimo)
                self.cont_nodes += 2
            elif not(type(val1) == tuple) and type(val2) == tuple:
                self.cont_nodes += 1
                primer = node.Node(self.cont_nodes,[(val1,val2[0].get_id())])
                self.all_nodes.append(primer)

                return primer,val2[1]

            elif type(val1) == tuple and not(type(val2) == tuple):
                self.cont_nodes += 1
                ultimo = node.Node(self.cont_nodes, [])
                val1[1].set_transitions((val2,ultimo.get_id()))
                self.all_nodes.append(ultimo)

                return val1[0], ultimo
            
            elif type(val1) == tuple and type(val2) == tuple:
                self.cont_nodes += 1
                val1[1].set_transitions(('ε',val2[0].get_id()))

                return val1[0],val2[1]

    def nodes_kleene(self,val):
        if len(self.all_nodes) == 0:
            primer = node.Node(self.cont_nodes,[('ε',self.cont_nodes+1),('ε',self.cont_nodes+3)])
            medio1 = node.Node(self.cont_nodes+1,[(val,self.cont_nodes+2)])
            medio2 = node.Node(self.cont_nodes+2,[('ε',self.cont_nodes+3),('ε',self.cont_nodes+1)])
            ultimo = node.Node(self.cont_nodes+3,[])

            self.all_nodes.append(primer)
            self.all_nodes.append(medio1)
            self.all_nodes.append(medio2)
            self.all_nodes.append(ultimo)

            self.cont_nodes += 3

            return primer,ultimo
        else:
            if not(type(val) == tuple):
                self.cont_nodes += 1
                primer = node.Node(self.cont_nodes,[('ε',self.cont_nodes+1),('ε',self.cont_nodes+3)])
                medio1 = node.Node(self.cont_nodes+1,[(val,self.cont_nodes+2)])
                medio2 = node.Node(self.cont_nodes+2,[('ε',self.cont_nodes+3),('ε',self.cont_nodes+1)])
                ultimo = node.Node(self.cont_nodes+3,[])

                self.all_nodes.append(primer)
                self.all_nodes.append(medio1)
                self.all_nodes.append(medio2)
                self.all_nodes.append(ultimo)

                self.cont_nodes += 3

                return primer,ultimo

            elif type(val) == tuple:
                self.cont_nodes += 1
                primer = node.Node(self.cont_nodes,[('ε',val[0].get_id()),('ε',self.cont_nodes+1)])
                val[1].set_transitions(('ε',val[0].get_id()))
                val[1].set_transitions(('ε',self.cont_nodes+1))
                ultimo = node.Node(self.cont_nodes+1,[])
                self.all_nodes.append(primer)
                self.all_nodes.append(ultimo)

                self.cont_nodes += 1

                return primer,ultimo

    def operations(self,op,val1,val2=None):
        first = last = None
        if op == "|":
            first, last = self.nodes_or(val1,val2)
        if op == ".":
            first, last = self.nodes_cat(val1,val2)
        if op == "*":
            first, last = self.nodes_kleene(val1)

        return first,last


    def status(self,operator):
        if operator == '*':
            return 3
        if operator == '.':
            return 2
        if operator == '|':
            return 1
        return 0

    def get_results(self):
        estados = []
        transicion = []
        for i in self.all_nodes:
            estados.append(i.get_id())
            for j in i.get_transitions():
                transicion.append((i.get_id(),j[0],j[1]))
        
        simbolos = list(dict.fromkeys(self.alphabet))
        try:
            simbolos.remove('ε')
        except:
            pass
        
        inicio  = self.first_final.get_id()
        final = self.last_final.get_id()
        return estados, simbolos, inicio, final, transicion

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
                     #   print("La expresion: ",val1+op+val2)
                        first,last =  self.operations(op,val1,val2)
                        #self.nodes_or(val1,val2,True)
                        print("Nodos")

                        self.values.append((first,last))##val1+op+val2)
                    #    nodes.append(val1+op+val2)

                self.operators.pop()

            elif not(self.expression[cont] in operadores):
                self.values.append(self.expression[cont])
                self.alphabet.append(self.expression[cont])
           #     nodes.append(self.expression[cont])
                
            else:
                if(self.expression[cont] != '*'):
                    while((self.operators) and self.status(self.operators[-1])>= self.status(self.expression[cont])):
                        # print('Empieza a ver el while')
                        val2 = self.values.pop()
                        val1 = self.values.pop()
                        op = self.operators.pop()
                        print('Valor 1: ',val1)
                        print('Valor 2: ',val2)
                  #      print("La expresion: ",val1+op+val2)
                        first,last = self.operations(op,val1,val2)
                        self.values.append((first,last))#val1+op+val2)
                        #self.nodes_or(val1,val2,True)
                        print("Nodos",self.all_nodes)
                     #   nodes.append(self.expression[cont]) 

                    self.operators.append(self.expression[cont])
                else:
                    # print("Entro que es una cadena")
                    val = self.values.pop()
                    op = self.expression[cont]
                    first, last = self.operations(op,val)
                    self.first_final = first
                    self.last_final = last
                  #  print("La expresion: ",val+op)
                   # nodes.append(val+op)
                    self.values.append((first,last))
                    
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
            #print("La expresion: ",val1+op+val2)
            self.first_final,self.last_final = self.operations(op,val1,val2)
            self.values.append((first,last))#val2+op+val1)

        for e in self.all_nodes:
            print(e.get_id(),"->",e.get_transitions(),"\n")

        #============ Area para Graficar ================================
        f = Digraph('finite_state_machine', filename='thompson.gv')
        f.attr(rankdir='LR', size='8,5')
        f.attr('node', shape='doublecircle')
        f.node(str(self.last_final.get_id()))
        f.attr('node',shape="circle")
        for element in self.all_nodes:
            for info in element.get_transitions():
                f.edge(str(element.get_id()),str(info[1]),label=str(info[0]))

        f.view()

        # Impresion de resultado
        estados = []
        transicion = []
        for i in self.all_nodes:
            estados.append(i.get_id())
            for j in i.get_transitions():
                transicion.append((i.get_id(),j[0],j[1]))

        print("======= Resultados Thompson ========")
        print("Estados => ",estados)
        print("Simbolos => ",list(dict.fromkeys(self.alphabet)))
        print("Inicio => ",self.first_final.get_id())
        print("Aceptacion => ",self.last_final.get_id())
        print("Transicion => ",transicion)
