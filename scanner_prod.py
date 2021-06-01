 
# coding=utf8
import leaf
import json

class AFD:
    def __init__(self,r,w):
        self.expression = r #'('+r+').'+'#'
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
        self.last_state = []
        self.token = {'s_action': '˂(˃˂.˃˂˂\t˥\x0b˥\r˥\x0e˥ ˥!˥"˥#˥$˥%˥&˥\'˥(˥)˥*˥+˥,˥-˥.˥/˥0˥1˥2˥3˥4˥5˥6˥7˥8˥9˥:˥;˥<˥=˥>˥?˥@˥A˥B˥C˥D˥E˥F˥G˥H˥I˥J˥K˥L˥M˥N˥O˥P˥Q˥R˥S˥T˥U˥V˥W˥X˥Y˥Z˥[˥\\˥]˥^˥_˥`˥a˥b˥c˥d˥e˥f˥g˥h˥i˥j˥k˥l˥m˥n˥o˥p˥q˥r˥s˥t˥u˥v˥w˥x˥y˥z˥{˥|˥}˥~˥\x7f˥\r˥\t˥ ˃˃˄˂.˃˂)˃', 'ident': '˂A˥B˥C˥D˥E˥F˥G˥H˥I˥J˥K˥L˥M˥N˥O˥P˥Q˥R˥S˥T˥U˥V˥W˥X˥Y˥Z˥a˥b˥c˥d˥e˥f˥g˥h˥i˥j˥k˥l˥m˥n˥o˥p˥q˥r˥s˥t˥u˥v˥w˥x˥y˥z˃˂˂A˥B˥C˥D˥E˥F˥G˥H˥I˥J˥K˥L˥M˥N˥O˥P˥Q˥R˥S˥T˥U˥V˥W˥X˥Y˥Z˥a˥b˥c˥d˥e˥f˥g˥h˥i˥j˥k˥l˥m˥n˥o˥p˥q˥r˥s˥t˥u˥v˥w˥x˥y˥z˃˥˂0˥1˥2˥3˥4˥5˥6˥7˥8˥9˃˃˄', 'tok': '˂"˃˂\t˥\n˥\x0b˥\r˥\x0e˥ ˥!˥#˥$˥%˥&˥\'˥(˥)˥*˥+˥,˥-˥.˥/˥0˥1˥2˥3˥4˥5˥6˥7˥8˥9˥:˥;˥<˥=˥>˥?˥@˥A˥B˥C˥D˥E˥F˥G˥H˥I˥J˥K˥L˥M˥N˥O˥P˥Q˥R˥S˥T˥U˥V˥W˥X˥Y˥Z˥[˥\\˥]˥^˥_˥`˥a˥b˥c˥d˥e˥f˥g˥h˥i˥j˥k˥l˥m˥n˥o˥p˥q˥r˥s˥t˥u˥v˥w˥x˥y˥z˥{˥|˥}˥~˥\x7f˃˂"˃', 'eq': '˂=˃', 'p_end': '˂.˃', 'br_open': '˂{˃', 'br_close': '˂}˃', 'sq_open': '˂[˃', 'sq_close': '˂]˃', 'p_open': '˂(˃', 'p_close': '˂)˃', 'union': '˂|˃', 'attr': '˂<˃˂˂\t˥\x0b˥\r˥\x0e˥ ˥!˥"˥#˥$˥%˥&˥\'˥(˥)˥*˥+˥,˥-˥.˥/˥0˥1˥2˥3˥4˥5˥6˥7˥8˥9˥:˥;˥<˥=˥>˥?˥@˥A˥B˥C˥D˥E˥F˥G˥H˥I˥J˥K˥L˥M˥N˥O˥P˥Q˥R˥S˥T˥U˥V˥W˥X˥Y˥Z˥[˥\\˥]˥^˥_˥`˥a˥b˥c˥d˥e˥f˥g˥h˥i˥j˥k˥l˥m˥n˥o˥p˥q˥r˥s˥t˥u˥v˥w˥x˥y˥z˥{˥|˥}˥~˥\x7f˥\r˥\t˥ ˃˃˄˂>˃', 'white': '˂\n˥\r˥\t˥ ˃˂˂\n˥\r˥\t˥ ˃˃˄'}
        self.excepciones = {'s_action': [], 'ident': [], 'tok': [], 'eq': [], 'p_end': [], 'br_open': [], 'br_close': [], 'sq_open': [], 'sq_close': [], 'p_open': [], 'p_close': [], 'union': [], 'attr': [], 'white': []}
        self.verification = {}
        self.states_tokens = {}
        self.states_inverse = {}
        self.productions = []
        self.process_expression()


    
    ## Ya estas haciendo aqui el or del arbol
    #Entonces devuelves el valor del id pero pregunta por eso
    #Tambien como manejar ahora los valores
    def nodes_or(self,val1,val2):
        temp_val = [val1,val2]
        if len(self.all_leaf) == 0:    #En caso es inicio haciendo un |
            # print("Entro a or cuando esta vacio")
            #Creo el primer y el ultimo nodo
            val1_leaf = leaf.Leaf(self.cont_leaf,val1,self.cont_leaf+2,self.cont_valueleaf,[]) #node.Node(self.cont_nodes,[('ε',self.cont_nodes+1),('ε',self.cont_nodes+3)])
            val2_leaf = leaf.Leaf(self.cont_leaf+1,val2,self.cont_leaf+2,self.cont_valueleaf+1,[])
            op_leaf = leaf.Leaf(self.cont_leaf+2,chr(741),None,None,[self.cont_leaf,self.cont_leaf+1])
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
                op_leaf = leaf.Leaf(self.cont_leaf+2,chr(741),None,None,[self.cont_leaf,self.cont_leaf+1])
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
                op_leaf = leaf.Leaf(self.cont_leaf+1,chr(741),None,None,[val1[0].get_id(),self.cont_leaf])
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
                op_leaf = leaf.Leaf(self.cont_leaf+1,chr(741),None,None,[val2[0].get_id(),self.cont_leaf])
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
                op_leaf = leaf.Leaf(self.cont_leaf,chr(741),None,None,[val1[0].get_id(),val2[0].get_id()])
                # self.all_leaf.append(val2_leaf)
                self.all_leaf.append(op_leaf)
                # self.cont_leaf += 1
                # self.cont_valueleaf += 1
                return op_leaf

    def nodes_cat(self,val1,val2):
        if len(self.all_leaf) == 0:
            # print("Entro a cat cuando esta vacio")
            val1_leaf = leaf.Leaf(self.cont_leaf,val1,self.cont_leaf+2,self.cont_valueleaf,[]) #node.Node(self.cont_nodes,[('ε',self.cont_nodes+1),('ε',self.cont_nodes+3)])
            val2_leaf = leaf.Leaf(self.cont_leaf+1,val2,self.cont_leaf+2,self.cont_valueleaf+1,[])
            op_leaf = leaf.Leaf(self.cont_leaf+2,chr(765),None,None,[self.cont_leaf,self.cont_leaf+1])
            self.all_leaf.append(val1_leaf)
            self.all_leaf.append(val2_leaf)
            self.all_leaf.append(op_leaf)
            self.cont_leaf += 2
            self.cont_valueleaf += 1
            return op_leaf

        else:
            if not(type(val1) == tuple) and not(type(val2) == tuple):
                # print("Entro a cat cuando esta ni a y b son tuplas")
                self.cont_leaf += 1
                val1_leaf = leaf.Leaf(self.cont_leaf,val1,self.cont_leaf+1,self.cont_valueleaf+1,[]) #node.Node(self.cont_nodes,[('ε',self.cont_nodes+1),('ε',self.cont_nodes+3)])
                val2_leaf = leaf.Leaf(self.cont_leaf+1,val2,self.cont_leaf+2,self.cont_valueleaf+2,[])
                op_leaf = leaf.Leaf(self.cont_leaf+2,chr(765),None,None,[self.cont_leaf,self.cont_leaf+1])
                self.all_leaf.append(val1_leaf)
                self.all_leaf.append(val2_leaf)
                self.all_leaf.append(op_leaf)
                self.cont_leaf += 2
                self.cont_valueleaf += 2
                return op_leaf

            elif type(val1) == tuple and not(type(val2) == tuple):
                # print("Entro a cat cuando a es una tupla y b no lo es")
                self.cont_leaf += 1
                val2_leaf = leaf.Leaf(self.cont_leaf,val2,self.cont_leaf+1,self.cont_valueleaf+1,[])
                val1[0].set_parent(self.cont_leaf+1)
                op_leaf = leaf.Leaf(self.cont_leaf+1,chr(765),None,None,[val1[0].get_id(),self.cont_leaf])
                self.all_leaf.append(val2_leaf)
                self.all_leaf.append(op_leaf)

                self.cont_leaf += 1
                self.cont_valueleaf += 1

                return op_leaf

            elif not(type(val1)== tuple) and type(val2) == tuple:
                self.cont_leaf += 1
                val2_leaf = leaf.Leaf(self.cont_leaf,val1,self.cont_leaf+1,self.cont_valueleaf+1,[])
                val2[0].set_parent(self.cont_leaf+1)
                op_leaf = leaf.Leaf(self.cont_leaf+1,chr(765),None,None,[self.cont_leaf,val2[0].get_id()])
                self.all_leaf.append(val2_leaf)
                self.all_leaf.append(op_leaf)

                self.cont_leaf += 1
                self.cont_valueleaf += 1

                return op_leaf
            
            elif type(val1) == tuple and type(val2) == tuple:
                self.cont_leaf += 1
                val1[0].set_parent(self.cont_leaf)
                val2[0].set_parent(self.cont_leaf)
                op_leaf = leaf.Leaf(self.cont_leaf,chr(765),None,None,[val1[0].get_id(),val2[0].get_id()])
                # self.all_leaf.append(val2_leaf)
                self.all_leaf.append(op_leaf)

                return op_leaf

    def nodes_kleene(self,val):
        if len(self.all_leaf) == 0:
            val_leaf = leaf.Leaf(self.cont_leaf,val,self.cont_leaf+1,self.cont_valueleaf,[]) #node.Node(self.cont_nodes,[('ε',self.cont_nodes+1),('ε',self.cont_nodes+3)])
            # val2_leaf = leaf.Leaf(self.cont_leaf+1,val2,self.cont_leaf+2,[])
            op_leaf = leaf.Leaf(self.cont_leaf+1,chr(708),None,None,[self.cont_leaf])
            self.all_leaf.append(val_leaf)
            self.all_leaf.append(op_leaf)
            self.cont_leaf += 1
            return op_leaf
        else:
            if not(type(val) == tuple):
                self.cont_leaf += 1
                val_leaf = leaf.Leaf(self.cont_leaf,val,self.cont_leaf+1,self.cont_valueleaf+1,[])
                op_leaf = leaf.Leaf(self.cont_leaf+1,chr(708),None,None,[self.cont_leaf])
                self.all_leaf.append(val_leaf)
                self.all_leaf.append(op_leaf)
                self.cont_leaf += 1
                self.cont_valueleaf += 1
                return op_leaf

            elif type(val) == tuple:
                self.cont_leaf += 1
                val[0].set_parent(self.cont_leaf)
                op_leaf = leaf.Leaf(self.cont_leaf,chr(708),None,None,[val[0].get_id()])
                self.all_leaf.append(op_leaf)

                return op_leaf

    def operations(self,op,val1,val2=None):
        parent = None
        if op == chr(741):
            parent = self.nodes_or(val1,val2)
        if op == chr(765):
            parent = self.nodes_cat(val1,val2)
        if op == chr(708):
            parent = self.nodes_kleene(val1)

        return parent


    def status(self,operator):
        if operator == chr(708):
            return 3
        if operator == chr(765):
            return 2
        if operator == chr(741):
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
        if value == chr(741):
            children = leaf.get_children()
            res1 = self._infoLeaf[children[0]][0]
            res2 = self._infoLeaf[children[1]][0]
            _nullable = res1 or res2
        elif value == chr(765):
            children = leaf.get_children()
            res1 = self._infoLeaf[children[0]][0]
            res2 = self._infoLeaf[children[1]][0]
            _nullable = res1 and res2
        elif value == chr(708):
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
        # print("Id",_id)
        if value == chr(741):
            children = leaf.get_children()
            for element in children:
                for val in self._infoLeaf[element][1]:
                    self._infoLeaf[_id][1].append(val)
        elif value == chr(765):
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
        elif value == chr(708):
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
        # print("Id",_id)
        if value == chr(741):
            children = leaf.get_children()
            for element in children:
                for val in self._infoLeaf[element][2]:
                    self._infoLeaf[_id][2].append(val)
        elif value == chr(765):
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
        elif value == chr(708):
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
        # print("Id",_id)
        if value == chr(765) and len(leaf.get_children()) == 2:
            childrens = leaf.get_children()
            _lastpos = self._infoLeaf[childrens[0]][2]
            for element in _lastpos:
                for val in self._infoLeaf[childrens[1]][1]:
                    realid = self.getIdByValue(element)
                    self._infoLeaf[realid][3].append(val)
    
        elif value == chr(708):
            _lastpos = self._infoLeaf[_id][2]
            _firstpos_n = self._infoLeaf[_id][1]
            for element in _lastpos:
                for val in _firstpos_n:
                    realid = self.getIdByValue(element)
                    # print("realid",realid)
                    # print(self._infoLeaf)
                    self._infoLeaf[realid][3].append(val)

    def create_states(self):
        cont_states = 1
        #print('Raiz',self.root.get_id())
        self.alphabet.remove(chr(920))
        fp_root = self._infoLeaf[self.root.get_id()][1] #First pos de la raiz o estado A
        # print(fp_root)
        temp_values_state = []
        self.all_states[str(fp_root)] = 'S0'
        self.list_states.append(fp_root)
        _isFinal = False


        #Verificacion de estados para tabla final
        for states in self.list_states:
            for letter in self.alphabet:
                # print("Letra del alfabeto",letter)
                for val in states:
                    # print("Valor del estado",val)
                    # print("Valor de hojas",self.leaf_values)
                    if letter == self.leaf_values[val]:
                        temp_values_state.append(val)

                temp_values_state = list(dict.fromkeys(temp_values_state))
                temp_values_state.sort()
                # print('Valores temporales',temp_values_state)
                temp_state = []
                for element in temp_values_state:
                    for _leaf in self._infoLeaf.items():
                        # print('Leaf',_leaf)
                        if _leaf[1][4] == element:
                            temp_state += _leaf[1][3]
                          #  print("print",_leaf[1])
                            # if self.last_state == _leaf[1][3]:
                            #     _isFinal = True

                if temp_state != []:
                    temp_state.sort()
                    temp_state = list(dict.fromkeys(temp_state))
                    # print("Valor de estado",temp_state)
                    
                    if(not(str(temp_state)) in self.all_states):
                        # print("Ingreso al ultimo if")
                        self.all_states[(str(temp_state))] = 'S'+str(cont_states)
                        # print("Todos los estados",self.all_states)
                        self.list_states.append(temp_state)
                        # Aqui se asigna a que token corresponde el estado
                        cont_states += 1
                    
                    # if _isFinal:
                    #     self.states_final.append(self.all_states[(str(temp_state))])

                    self.routes.append((self.all_states[str(states)],letter,self.all_states[str(temp_state)]))
                temp_values_state = []
                _isFinal = False

        self.routes = list(dict.fromkeys(self.routes))
  
    def simulacionTokens(self,word,pos):
        # s0 = list(self.all_states.values())[0])
        token = ''
        match = True
        check = pos
        index = pos
        finalState = []
        _state = 'S0'
        _isValid = True
        _isInSymbol = True
        res = None

        while match and index < len(word):   
            # for c in word[index]:
                # if not(_isValid):
                #     break
            # if word[index] not in self.alphabet:
            #     _isInSymbol = False
            for t in self.routes:
                if t[0] == _state and t[1] == word[index]:
                    _state = t[2]
                    _isValid = True
                    break
                else:
                    _isValid = False

            if not(_isValid):
                _state = None

            if _state in self.states_final:
                check = index
                finalState = self.states_inverse[_state]
            
            if _state == None:
                match = False
            
            index += 1
        token = word[pos:check + 1]
        for key,value in self.verification.items():
            if str(value) in finalState:
                res = key
        return token, check+1, res
        


    def Simulacion(self):
        _state = 'S0'
        _isValid = True
        _isInSymbol = True
        for c in self.word:
            if not(_isValid):
                break
            if c not in self.alphabet:
                _isInSymbol = False
            for t in self.routes:
                if t[0] == _state and t[1] == c:
                    _state = t[2]
                    _isValid = True
                    break
                else:
                    _isValid = False

        if(_state in self.states_final and _isInSymbol):
            print("******************************* SI es valida la palabra ********************************")
            for key,value in self.states_tokens.items():
                if _state in value:
                    print("Es un "+key)
        else:
            print("******************************* NO es valida la palabra ********************************")

    #Metodo para procesar la expresion ingresada e iniciar la creacion de nodos y sus transiciones
    def process_expression(self):
        cont = 0
        nodes = []
        # print(self.expression)
        operadores = [chr(765),chr(708),chr(707),chr(706),chr(741)] #['.','*',')','(','|']
        # try:
        while cont < len(self.expression):
            #En el caso del | se generan 6 nodos diferentes
            # print("Caracter: ",self.expression[cont])
            if self.expression[cont] == chr(706):
                self.operators.append(self.expression[cont])
            elif self.expression[cont] == chr(707):
                while((self.operators) and self.operators[-1] != chr(706)):
                    op = self.operators.pop()
                    if op != chr(708):
                        val2 = self.values.pop()
                        val1 = self.values.pop()
                        # print('Valor 1: ',val1)
                        # print('Valor 2: ',val2)
                     #   print("La expresion: ",val1+op+val2)
                        parent =  self.operations(op,val1,val2)
                        #self.nodes_or(val1,val2,True)
                        # print("Nodos")

                        self.values.append((parent,))##val1+op+val2)
                    #    nodes.append(val1+op+val2)

                self.operators.pop()

            elif not(self.expression[cont] in operadores):
                self.values.append(self.expression[cont])
                self.alphabet.append(self.expression[cont])
           #     nodes.append(self.expression[cont])
                
            else:
                if(self.expression[cont] != chr(708)):
                    while((self.operators) and self.status(self.operators[-1])>= self.status(self.expression[cont])):
                        # print('Empieza a ver el while')
                        val2 = self.values.pop()
                        val1 = self.values.pop()
                        op = self.operators.pop()
                        # print('Valor 1: ',val1)
                        # print('Valor 2: ',val2)
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
            # print("ultimo while")
            # print("Valores",self.values)
            # print("Operadores",self.operators)
            val2 = self.values.pop()
            val1 = self.values.pop()
            op = self.operators.pop()

            # print('Valor 1: ',val1)
            # print('Valor 2: ',val2)
            #print("La expresion: ",val1+op+val2)
            self.root = self.operations(op,val1,val2)
            # print("Raiz->",self.root)
            self.values.append((self.root,))#val2+op+val1)

        # print("all leaf",self.all_leaf)
        for e in self.all_leaf:
            # print(e.get_id(),", - valor de nodo ->",e.get_value(),'- hijos -> ',e.get_children(),'- valor de hoja -> ',e.get_idValue(), '- padre -> ',e.get_parent())
            if e.get_parent() == None:
                self.root = e
            # if e.get_value() == '#':


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
                print('	' * indent + str(key))
                if isinstance(value, dict):
                    pretty(value, indent+1)
                else:
                    print('	' * (indent+1) + str(value))

        keys = list(self.leaf_values.keys())
        # print("Hojas->",self.leaf_values.values())
        cont = 0
        for val in list(self.leaf_values.values()):
            # print("VAL->",val)
            if val == chr(920):
                self.last_state.append(keys[cont])
            cont += 1
        
        # print("Ultimos estados->",self.last_state)
        # position = list(self.leaf_values.values()).index('#')
        # self.last_state = keys[position]
        

        # pretty(self._infoLeaf)
        # pretty(self.leaf_values)
    
        self.create_states()

        cont = 0
        for key in self.token.keys():
            newKey = self.last_state[cont]
            self.verification[key] = newKey
            self.states_tokens[key] = []
            cont += 1

        #print("Verificacion -> ",self.verification)
        #print('Estados ->',self.all_states)

        for key,value in self.all_states.items():
            self.states_inverse[value] = key

        #print('Inverso ',self.states_inverse)
        #Verificacion si un estado final esta dentro del estado a revisar
        # print("Lista de estados",states)
        llave_token = None
        esEstadoFinal = False
        for state,val in self.all_states.items():
            # print("Estado->",state)
            for keys,value in self.verification.items():
                # print("Keys->",keys)
                if str(keys) in state:
                    # print("En este estado hay un token")
                    self.states_tokens[value].append(val)

        #print("Estados de tokens->",self.states_tokens)
        # print("States tokens->",self.states_tokens)
        #  print("Entro aqui y estado final es ->",esEstadoFinal,'Y el estado es ->',str(temp_state))
        # if esEstadoFinal:
        #     print("Entro al if")
        #     self.states_tokens[llave_token].append(self.all_states[(str(temp_state))])




        # pretty(self.all_states)
        # print("Rutas")
        # print(self.routes)
        for element in self.all_states.keys():
            _element = json.loads(element)
            for val in _element:
                if val in self.last_state:
                    self.states_final.append(self.all_states[element])
            # print("Element",element)            

        self.states_final = list(dict.fromkeys(self.states_final))
        #print("Finales ",self.states_final)

        
        #print("Info leafs: ",json.dumps(self._infoLeaf))


        #Encontrar nodos finales






        #============ Area para Graficar ================================
        # f = Digraph('AFD', filename='AFD.gv')
        # f.attr(rankdir='LR', size='8,5')
        # f.attr('node', shape='doublecircle')
        # for finals in self.states_final:
        #     f.node(finals)
        # f.attr('node',shape="circle")
        # for element in self.routes:
        #     f.edge(element[0],element[2],label=str(element[1]))

        # f.view()

        # # Impresion de resultado
        # estados = []
        # transicion = []
        # for i in self.all_nodes:
        #     estados.append(i.get_id())
        #     for j in i.get_transitions():
        #         transicion.append((i.get_id(),j[0],j[1]))
        try:
            self.alphabet.remove('ε')
        except:
            pass

    
        primero = False
        resultados = []
        # self.Simulacion()
        #Ciclo que va recorriendo las distintas lineas de la produccion encontrada y va encontrando lo tokens y poniendo su tipo
        for expr in self.word:
            pos = 0
            # key = ""
            while pos < len(expr):
                token, pos, identificador = self.simulacionTokens(expr,pos)
                if identificador:
                    acepta = True
                    for exp in self.excepciones[identificador]:
                        if token == exp:
                            acepta = False
                            print('[======',repr(exp),'es el keyword', exp,' ======]')
                            break
                    if acepta:
                        resultados.append((token,identificador))
                        print("[====== El simbolo es ",repr(token),' y es de tipo ->',identificador,'======]')
                else:
                    resultados.append((token,"no_esperado"))
                    print('[======',repr(token),'es un simbolo no esperado ======]')
            
            self.productions = resultados


