from graphviz import Digraph
import ast
import json

class Subconjuntos:
    def __init__(self, estados, simbolos, inicio, final, transicion,word):
        self.word = word
        self.states = estados
        self.symbols = simbolos
        self.initial = inicio
        self.final = final
        self.transitions = transicion
        self.all_states = {}
        self.all_states_list = []
        self.routes = []
        self.states_final = []
        self.e_closure(self.initial)
        self.process()

    def e_closure(self,val_ele):
        values = []
        state = ""
        visited = []
        if not(type(val_ele) == list):
            values.append(val_ele)
            values = list(dict.fromkeys(values))
            for val in values:
                for element in self.transitions:
                    if element[0] == val and element[1] =='ε' and element[2] not in visited:
                        values.append(element[2])
                        visited.append(element[2])
            values.sort()
            self.all_states[str(values)] = 'S0'
            self.all_states_list.append(values)
        else:
            values = val_ele.copy() #[2]
            for val in values:
                for element in self.transitions:
                    if element[0] == val and element[1] =='ε' and element[2] not in visited:
                        values.append(element[2])
                        visited.append(element[2])

            values.sort()

            if(not(str(values) in self.all_states)):
                num = str(len(self.all_states.keys()))
                self.all_states[str(values)] = 'S'+num
                state = 'S'+num
                self.all_states_list.append(values)
            else:
                state = self.all_states[str(values)]

            try:
                if(values.index(self.final) > -1):
                    self.states_final.append(state)
            except:
                pass

        


        values = list(dict.fromkeys(values))
        # print('Closure-e: ',values,' -> Estado:',state)

        return state

    def move(self,_list,sym):
        values = _list.copy()
        res = []
        for val in values:
            for element in self.transitions:
                if element[0] == val and element[1] == sym:
                    res.append(element[2])

        res = list(dict.fromkeys(res))
        # print("Resultado mov con simbolo",sym, '->',res)

        # if(not(str(values) in self.all_states)):
        #     num = str(len(self.all_states.keys())+1)
        #     self.all_states[str(values)] = 'S'+num

        return res
            

        # values = list(dict.fromkeys(values))
        # print('Values',values)

    def getValuesState(self,val):
        key_list = list(self.all_states.keys())
        val_list = list(self.all_states.values())

        position = val_list.index(val)

        return json.loads(key_list[position])

    def Simulacion(self,inicio):
        _state = 'S0'
        _isValid = True
        _isInSymbol = True
        for c in self.word:
            if not(_isValid):
                break
            if c not in self.symbols:
                _isInSymbol = False
            for t in self.routes:
                if t[0] == _state and t[1] == c:
                    _state = t[2]
                    _isValid = True
                    break
                else:
                    _isValid = False
                    

        # S = inicio
        # cont = 0
        # for c in self.word:
        #     S = self.move(S,c)
        
        # for i in self.states_final:
        #     #_temp = self.getValuesState(i)
        #     if(i in S):
        #         cont+=1
        
        if(_state in self.states_final and _isInSymbol == True):
            print("""
            *******************************
            SI en Subconjuntos
            ********************************
            """)
        else:
            print("""
            *******************************
            NO en Subconjuntos
            ********************************
            """)

    def process(self):
        for key in self.all_states_list:
            for letter in self.symbols:
                res_mov = self.move(key,letter)
                if len(res_mov) > 0:
                    state = self.e_closure(res_mov)
                    self.routes.append((self.all_states[str(key)],letter,state))
                    #print("Estado",self.all_states[key],' - simbolo - ',letter,'lleva a ',state)

        self.states_final = list(dict.fromkeys(self.states_final))
        # print("Todos los estados ",self.all_states)
        # print("Rutas ",self.routes)
        # print("Nodos finales ",self.states_final)
        # print("Final",self.final)

        #====== Para graficar DFA
        f = Digraph('finite_state_machine', filename='DFA_subconjuntos.gv')
        f.attr(rankdir='LR', size='8,5')
        f.attr('node', shape='doublecircle')
        for finals in self.states_final:
            f.node(finals)
        f.attr('node',shape="circle")
        for element in self.routes:
            f.edge(element[0],element[2],label=str(element[1]))

        f.view()


        print("======= Resultados Subconjuntos ========")
        print("Estados => ",self.all_states.values())
        print("Simbolos => ",self.symbols)
        print("Inicio => ",'S0')
        print("Aceptacion => ",self.states_final)
        print("Transicion => ", self.routes)

        cadena = f'''
        ============= RESULTADOS DE SUBCONJUNTOS ==========
        Estados => {self.all_states.values()}
        Simbolos => {self.symbols}
        Inicio => S0
        Aceptacion => {self.states_final}
        Transicion => {self.routes}
        '''
        # print(cadena)
        with open('resultados_subconjuntos.txt',"w",encoding="utf-8") as f:
            f.write(cadena)
        f.close()

        s0 = self.getValuesState('S0')
        self.Simulacion(s0)