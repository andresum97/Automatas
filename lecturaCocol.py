import re

#Validaciones
# 0: SetDecl = ident '='Set.
# 1: KeywordDecl = ident '=' string.
# 2: Es un encabezado
# 3: TokenDecl = ident ['='TokenExpr]["EXCEPT KEYWORDS"] '.'.

#========= Pendientes
# Considerar tambien que no es buena idea borrar las "" debido que pueden ser utiles al momento de eliminar
# hacer los cambios en los Characters
# Ya funciona + o -  en characters, ahora ya puedes ver lo los tokens
# Ver el regex del TokenDecl
# Cambiar validacion de char!!! para que tenga chr()

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
            expresion_final = ""
            fin_expr = False
            for line in lines:

                if flag:
                    if line != "\n":
                        line = line.lstrip()
                        expresion_final += line
                        # expresion_final = " ".join(expresion_final.split())
                        if expresion_final.endswith("."):
                            fin_expr = True
                        else:
                            keys, error = self.Validator(expresion_final,[2])
                            if(keys):
                                print("Encontro un encabezado")
                                flag = False
                                break

                
                    if fin_expr:
                        valid,error = self.Validator(expresion_final,[0])
                        print("Line->",expresion_final)
                        if valid and not(error):
                            index = expresion_final.find('=')
                            key = expresion_final[0:index].strip()
                            value = expresion_final[index+1:-1].strip().replace('"','').replace('.','')
                            self.characters[key] = value
                        elif not(valid) and not(error):
                            print("Pudo encontrar un encabezado")
                            keys, error = self.Validator(expresion_final,[2])
                            print("Keys",keys)
                            if(keys):
                                print("Ingreso al if")
                                flag = False
                                break
                            else:
                                print("Encontro una expresion no valida")
                        elif error:
                            print("La expresion no es valida")

                        expresion_final = ""
                        fin_expr = False

                if 'CHARACTERS' in line:
                    flag = True
                    expresion_final = ""
        
        #Para trabajar con el mayor len de llave al momento de hacer sustituciones
        for key in sorted(self.characters, key=len, reverse=True):
            for keyValue,value in self.characters.items():
                self.characters[keyValue] = self.characters[keyValue].replace(key,self.characters[key])
        
        #Reemplazo de + o -, para unir o eliminar caracteres
        for keyValue,value in self.characters.items():
            while self.characters[keyValue].find('-') > -1:
                temp_index = self.characters[keyValue].find('-')
                if str(self.characters[keyValue]).find('+',temp_index+1) > -1:
                    next_index = str(self.characters[keyValue]).find('+',temp_index+1)
                elif str(self.characters[keyValue]).find('-',temp_index+1) > -1:
                    next_index = str(self.characters[keyValue]).find('-',temp_index+1)
                else:
                    next_index = -1
                first_element = str(self.characters[keyValue])[:temp_index]
                if next_index > -1:
                    second_element = str(self.characters[keyValue])[temp_index+1:next_index]
                    cont_word = str(self.characters[keyValue])[next_index:]
                    # print("cont_word->",cont_word)
                    new_word = first_element.translate({ord(i): None for i in second_element})
                    self.characters[keyValue] = new_word+cont_word
                else:
                    # print("Entro al else")
                    second_element = str(self.characters[keyValue])[temp_index+1:]
                    new_word = first_element.translate({ord(i): None for i in second_element})
                    self.characters[keyValue] = new_word

                # print("New word -> "+self.characters[keyValue])

                # print("Temp index -> ",temp_index,"; next index-> ",next_index," f_element-> ",first_element,"; s_element->",second_element)

            self.characters[keyValue] = self.characters[keyValue].replace("+","")
        

        print("Characters",self.characters)

    def readKeywords(self):
        flag = False #Para indicar que encontro Keyboards
        with open(self.filename,'r') as f:
            lines = (line.rstrip() for line in f)
            for line in lines:
                if flag and len(line.replace(" ","")) > 0:
                    valid,error = self.Validator(line,[1])
                    print("Line->",line)
                    if valid and not(error):
                        index = line.find('=')
                        key = line[0:index].strip()
                        value = line[index+1:-1].strip().replace('"','').replace('.','')
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

    def readTokens(self):
        flag = False #Para indicar que encontro TOKENS
        with open(self.filename,'r') as f:
            lines = (line.rstrip() for line in f)
            for line in lines:
                if flag and len(line.replace(" ","")) > 0:
                    valid,error = self.Validator(line,[3])
                    print("Line->",line)
                    if valid and not(error):
                        index = line.find('=')
                        key = line[0:index].strip()
                        value = line[index+1:-1].strip().replace('"','').replace('.','')
                        self.tokens[key] = value
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

                if 'TOKENS' in line:
                    flag = True

        print("Tokens",self.tokens)
                
    def tokenEvaluator(self):
        print("Evaluando los tokens")
        #Se realiza la sustitucion de characters en tokens

        #Para trabajar con el mayor len de llave al momento de hacer sustituciones
        for key in sorted(self.characters, key=len, reverse=True):
            for keyToken,value in self.tokens.items():
                #sustitucion de characters por tokens
                self.tokens[keyToken] = self.tokens[keyToken].replace(key,self.characters[key])

        print("Tokens -> ",self.tokens)



        


    def Validator(self,expr,rules):
        checked = True #Variable de respuesta
        _error = False #variable que en caso no acepte una regla, es un error sintactico
        for rule in rules:
            res = None
            #Regla que valida SetDecl
            if rule == 0:
                regex = r'[a-zA-Z].[a-zA-Z0-9]* =[\s]*"?[\W|\w]*"?[\s]*([+|-]"?[\W|\w]*"?)*\.'
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
                if expr == 'CHARACTERS' or expr == 'KEYWORDS' or expr =='TOKENS' or expr =='PRODUCTIONS':
                    checked = True
                    _error = False
                else:
                    checked = False
            
            #Regla que valida si esta leyendo un token
            elif rule == 3:
                regex = r'[a-zA-Z].[a-zA-Z0-9]* = ["?\[\W|\w]*"?|\(\[\W|\w]*\)|\[\[\W|\w]*\]|\{[\W|\w]*\}|\s*]*\.' # ["?\w*"?|\(\w*\)|\[\w*\]|\{\w*\}|\s]*\.    (FUNCIONA PARCIALMENTE)
                res = re.match(regex,expr)
                checked = res
                _error = False
            #En caso ninguna regla aplique, es porque es un error
            else:
                _error = True
            
        return checked,_error


if __name__ == "__main__":
    lec = Lectura('examplecoco.txt')
    lec.readCharacters()
    print("=======================================================")
    lec.readKeywords()
    lec.readTokens()
    lec.tokenEvaluator()