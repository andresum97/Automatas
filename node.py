#Clase de nodo


class Node:
    def __init__(self,id,transitions = []):
        self.id = id
        self.transitions = transitions

    def get_transitions(self):
        return self.transitions

    def set_transitions(self,element):
        self.transitions.append(element)
