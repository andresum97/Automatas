import leaf
from graphviz import Digraph
import json

class AFD:
    def __init__(self,r,w):
        self.expression = '('+r+').'+'#'
        self.word = w
        self.values = []
        self.operators = []
        self.cont_leaf = 0 #Contador general de hojas
        self.cont_valueleaf = 1 #Este sirve para firstpos y laspost
        self.all_leaf = [] #Para guardar las hojas
        self.alphabet = [] #Simbolos del ADF
        self.root = None
        self._infoLeaf = {}  #Key: id de nodo / value [nullable,firstpos,lastpost,followpos]
        self.all_states = {}
        self.list_states = []
        self.leaf_values = {}
        self.states_final = []
        self.routes = []
        self.last_state = 0
        self.process_expression()


    ## Ya estas haciendo aqui el or del arbol
    #Entonces devuelves el valor del id pero pregunta por eso
    #Tambien como manejar ahora los valores
    def nodes_or(self,val1,val2):
        temp_val = [val1,val2]
        if len(self.all_leaf) == 0:    #En caso es inicio haciendo un |
            print("Entro a or cuando esta vacio")
            #Creo el primer y el ultimo nodo
            val1_leaf = leaf.Leaf(self.cont_leaf,val1,self.cont_leaf+2,self.cont_valueleaf,[]) #node.Node(self.cont_nodes,[('ε',self.cont_nodes+1),('ε',self.cont_nodes+3)])
            val2_leaf = leaf.Leaf(self.cont_leaf+1,val2,self.cont_leaf+2,self.cont_valueleaf+1,[])
            op_leaf = leaf.Leaf(self.cont_leaf+2,'|',None,None,[self.cont_leaf,self.cont_leaf+1])
            self.all_leaf.append(val1_leaf)
            self.all_leaf.append(val2_leaf)
            self.all_leaf.append(op_leaf)
            self.cont_leaf += 2
            self.cont_valueleaf += 1
            return op_leaf
        else:
            if not(type(val1) == tuple) and not(type(val2) == tuple):
                self.cont_leaf += 1
                val1_leaf = leaf.Leaf(self.cont_leaf,val1,self.cont_leaf+2,self.cont_valueleaf+1,[]) #node.Node(self.cont_nodes,[('ε',self.cont_nodes+1),('ε',self.cont_nodes+3)])
                val2_leaf = leaf.Leaf(self.cont_leaf+1,val2,self.cont_leaf+2,self.cont_valueleaf+2,[])
                op_leaf = leaf.Leaf(self.cont_leaf+2,'|',None,None,[self.cont_leaf,self.cont_leaf+1])
                self.all_leaf.append(val1_leaf)
                self.all_leaf.append(val2_leaf)
                self.all_leaf.append(op_leaf)
                self.cont_leaf += 2
                self.cont_valueleaf += 2
                return op_leaf
                
            if type(val1) == tuple and not(type(val2) == tuple):
                self.cont_leaf += 1
                #val1_leaf = leaf.Leaf(self.cont_leaf,val1,self.cont_leaf+2,self.cont_valueleaf,[]) #node.Node(self.cont_nodes,[('ε',self.cont_nodes+1),('ε',self.cont_nodes+3)])
                val2_leaf = leaf.Leaf(self.cont_leaf,val2,self.cont_leaf+1,self.cont_valueleaf+1,[])
                val1[0].set_parent(self.cont_leaf+1)
                op_leaf = leaf.Leaf(self.cont_leaf+1,'|',None,None,[val1[0].get_id(),self.cont_leaf])
                self.all_leaf.append(val2_leaf)
                self.all_leaf.append(op_leaf)
                self.cont_leaf += 1
                self.cont_valueleaf += 1
                return op_leaf

            elif not(type(val1) == tuple) and type(val2) == tuple:
                self.cont_leaf += 1
                #val1_leaf = leaf.Leaf(self.cont_leaf,val1,self.cont_leaf+2,self.cont_valueleaf,[]) #node.Node(self.cont_nodes,[('ε',self.cont_nodes+1),('ε',self.cont_nodes+3)])
                val2_leaf = leaf.Leaf(self.cont_leaf,val1,self.cont_leaf+1,self.cont_valueleaf+1,[])
                val2[0].set_parent(self.cont_leaf+1)
                op_leaf = leaf.Leaf(self.cont_leaf+1,'|',None,None,[val2[0].get_id(),self.cont_leaf])
                self.all_leaf.append(val2_leaf)
                self.all_leaf.append(op_leaf)
                self.cont_leaf += 1
                self.cont_valueleaf += 1
                return op_leaf

            elif type(val1) == tuple and type(val2) == tuple:
                self.cont_leaf += 1
                #val1_leaf = leaf.Leaf(self.cont_leaf,val1,self.cont_leaf+2,self.cont_valueleaf,[]) #node.Node(self.cont_nodes,[('ε',self.cont_nodes+1),('ε',self.cont_nodes+3)])
                # val2_leaf = leaf.Leaf(self.cont_leaf,val2,self.cont_leaf+1,self.cont_valueleaf+1,[])
                val1[0].set_parent(self.cont_leaf)
                val2[0].set_parent(self.cont_leaf)
                op_leaf = leaf.Leaf(self.cont_leaf,'|',None,None,[val1[0].get_id(),val2[0].get_id()])
                # self.all_leaf.append(val2_leaf)
                self.all_leaf.append(op_leaf)
                # self.cont_leaf += 1
                # self.cont_valueleaf += 1
                return op_leaf

    def nodes_cat(self,val1,val2):
        if len(self.all_leaf) == 0:
            print("Entro a cat cuando esta vacio")
            val1_leaf = leaf.Leaf(self.cont_leaf,val1,self.cont_leaf+2,self.cont_valueleaf,[]) #node.Node(self.cont_nodes,[('ε',self.cont_nodes+1),('ε',self.cont_nodes+3)])
            val2_leaf = leaf.Leaf(self.cont_leaf+1,val2,self.cont_leaf+2,self.cont_valueleaf+1,[])
            op_leaf = leaf.Leaf(self.cont_leaf+2,'.',None,None,[self.cont_leaf,self.cont_leaf+1])
            self.all_leaf.append(val1_leaf)
            self.all_leaf.append(val2_leaf)
            self.all_leaf.append(op_leaf)
            self.cont_leaf += 2
            self.cont_valueleaf += 1
            return op_leaf

        else:
            if not(type(val1) == tuple) and not(type(val2) == tuple):
                print("Entro a cat cuando esta ni a y b son tuplas")
                self.cont_leaf += 1
                val1_leaf = leaf.Leaf(self.cont_leaf,val1,self.cont_leaf+1,self.cont_valueleaf+1,[]) #node.Node(self.cont_nodes,[('ε',self.cont_nodes+1),('ε',self.cont_nodes+3)])
                val2_leaf = leaf.Leaf(self.cont_leaf+1,val2,self.cont_leaf+2,self.cont_valueleaf+2,[])
                op_leaf = leaf.Leaf(self.cont_leaf+2,'.',None,None,[self.cont_leaf,self.cont_leaf+1])
                self.all_leaf.append(val1_leaf)
                self.all_leaf.append(val2_leaf)
                self.all_leaf.append(op_leaf)
                self.cont_leaf += 2
                self.cont_valueleaf += 2
                return op_leaf

            elif type(val1) == tuple and not(type(val2) == tuple):
                print("Entro a cat cuando a es una tupla y b no lo es")
                self.cont_leaf += 1
                val2_leaf = leaf.Leaf(self.cont_leaf,val2,self.cont_leaf+1,self.cont_valueleaf+1,[])
                val1[0].set_parent(self.cont_leaf+1)
                op_leaf = leaf.Leaf(self.cont_leaf+1,'.',None,None,[val1[0].get_id(),self.cont_leaf])
                self.all_leaf.append(val2_leaf)
                self.all_leaf.append(op_leaf)

                self.cont_leaf += 1
                self.cont_valueleaf += 1

                return op_leaf

            elif not(type(val1)== tuple) and type(val2) == tuple:
                self.cont_leaf += 1
                val2_leaf = leaf.Leaf(self.cont_leaf,val1,self.cont_leaf+1,self.cont_valueleaf+1,[])
                val2[0].set_parent(self.cont_leaf+1)
                op_leaf = leaf.Leaf(self.cont_leaf+1,'.',None,None,[self.cont_leaf,val2[0].get_id()])
                self.all_leaf.append(val2_leaf)
                self.all_leaf.append(op_leaf)

                self.cont_leaf += 1
                self.cont_valueleaf += 1

                return op_leaf
            
            elif type(val1) == tuple and type(val2) == tuple:
                self.cont_leaf += 1
                val1[0].set_parent(self.cont_leaf)
                val2[0].set_parent(self.cont_leaf)
                op_leaf = leaf.Leaf(self.cont_leaf,'.',None,None,[val1[0].get_id(),val2[0].get_id()])
                # self.all_leaf.append(val2_leaf)
                self.all_leaf.append(op_leaf)

                return op_leaf

    def nodes_kleene(self,val):
        if len(self.all_leaf) == 0:
            val_leaf = leaf.Leaf(self.cont_leaf,val,self.cont_leaf+1,self.cont_valueleaf,[]) #node.Node(self.cont_nodes,[('ε',self.cont_nodes+1),('ε',self.cont_nodes+3)])
            # val2_leaf = leaf.Leaf(self.cont_leaf+1,val2,self.cont_leaf+2,[])
            op_leaf = leaf.Leaf(self.cont_leaf+1,'*',None,None,[self.cont_leaf])
            self.all_leaf.append(val_leaf)
            self.all_leaf.append(op_leaf)
            self.cont_leaf += 1
            return op_leaf
        else:
            if not(type(val) == tuple):
                self.cont_leaf += 1
                val_leaf = leaf.Leaf(self.cont_leaf,val,self.cont_leaf+1,self.cont_valueleaf+1,[])
                op_leaf = leaf.Leaf(self.cont_leaf+1,'*',None,None,[self.cont_leaf])
                self.all_leaf.append(val_leaf)
                self.all_leaf.append(op_leaf)
                self.cont_leaf += 1
                self.cont_valueleaf += 1
                return op_leaf

            elif type(val) == tuple:
                self.cont_leaf += 1
                val[0].set_parent(self.cont_leaf)
                op_leaf = leaf.Leaf(self.cont_leaf,'*',None,None,[val[0].get_id()])
                self.all_leaf.append(op_leaf)

                return op_leaf

    def operations(self,op,val1,val2=None):
        parent = None
        if op == "|":
            parent = self.nodes_or(val1,val2)
        if op == ".":
            parent = self.nodes_cat(val1,val2)
        if op == "*":
            parent = self.nodes_kleene(val1)

        return parent


    def status(self,operator):
        if operator == '*':
            return 3
        if operator == '.':
            return 2
        if operator == '|':
            return 1
        return 0


    def getIdByValue(self,value):
        res = 0
        for val in self.all_leaf:
            if value == val.get_idValue():
                res = val.get_id()

        return res


    def nullable(self,leaf):
        value = leaf.get_value()
        _id = leaf.get_id()
        _nullable = None
        if value == '|':
            children = leaf.get_children()
            res1 = self._infoLeaf[children[0]][0]
            res2 = self._infoLeaf[children[1]][0]
            _nullable = res1 or res2
        elif value == '.':
            children = leaf.get_children()
            res1 = self._infoLeaf[children[0]][0]
            res2 = self._infoLeaf[children[1]][0]
            _nullable = res1 and res2
        elif value == '*':
            _nullable = True
        elif value == 'ε':
            _nullable = True
        else:
            _nullable = False

        self._infoLeaf[_id] = [_nullable,[],[],[],leaf.get_idValue(),leaf.get_value()]
    
    def firstpos(self,leaf):
        value = leaf.get_value()
        _id = leaf.get_id()
        _firstpos = None
        print("Id",_id)
        if value == '|':
            children = leaf.get_children()
            for element in children:
                for val in self._infoLeaf[element][1]:
                    self._infoLeaf[_id][1].append(val)
        elif value == '.':
            children = leaf.get_children()
            # print("Concat child",children)
            _nullable1 = self._infoLeaf[children[0]][0]
            if(_nullable1):
                # print("Entro a nullable")
                for element in children:
                    for val in self._infoLeaf[element][1]:
                        self._infoLeaf[_id][1].append(val)
            else:
                # print("Entro a else")
                first_child = self._infoLeaf[children[0]][1]
                # print("First child",first_child)
                for val in first_child:
                    self._infoLeaf[_id][1].append(val)
        elif value == '*':
            children = leaf.get_children()
            # print("Children",children)
            element = self._infoLeaf[children[0]][1]
            for val in element:
                self._infoLeaf[_id][1].append(val)
        elif value == 'ε':
            self._infoLeaf[_id][1] = []
        else:
            _firstpos = leaf.get_idValue()
            self._infoLeaf[_id][1].append(_firstpos)
            self.leaf_values[_firstpos] = value

    def lastpos(self,leaf):
        value = leaf.get_value()
        _id = leaf.get_id()
        _lastpos = None
        print("Id",_id)
        if value == '|':
            children = leaf.get_children()
            for element in children:
                for val in self._infoLeaf[element][2]:
                    self._infoLeaf[_id][2].append(val)
        elif value == '.':
            children = leaf.get_children()
            # print("Concat child",children)
            _nullable1 = self._infoLeaf[children[1]][0]
            if(_nullable1):
                for element in children:
                    for val in self._infoLeaf[element][2]:
                        self._infoLeaf[_id][2].append(val)
            else:
                # print("Entro a else")
                second_child = self._infoLeaf[children[1]][2]
                # print("First child",second_child)
                for val in second_child:
                    self._infoLeaf[_id][2].append(val)
        elif value == '*':
            children = leaf.get_children()
            # print("Children",children)
            element = self._infoLeaf[children[0]][2]
            for val in element:
                self._infoLeaf[_id][2].append(val)
        elif value == 'ε':
            self._infoLeaf[_id][2] = []
        else:
            _firstpos = leaf.get_idValue()
            self._infoLeaf[_id][2].append(_firstpos)

    def followpos(self,leaf):
        value = leaf.get_value()
        _id = leaf.get_id()
        print("Id",_id)
        if value == '.' and len(leaf.get_children()) == 2:
            childrens = leaf.get_children()
            _lastpos = self._infoLeaf[childrens[0]][2]
            for element in _lastpos:
                for val in self._infoLeaf[childrens[1]][1]:
                    realid = self.getIdByValue(element)
                    self._infoLeaf[realid][3].append(val)
    
        elif value == '*':
            _lastpos = self._infoLeaf[_id][2]
            _firstpos_n = self._infoLeaf[_id][1]
            for element in _lastpos:
                for val in _firstpos_n:
                    realid = self.getIdByValue(element)
                    print("realid",realid)
                    print(self._infoLeaf)
                    self._infoLeaf[realid][3].append(val)

    def create_states(self):
        cont_states = 1
        print('Raiz',self.root.get_id())
        self.alphabet.remove('#')
        fp_root = self._infoLeaf[self.root.get_id()][1] #First pos de la raiz o estado A
        print(fp_root)
        temp_values_state = []
        self.all_states[str(fp_root)] = 'S0'
        self.list_states.append(fp_root)
        _isFinal = False

        for states in self.list_states:
            print("Lista de estados",states)
            for letter in self.alphabet:
                print("Letra del alfabeto",letter)
                for val in states:
                    # print("Valor del estado",val)
                    # print("Valor de hojas",self.leaf_values)
                    if letter == self.leaf_values[val]:
                        temp_values_state.append(val)

                temp_values_state = list(dict.fromkeys(temp_values_state))
                temp_values_state.sort()
                print('Valores temporales',temp_values_state)
                temp_state = []
                for element in temp_values_state:
                    for _leaf in self._infoLeaf.items():
                        # print('Leaf',_leaf)
                        if _leaf[1][4] == element:
                            temp_state += _leaf[1][3]
                            print("print",_leaf[1])
                            # if self.last_state == _leaf[1][3]:
                            #     _isFinal = True

                if temp_state != []:
                    temp_state.sort()
                    temp_state = list(dict.fromkeys(temp_state))
                    print("Valor de estado",temp_state)
                    
                    if(not(str(temp_state)) in self.all_states):
                        print("Ingreso al ultimo if")
                        self.all_states[(str(temp_state))] = 'S'+str(cont_states)
                        print("Todos los estados",self.all_states)
                        self.list_states.append(temp_state)
                        cont_states += 1
                    
                    # if _isFinal:
                    #     self.states_final.append(self.all_states[(str(temp_state))])

                    self.routes.append((self.all_states[str(states)],letter,self.all_states[str(temp_state)]))
                temp_values_state = []
                _isFinal = False

        self.routes = list(dict.fromkeys(self.routes))

                


    # def get_results(self):
    #     estados = []
    #     transicion = []
    #     for i in self.all_nodes:
    #         estados.append(i.get_id())
    #         for j in i.get_transitions():
    #             transicion.append((i.get_id(),j[0],j[1]))
        
    #     simbolos = list(dict.fromkeys(self.alphabet))
    #     inicio  = self.first_final.get_id()
    #     final = self.last_final.get_id()
    #     return estados, simbolos, inicio, final, transicion

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
                        parent =  self.operations(op,val1,val2)
                        #self.nodes_or(val1,val2,True)
                        print("Nodos")

                        self.values.append((parent,))##val1+op+val2)
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
                        parent = self.operations(op,val1,val2)
                        self.values.append((parent,))#val1+op+val2)
                        #self.nodes_or(val1,val2,True)
                      #  print("Nodos",self.all_nodes)
                     #   nodes.append(self.expression[cont]) 

                    self.operators.append(self.expression[cont])
                else:
                    # print("Entro que es una cadena")
                    val = self.values.pop()
                    op = self.expression[cont]
                    parent = self.operations(op,val)
                    # self.first_final = first
                    # self.last_final = last
                    self.values.append((parent,))
                    
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
            self.root = self.operations(op,val1,val2)
            self.values.append((self.root,))#val2+op+val1)

        print("all leaf",self.all_leaf)
        for e in self.all_leaf:
            print(e.get_id(),", - valor de nodo ->",e.get_value(),'- hijos -> ',e.get_children(),'- valor de hoja -> ',e.get_idValue())

        #Nullable
        for e in self.all_leaf:
            self.nullable(e)
            self.firstpos(e)
            self.lastpos(e)
        
        for e in self.all_leaf:
            self.followpos(e)
            
        #Para ordenar los followpos
        for e in self.all_leaf:
            _id = e.get_id()
            self._infoLeaf[_id][3] = list(dict.fromkeys(self._infoLeaf[_id][3]))


        def pretty(d, indent=0):
            for key, value in d.items():
                print('\t' * indent + str(key))
                if isinstance(value, dict):
                    pretty(value, indent+1)
                else:
                    print('\t' * (indent+1) + str(value))

        keys = list(self.leaf_values.keys())
        position = list(self.leaf_values.values()).index('#')
        self.last_state = keys[position]
        
        pretty(self._infoLeaf)
        pretty(self.leaf_values)
        self.create_states()
        pretty(self.all_states)
        print("Rutas")
        print(self.routes)
        for element in self.all_states.keys():
            _element = json.loads(element)
            for val in _element:
                if val == self.last_state:
                    self.states_final.append(self.all_states[element])
            print("Element",element)            

        self.states_final = list(dict.fromkeys(self.states_final))
        #print("Info leafs: ",json.dumps(self._infoLeaf))


        #Encontrar nodos finales






        #============ Area para Graficar ================================
        f = Digraph('AFD', filename='AFD.gv')
        f.attr(rankdir='LR', size='8,5')
        f.attr('node', shape='doublecircle')
        for finals in self.states_final:
            f.node(finals)
        f.attr('node',shape="circle")
        for element in self.routes:
            f.edge(element[0],element[2],label=str(element[1]))

        f.view()

        # # Impresion de resultado
        # estados = []
        # transicion = []
        # for i in self.all_nodes:
        #     estados.append(i.get_id())
        #     for j in i.get_transitions():
        #         transicion.append((i.get_id(),j[0],j[1]))

        print("======= Resultados Thompson ========")
        print("Estados => ",self.all_states.values())
        print("Simbolos => ",list(dict.fromkeys(self.alphabet)))
        print("Inicio => ",list(self.all_states.values())[0])
        print("Aceptacion => ",self.states_final)
        print("Transicion => ",self.routes)