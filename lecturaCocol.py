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
# Quitar del Any las comillas y la apostrofe. 
# Preguntar lo de reemplazar o hacer el cambio

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
        with open(self.filename,'r',encoding='utf-8') as f:
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
                            value = expresion_final[index+1:-1].strip() #quitaste el remove de este simbolo ""
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
        

        # print('Characters original->',self.characters)
        for key,value in self.characters.items():
            self.characters[key] = self.comillasValidator(value) 

        # print("Comillas cambiadas ",self.characters)
        #Para manejar los chars
        for key,value in self.characters.items():
            self.characters[key] = self.charValidator(value)

        for key,value in self.characters.items():
            self.characters[key] = self.anyValidator(value)

        # print("Characters luego de manejar chars",self.characters)

        

        #Para trabajar con el mayor len de llave al momento de hacer sustituciones
        for key in sorted(self.characters, key=len, reverse=True):
            for keyValue,value in self.characters.items():
                self.characters[keyValue] = self.characters[keyValue].replace(key,self.characters[key])

        # print("Caracteres sustituidos: ",self.characters)
        
        #Reemplazo de + o -, para unir o eliminar caracteres
        for keyValue,value in self.characters.items():

            check = True #Termino de recorrer la palabra
            flag = False #Para indicar si esta en un string o no
            cont = 0 #Contador de digito
            respuesta = ""
            primera = False
            primer = ""
            segunda = ""
            operador = ""
            calculo = False

            if value.find("+") > -1 or value.find("-") > -1: #Si no posee estos simbolos no vale la pena hacer cambios
                while cont < len(value): #Mientras siga revisando
                    if not(primera): #Encontro la primera palabra, entonces esta es la que hay que calcular
                        if value[cont] == chr(1000):
                            flag = not(flag)

                        if flag: #Es la primera palabra
                            primer += value[cont]
                        else: #Ya termino de guardar la primera palabra
                            respuesta = primer[1:]
                            primera = True

                    else: #Ya guardo la primera entonces ahora ya puedo calcular lo que vaya encontrando
                        if value[cont] == chr(1000):
                            flag = not(flag)

                        if (not(flag) and value[cont] == "+") or (not(flag) and value[cont] == "-"): #Si encuentra un operador
                            operador = value[cont]
                        else:
                            if flag: #Guardando el segundo valor
                                segunda += value[cont]
                            else: #Ya realizara el calculo
                                if operador == "+" and not(flag): #Si el operador es suma
                                    segunda = segunda[1:]
                                    respuesta = respuesta+segunda
                                    calculo = True
                                elif operador == "-" and not(flag): #Si el operador es resta
                                    segunda = segunda[1:]
                                    respuesta = respuesta.translate({ord(i): None for i in segunda})
                                    calculo = True

                                if calculo:
                                    op = ""
                                    segunda = ""




                    cont += 1
                
                self.characters[keyValue] = chr(1000)+respuesta+chr(1000)




            ### INTENTO 3 CON  findall
            # sentence = value
            # newValue = ""
            # cont = 0
            # res = ""
            # contString = 0
            # notString = True
            # check = True

            # _wordsString = re.findall(r'\"(.*?)\"',sentence)
            # if len(_wordsString) > 1: #Para indicar si solamente es una palabra o si hay operaciones
            #     while check:
            #         primer =  _wordsString[0]
            #         op = sentence[len(primer)+3] if cont == 0 else sentence[len(primer)+1]
            #         segundo = _wordsString[1]
            #         if op == '+':
            #             res = primer+segundo
            #         elif op == '-':
            #             res = primer.translate({ord(i): None for i in segundo})
                    
            #         if len(_wordsString) == 2: #Si ya solo quedan dos valores
            #             sentence = '"'+res+'"'
            #             check = False
            #         else:
            #             cont = len(primer)+len(segundo)+5
            #             sentence = '"'+res+sentence[cont:]
            #             _wordsString = re.findall(r'\"(.*?)\"',sentence)
                    
            #         cont += 1

            #     self.characters[keyValue] = sentence

            #==============================================================================

            # for letter in sentence:
            #     if letter == '"':
            #         notString = not(notString)
            #     if notString and letter == '-':
            #         temp_index = sentence.find('-',cont) 
            #         if str(sentence).find('+',temp_index+1) > -1:
            #             next_index = str(sentence).find('+',temp_index+1)
            #         elif str(sentence).find('-',temp_index+1) > -1:
            #             next_index = str(sentence).find('-',temp_index+1)
            #         else:
            #             next_index = -1
            #         first_element = sentence[:temp_index]
            #         if next_index > -1:
            #             second_element = str(sentence)[temp_index+1:next_index]
            #             cont_word = str(sentence)[next_index:]
            #             new_word = first_element.translate({ord(i): None for i in second_element})
            #             sentence = new_word+cont_word
            #         else:
            #             second_element = str(sentence)[temp_index+1:]
            #             new_word = first_element.translate({ord(i): None for i in second_element})
            #             sentence = new_word
            #TE QUEDASTE AQUI!!! ESTAS ARREGLANDO LO DEL -  PARA QUE NO SE CUMPLA SI ESTA DENTRO DE ""

            #     cont += 1

            # self.characters[keyValue] = sentence

            
            # esto funcionaba antes
            
            # while self.characters[keyValue].find('-') > -1:
            #     temp_index = self.characters[keyValue].find('-')
            #     if str(self.characters[keyValue]).find('+',temp_index+1) > -1:
            #         next_index = str(self.characters[keyValue]).find('+',temp_index+1)
            #     elif str(self.characters[keyValue]).find('-',temp_index+1) > -1:
            #         next_index = str(self.characters[keyValue]).find('-',temp_index+1)
            #     else:
            #         next_index = -1
            #     first_element = str(self.characters[keyValue])[:temp_index]
            #     if next_index > -1:
            #         second_element = str(self.characters[keyValue])[temp_index+1:next_index]
            #         cont_word = str(self.characters[keyValue])[next_index:]
            #         new_word = first_element.translate({ord(i): None for i in second_element})
            #         self.characters[keyValue] = new_word+cont_word
            #     else:
            #         second_element = str(self.characters[keyValue])[temp_index+1:]
            #         new_word = first_element.translate({ord(i): None for i in second_element})
            #         self.characters[keyValue] = new_word

                # print("New word -> "+self.characters[keyValue])

                # print("Temp index -> ",temp_index,"; next index-> ",next_index," f_element-> ",first_element,"; s_element->",second_element)

            # self.characters[keyValue] = self.characters[keyValue].replace("+","")
        

        print("Characters",self.characters)

    def readKeywords(self):
        flag = False #Para indicar que encontro Keyboards
        with open(self.filename,'r') as f:
            lines = (line.rstrip() for line in f)
            for line in lines:
                if flag and len(line.replace(" ","")) > 0:
                    valid,error = self.Validator(line,[1])
                    # print("Line->",line)
                    if valid and not(error):
                        index = line.find('=')
                        key = line[0:index].strip()
                        value = line[index+1:-1].strip().replace('"','').replace('.','')
                        self.keywords[key] = value
                    elif not(valid) and not(error):
                        # print("Pudo encontrar un encabezado")
                        keys, error = self.Validator(line,[2])
                        # print("Keys",keys)
                        if(keys):
                            # print("Ingreso al if")
                            flag = False
                            break
                        else:
                            print("Encontro una expresion no valida")
                    elif error:
                        print("La expresion no es valida")

                if 'KEYWORDS' in line:
                    flag = True

        print("Keywords",self.keywords)

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
                                # print("Encontro un encabezado")
                                flag = False
                                break

                if fin_expr:
                    valid,error = self.Validator(expresion_final,[3])
                    # print("Line->",expresion_final)
                    if valid and not(error):
                        index = expresion_final.find('=')
                        key = expresion_final[0:index].strip()
                        value = expresion_final[index+1:-1].strip()
                        # value = value[:-1]
                        self.tokens[key] = value
                    elif not(valid) and not(error):
                        # print("Pudo encontrar un encabezado")
                        keys, error = self.Validator(expresion_final,[2])
                        # print("Keys",keys)
                        if(keys):
                            # print("Ingreso al if")
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
            temp = chr(1000)+"("
            cont = 0
            expr = value.replace(chr(1000),'')
            for letter in expr:
                temp += letter+'|' if cont < len(expr)-1 else letter
                cont += 1
            
            self.characters[key] = temp+")"+chr(1000)
                
    def tokenEvaluator(self):
        print("======= Evaluando los tokens =========")
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
            _notString = False
            cont = 0
            while cont < len(word): 
                letter = word[cont]
                if letter == chr(1000):
                    _notString = not(_notString)
                
                if _notString:
                    new_word += letter
                else:
                    if letter == "{":
                        new_word += '('
                        # print("Ingreso al primer if")
                        # word = word[:index]+'('+word[index+1:]
                    elif letter == "}":
                        new_word += ')*'
                    elif letter == '[':
                        new_word += '('
                    elif letter == ']':
                        new_word += ')?'
                    else:
                        new_word += letter
                    #     # print("Ingreso al segundo if")
                    #     word += word[:index]+')*'+word[index+1:]
                    # index += 1
                cont += 1
            
            self.tokens[key] = new_word.replace(chr(1000),'')

        print("Token ya con cerradura -> ",self.tokens)
            
    #Genera los caracteres de c1 a c2
    def char_range(self,c1, c2):
        for c in range(ord(c1), ord(c2)+1):
            yield chr(c)

    #Valida la expresion tenga char o ..
    def charValidator(self, expresion):
        #Hay que validar si la expresion tiene chars
        respuesta = ''
        temp = ''
        #Formato de chars 'A' .. 'Z' | CHR(0) .. CHR(50)
        if expresion.find("..") > -1:
            index = expresion.find("..")
            primer = expresion[:index].rstrip().lstrip()
            segundo = expresion[index+2:].rstrip().lstrip()
            val1 = chr(int(primer[4:-1])) if primer.find('CHR(') == 0 else primer.replace("'","")
            val2 = chr(int(segundo[4:-1])) if segundo.find('CHR(') == 0 else segundo.replace("'","")
            for x in self.char_range(val1,val2):
                respuesta += x
            respuesta = chr(1000)+respuesta+chr(1000)
        else:
            for letter in expresion:
                if letter == "'":
                    temp += chr(1000)
                else:
                    temp += letter

            respuesta = temp
            #En caso solo haya que revisar y reemplazar CHR()
            if respuesta.find('CHR(') > -1:
                temp = respuesta
                while temp.find('CHR(') > -1:
                    inicio = temp.find('CHR(')
                    final = temp.find(')',inicio)
                    valor = chr(int(temp[inicio+4:final]))
                    temp = temp[:inicio]+chr(1000)+valor+chr(1000)+temp[final+1:]
                respuesta = temp #if temp != '"' else temp
            # else:
            #     #En caso no encuentre ningun CHR() o '..'
            #     respuesta = expresion

        # for letter in respuesta:
        #     if letter == "'":
        #         temp += chr(1000)
        #     else:
        #         temp += letter
        # respuesta = temp

            # _wordsString = re.findall(r"\'(.*?)\'",respuesta)



        return respuesta
            
    def anyValidator(self,expresion):
        respuesta = ""
        final = ""
        if expresion.find('ANY') > -1:
            index = expresion.find("ANY")
            primer = expresion[:index].rstrip().lstrip()
            segundo = expresion[index+3:].rstrip().lstrip()
            for x in self.char_range(chr(0),chr(255)):
                respuesta += x
            final = primer+chr(1000)+respuesta+chr(1000)+segundo
        else:
            final = expresion

        return final


    def comillasValidator(self,expresion):
        respuesta = ""
        for letter in expresion:
            if letter == '"':
                respuesta += chr(1000) #Caracter especial para dividir palabras
            else:
                respuesta += letter

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
    lec.readKeywords()
    lec.readTokens()
    lec.transformCharacters()
    lec.tokenEvaluator()