from graphviz import Digraph
import ast

class Subconjuntos:
    def __init__(self, estados, simbolos, inicio, final, transicion):
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
        if not(type(val_ele) == list):
            values.append(val_ele)
            for val in values:
                for element in self.transitions:
                    if element[0] == val and element[1] =='ε':
                        values.append(element[2])
            values.sort()
            self.all_states[str(values)] = 'S0'
            self.all_states_list.append(values)
        else:
            values = val_ele.copy() #[2]
            for val in values:
                for element in self.transitions:
                    if element[0] == val and element[1] =='ε':
                        values.append(element[2])

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
        print('Closure-e: ',values,' -> Estado:',state)

        return state

    def move(self,_list,sym):
        values = _list.copy()
        res = []
        for val in values:
            for element in self.transitions:
                if element[0] == val and element[1] == sym:
                    res.append(element[2])

        res = list(dict.fromkeys(res))
        print("Resultado mov con simbolo",sym, '->',res)

        # if(not(str(values) in self.all_states)):
        #     num = str(len(self.all_states.keys())+1)
        #     self.all_states[str(values)] = 'S'+num

        return res
            

        # values = list(dict.fromkeys(values))
        # print('Values',values)


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

