#Clase de hoja de arbol

class Leaf():
    def __init__(self,id,value=None,parent=None,id_value=None,children=[]):
        self.id = id
        self.id_value = id_value
        self.value = value
        self.parent = parent
        self.children = children

    def get_id(self):
        return self.id

    def get_value(self):
        return self.value

    def get_parent(self):
        return self.parent

    def set_parent(self,parent):
        self.parent = parent

    def get_children(self):
        return self.children

    def set_children(self,val):
        self.children.append(val)

    def get_idValue(self):
        return self.id_value