##========================= Menu =================



#Clase que va a obtener las producciones
class lecProductions():
    def __init__(self,word):
        self.word = word
        self.expression = '˂˂˂(˃˂.˃˂˂\t˥\x0b˥\r˥\x0e˥ ˥!˥"˥#˥$˥%˥&˥\'˥(˥)˥*˥+˥,˥-˥.˥/˥0˥1˥2˥3˥4˥5˥6˥7˥8˥9˥:˥;˥<˥=˥>˥?˥@˥A˥B˥C˥D˥E˥F˥G˥H˥I˥J˥K˥L˥M˥N˥O˥P˥Q˥R˥S˥T˥U˥V˥W˥X˥Y˥Z˥[˥\\˥]˥^˥_˥`˥a˥b˥c˥d˥e˥f˥g˥h˥i˥j˥k˥l˥m˥n˥o˥p˥q˥r˥s˥t˥u˥v˥w˥x˥y˥z˥{˥|˥}˥~˥\x7f˥\r˥\t˥ ˃˃˄˂.˃˂)˃˃Θ˃˥˂˂˂A˥B˥C˥D˥E˥F˥G˥H˥I˥J˥K˥L˥M˥N˥O˥P˥Q˥R˥S˥T˥U˥V˥W˥X˥Y˥Z˥a˥b˥c˥d˥e˥f˥g˥h˥i˥j˥k˥l˥m˥n˥o˥p˥q˥r˥s˥t˥u˥v˥w˥x˥y˥z˃˂˂A˥B˥C˥D˥E˥F˥G˥H˥I˥J˥K˥L˥M˥N˥O˥P˥Q˥R˥S˥T˥U˥V˥W˥X˥Y˥Z˥a˥b˥c˥d˥e˥f˥g˥h˥i˥j˥k˥l˥m˥n˥o˥p˥q˥r˥s˥t˥u˥v˥w˥x˥y˥z˃˥˂0˥1˥2˥3˥4˥5˥6˥7˥8˥9˃˃˄˃Θ˃˥˂˂˂"˃˂\t˥\n˥\x0b˥\r˥\x0e˥ ˥!˥#˥$˥%˥&˥\'˥(˥)˥*˥+˥,˥-˥.˥/˥0˥1˥2˥3˥4˥5˥6˥7˥8˥9˥:˥;˥<˥=˥>˥?˥@˥A˥B˥C˥D˥E˥F˥G˥H˥I˥J˥K˥L˥M˥N˥O˥P˥Q˥R˥S˥T˥U˥V˥W˥X˥Y˥Z˥[˥\\˥]˥^˥_˥`˥a˥b˥c˥d˥e˥f˥g˥h˥i˥j˥k˥l˥m˥n˥o˥p˥q˥r˥s˥t˥u˥v˥w˥x˥y˥z˥{˥|˥}˥~˥\x7f˃˂"˃˃Θ˃˥˂˂˂=˃˃Θ˃˥˂˂˂.˃˃Θ˃˥˂˂˂{˃˃Θ˃˥˂˂˂}˃˃Θ˃˥˂˂˂[˃˃Θ˃˥˂˂˂]˃˃Θ˃˥˂˂˂(˃˃Θ˃˥˂˂˂)˃˃Θ˃˥˂˂˂|˃˃Θ˃˥˂˂˂<˃˂˂\t˥\x0b˥\r˥\x0e˥ ˥!˥"˥#˥$˥%˥&˥\'˥(˥)˥*˥+˥,˥-˥.˥/˥0˥1˥2˥3˥4˥5˥6˥7˥8˥9˥:˥;˥<˥=˥>˥?˥@˥A˥B˥C˥D˥E˥F˥G˥H˥I˥J˥K˥L˥M˥N˥O˥P˥Q˥R˥S˥T˥U˥V˥W˥X˥Y˥Z˥[˥\\˥]˥^˥_˥`˥a˥b˥c˥d˥e˥f˥g˥h˥i˥j˥k˥l˥m˥n˥o˥p˥q˥r˥s˥t˥u˥v˥w˥x˥y˥z˥{˥|˥}˥~˥\x7f˥\r˥\t˥ ˃˃˄˂>˃˃Θ˃˥˂˂˂\n˥\r˥\t˥ ˃˂˂\n˥\r˥\t˥ ˃˃˄˃Θ˃'
        res = self.replace(self.expression)
        self.res_final = self.add_concat(res)
        self.resultado = []
        self.key = ""
        self.execAFD()
        

    def replace(self,r):
        #ε
        i = 0
        expr = ''
        par = []
        sub = ''
        resta = []
        while i <len(r):
            if(r[i] == chr(706)):
                par.append(i)
            # if r[i] == '+':
                
            #     if(r[i-1] == chr(707)):

            #         sub = r[par.pop():i]
                    
            #         expr = expr + chr(708) + sub
            #     else:
            #         expr = expr + chr(708) + r[i-1]
            if r[i] == chr(709):
                if(r[i-1] == chr(707)):
        
                    sub = r[par.pop():i]
                    subl = len(sub)-1
                    expr = expr[:-subl]
                    expr = expr + sub
                    expr = expr  +  chr(741) + 'ε'+chr(707)
                else:
                    letra = expr[-1]
                    expr = expr[:-1]
                    expr = expr + chr(706) + letra + chr(741) + 'ε'+chr(707)
            else:
                expr = expr + r[i]
            i+=1

        return expr


    # Metodo que agrega el valor de . a la expresion
