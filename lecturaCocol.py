import re

#Validaciones
# 0: SetDecl = ident '='Set.
# 1: KeywordDecl = ident '=' string.
# 2: Es un encabezado
# 3: TokenDecl = ident ['='TokenExpr]["EXCEPT KEYWORDS"] '.'.

#========= Pendientes
# Considerar tambien que no es buena idea borrar las "" debido que pueden ser utiles al momento de eliminar
# hacer los cambios en los Characters
# Ver el regex del TokenDecl
# Arreglar simbolos de + y -

class Lectura():
    def __init__(self,_filename):
        self.filename = _filename
        self.characters = {}
        self.keywords = {}
        self.tokens = {}
        self.productions = {}
        self.exceptions = {}

    def readCharacters(self):
        flag = False #Para indicar que encontro CHARACTER
        with open(self.filename,'r') as f:
            lines = (line.rstrip() for line in f)
            expresion_final = ""
            fin_expr = False
            for line in lines:

                if flag:
                    if line != "\n": #Si no es una linea vacia
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

                
                    if fin_expr:# Si encuentra una expresion que ya cumpla con el punto y todo
                        valid,error = self.Validator(expresion_final,[0])
                        if valid and not(error):
                            index = expresion_final.find('=')
                            key = expresion_final[0:index].strip()
                            value = expresion_final[index+1:-1].strip().replace('"','')
                            # value = value[:-1]
                            self.characters[key] = value
                        elif not(valid) and not(error):
                            keys, error = self.Validator(expresion_final,[2])
                            if(keys):
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
        
        print('Characters original->',self.characters)
        #Para manejar los chars
        for key,value in self.characters.items():
            self.characters[key] = self.charValidator(value)

        print("Characters luego de manejar chars",self.characters)

        #Para trabajar con el mayor len de llave al momento de hacer sustituciones
        for key in sorted(self.characters, key=len, reverse=True):
            for keyValue,value in self.characters.items():
                self.characters[keyValue] = self.characters[keyValue].replace(key,self.characters[key])

        print("Caracteres sustituidos: ",self.characters)
        
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
                    new_word = first_element.translate({ord(i): None for i in second_element})
                    self.characters[keyValue] = new_word+cont_word
                else:
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
                    valid,error = self.Validator(expresion_final,[3])
                    print("Line->",expresion_final)
                    if valid and not(error):
                        index = expresion_final.find('=')
                        key = expresion_final[0:index].strip()
                        value = expresion_final[index+1:-1].strip()
                        # value = value[:-1]
                        self.tokens[key] = value
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

                if 'TOKENS' in line:
                    flag = True
                    expresion_final = ""

        print("Tokens",self.tokens)

    # Metodo que obtiene los | de los characters y tambien agrega los parentesis
    def transformCharacters(self):
        for key,value in self.characters.items():
            temp = "("
            cont = 0
            for letter in value:
                temp += letter+'|' if cont < len(value)-1 else letter
                cont += 1
            
            self.characters[key] = temp+")"
                
    def tokenEvaluator(self):
        print("Evaluando los tokens")
        #Se realiza la sustitucion de characters en tokens

        #Para trabajar con el mayor len de llave al momento de hacer sustituciones
        for key in sorted(self.characters, key=len, reverse=True):
            for keyToken,value in self.tokens.items():
                #sustitucion de characters por tokens
                self.tokens[keyToken] = self.tokens[keyToken].replace(key,self.characters[key])

        print("Tokens -> ",self.tokens)
        #Validar que tenga los keywords para enviar la señal

        for keyToken,value in self.tokens.items():
            if str(value).find('EXCEPT KEYWORDS') > -1:
                self.exceptions[keyToken] = True
                self.tokens[keyToken] = self.tokens[keyToken].replace(" EXCEPT KEYWORDS","")
            else:
                self.exceptions[keyToken] = False

        print("Exceptions ",self.exceptions)
        print("Tokens sin keywords -> ",self.tokens)

        #Ahora ya transforma las expresiones regulares
        #Recorrer cada letra, y si encuentra la expresion la cambia
        for key,values  in self.tokens.items():
            word = str(values)
            new_word = ""
            _notString = True
            index = 0
            for letter in word:
                if letter == '"':
                    _notString = not(_notString)
                if _notString and letter == "{":
                    print("Ingreso al primer if")
                    word = word[:index]+'('+word[index+1:]
                if _notString and letter == "}":
                    print("Ingreso al segundo if")
                    word += word[:index]+')*'+word[index+1:]
                index += 1
            
            self.tokens[key] = word

        print("Token ya con cerradura -> ",self.tokens)
            
    #Genera los caracteres de c1 a c2
    def char_range(self,c1, c2):
        for c in range(ord(c1), ord(c2)+1):
            yield chr(c)

    #Valida la expresion tenga char o ..
    def charValidator(self, expresion):
        #Hay que validar si la expresion tiene chars
        respuesta = ""
        #Formato de chars 'A' .. 'Z' | CHR(0) .. CHR(50)
        if expresion.find("..") > -1:
            index = expresion.find("..")
            primer = expresion[:index].rstrip().lstrip()
            segundo = expresion[index+2:].rstrip().lstrip()
            val1 = chr(int(primer[4:-1])) if primer.find('CHR(') == 0 else primer.replace("'","")
            val2 = chr(int(segundo[4:-1])) if segundo.find('CHR(') == 0 else segundo.replace("'","")
            for x in self.char_range(val1,val2):
                respuesta += x

        else:
            #En caso solo haya que revisar y reemplazar CHR()
            if expresion.find('CHR(') > -1:
                temp = expresion
                while temp.find('CHR(') > -1:
                    inicio = temp.find('CHR(')
                    final = temp.find(')',inicio)
                    valor = chr(int(temp[inicio+4:final]))
                    temp = temp[:inicio]+valor+temp[final+1:]
                respuesta = temp
            else:
                #En caso no encuentre ningun CHR() o '..'
                respuesta = expresion

        return respuesta
            

            

        


    def Validator(self,expr,rules):
        checked = True #Variable de respuesta
        _error = False #variable que en caso no acepte una regla, es un error sintactico
        for rule in rules:
            res = None
            #Regla que valida SetDecl
            if rule == 0:
                regex = r'[a-zA-Z].[a-zA-Z0-9]*[\s]?=[\s]*"?[\W|\w]*"?[\s]*([+|-]"?[\W|\w]*"?)*\.'
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
    lec = Lectura('examplecoco.atg')
    # print("Caracter:",lec.charValidator('eol+tab'))
    lec.readCharacters()
    # print("=======================================================")
    # lec.readKeywords()
    # lec.readTokens()
    # lec.transformCharacters()
    # lec.tokenEvaluator()