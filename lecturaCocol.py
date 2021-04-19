import re

#Validaciones
# 0: SetDecl = ident '='Set.
# 1: KeywordDecl = ident '=' string.
# 2: Es un encabezado

class Lectura():
    def __init__(self,_filename):
        self.filename = _filename
        self.characters = {}
        self.keywords = {}
        self.tokens = {}
        self.productions = {}

    def readCharacters(self):
        flag = False #Para indicar que encontro CHARACTER
        with open(self.filename,'r') as f:
            lines = (line.rstrip() for line in f)
            for line in lines:
                if flag and len(line.replace(" ","")) > 0:
                    valid,error = self.Validator(line,[0])
                    print("Line->",line)
                    if valid and not(error):
                        index = line.find('=')
                        key = line[0:index].strip()
                        value = line[index+1:-2].strip().replace('"','')
                        self.characters[key] = value
                    elif not(valid) and not(error):
                        print("Pudo encontrar un encabezado")
                        keys, error = self.Validator(line,[2])
                        print("Keys",keys)
                        if(keys):
                            print("Ingreso al if")
                            flag = False
                            break
                        else:
                            print("Encontro una expresion no valida")
                    elif error:
                        print("La expresion no es valida")

                if 'CHARACTERS' in line:
                    flag = True

        print("Characters",self.characters)

    def readKeywords(self):
        flag = False #Para indicar que encontro CHARACTER
        with open(self.filename,'r') as f:
            lines = (line.rstrip() for line in f)
            for line in lines:
                if flag and len(line.replace(" ","")) > 0:
                    valid,error = self.Validator(line,[1])
                    print("Line->",line)
                    if valid and not(error):
                        index = line.find('=')
                        key = line[0:index].strip()
                        value = line[index+1:-2].strip().replace('"','')
                        self.keywords[key] = value
                    elif not(valid) and not(error):
                        print("Pudo encontrar un encabezado")
                        keys, error = self.Validator(line,[2])
                        print("Keys",keys)
                        if(keys):
                            print("Ingreso al if")
                            flag = False
                            break
                        else:
                            print("Encontro una expresion no valida")
                    elif error:
                        print("La expresion no es valida")

                if 'KEYWORDS' in line:
                    flag = True

        print("Keyboards",self.keywords)
                


    def Validator(self,expr,rules):
        checked = True #Variable de respuesta
        _error = False #variable que en caso no acepte una regla, es un error sintactico
        for rule in rules:
            res = None
            #Regla que valida SetDecl
            if rule == 0:
                regex = r'[a-zA-Z].[a-zA-Z0-9]* = "?\w*"?([+|-]"?\w*"?)*\.'
                res = re.match(regex,expr)
                checked = res
                _error = False
            #Regla que valida KeyboardDecl
            elif rule == 1:
                regex = r'[a-zA-Z].[a-zA-Z0-9]* = (.*).'   #"(.*)".
                res = re.match(regex,expr)
                checked = res
                _error = False
            #Regla que valida si esta leyendo de los encabezados
            elif rule == 2:
                print("Expresion en regla 1",expr)
                if expr == 'CHARACTERS' or expr == 'KEYWORDS' or expr =='TOKENS':
                    checked = True
                    _error = False
                else:
                    checked = False
            #En caso ninguna regla aplique, es porque es un error
            else:
                _error = True
            
        return checked,_error


if __name__ == "__main__":
    lec = Lectura('examplecoco.txt')
    lec.readCharacters()
    print("=======================================================")
    lec.readKeywords()