# para facilitar la lectura de la concatenacion
    def add_concat(self,expresion):
        new_word = ""
        operators = [chr(708),chr(741),chr(706),chr(709)]
        cont = 0
        while cont < len(expresion):
            if cont+1 >= len(expresion):
                new_word += expresion[-1]
                break

            if expresion[cont] == chr(708) and not (expresion[cont+1] in operators) and expresion[cont+1] != chr(707):
                new_word += expresion[cont]+chr(765)
                cont += 1
            elif expresion[cont] == chr(708) and expresion[cont+1] == chr(706):
                new_word += expresion[cont]+chr(765)
                cont += 1
            elif expresion[cont] == chr(709) and not (expresion[cont+1] in operators) and expresion[cont+1] != chr(707):
                new_word += expresion[cont]+chr(765)
                cont += 1
            elif expresion[cont] == chr(709) and expresion[cont+1] == chr(706):
                new_word += expresion[cont]+chr(765)
                cont += 1
            elif not (expresion[cont] in operators) and expresion[cont+1] == chr(707):
                new_word += expresion[cont]
                cont += 1
            elif (not (expresion[cont] in operators) and not (expresion[cont+1] in operators)) or (not (expresion[cont] in operators) and (expresion[cont+1] == chr(706))):
                new_word += expresion[cont]+chr(765)
                cont += 1
            else:
                new_word += expresion[cont]
                cont += 1
        
        return new_word
    
    #Metodo que ejecuta el AFD para analizar la produccion
    def execAFD(self):
        afd = AFD(self.res_final,self.word)
        self.resultado = afd.productions
    
    #Devuelve el resultado de la produccion, la lista con  (caracter,tipo)
    def getResult(self):
        return self.resultado


    