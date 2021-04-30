import re

#Validaciones
# 0: SetDecl = ident '='Set.
# 1: KeywordDecl = ident '=' string.
# 2: Es un encabezado
# 3: TokenDecl = ident ['='TokenExpr]["EXCEPT KEYWORDS"] '.'.


#=============== CAMBIO PARA AUTOMATAS =========================
# '('  parentesis inicial ->   CHR(706) = '˂'
# ')'  parentesis final -> CHR(707) = '˃'
# '*'  cerradura kleene -> CHR(708) = '˄' 
# '|'  pipe de OR -> CHR(741) = '˥' listo
# '?'  interrogacion -> CHR(709) = '˅'
# '.'  concatenacion -> CHR(765) = '˽'    listo
# '+'  agregar otra cerradura -> CHR(931) = 'Σ'
# '#'  signo de finalizacion de exp -> CHR(920) = 'Θ'       listo

#========= Pendientes
# hacer los cambios en los Characters
# Ver el regex del TokenDecl
# El + y - no funcionan en el DFA! pensar en un reemplazo, al igual que con los otros caracteres especiales
# No funcionan las \t y los caracteres de espacio. En el DFA
# Probar los demas ATG
# El ANY tiene problemas con los otros signos. Puede arruinar las cosas en el DFA
# los caracteres que aparecen en la expresion regular, como parentesis, pueden llegar a ocasionar problemas



class Lectura():
    def __init__(self,_filename):
        self.filename = _filename
        self.characters = {}
        self.keywords = {}
        self.tokens = {}
        self.productions = {}
        self.exceptions = {}
        self.final_expresion = ""

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

                if 'KEYWORDS' in line and not('EXCEPT KEYWORDS.' in line):
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
                temp += letter+chr(741) if cont < len(expr)-1 else letter
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

        # print("Tokens -> ",self.tokens)
        #Validar que tenga los keywords para enviar la señal

        for keyToken,value in self.tokens.items():
            if str(value).find('EXCEPT KEYWORDS') > -1:
                self.exceptions[keyToken] = [value for value in self.keywords.values()]
                self.tokens[keyToken] = self.tokens[keyToken].replace(" EXCEPT KEYWORDS","")
            else:
                self.exceptions[keyToken] = []

        # print("Exceptions ",self.exceptions)
        # print("Tokens sin keywords -> ",self.tokens)

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
                        new_word += ')'+chr(708)
                    elif letter == '[':
                        new_word += '('
                    elif letter == ']':
                        new_word += ')?'
                    elif letter == '|':
                        new_word += chr(741)
                    else:
                        new_word += letter
                    #     # print("Ingreso al segundo if")
                    #     word += word[:index]+')*'+word[index+1:]
                    # index += 1
                cont += 1
            
            self.tokens[key] = new_word.replace(chr(1000),'')

        # print("Token ya con cerradura -> ",self.tokens)

        primero = True
        #Para devolver el gran string
        for key,values in self.tokens.items():
            if primero:
                new_word = '(('+values+')'+chr(920)+')'
            else:
                new_word = chr(741)+'(('+values+')'+chr(920)+')'
            self.final_expresion += new_word
            primero = False

        print("Final",repr(self.final_expresion))

        return repr(self.final_expresion), self.exceptions, self.tokens
            
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
    expresion_final, excepciones, tokens = lec.tokenEvaluator()


    automata_DFA = """ 
# coding=utf8
import leaf
from graphviz import Digraph
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
        self._infoLeaf = {{}}  #Key: id de nodo / value [nullable,firstpos,lastpost,followpos]
        self.all_states = {{}}
        self.list_states = []
        self.leaf_values = {{}}
        self.states_final = []
        self.routes = []
        self.last_state = []
        self.token = {tokens}
        self.excepciones = {excepciones}
        self.verification = {{}}
        self.states_tokens = {{}}
        self.states_inverse = {{}}
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
        print('Raiz',self.root.get_id())
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
        operadores = [chr(765),chr(708),')','(',chr(741)] #['.','*',')','(','|']
        # try:
        while cont < len(self.expression):
            #En el caso del | se generan 6 nodos diferentes
            # print("Caracter: ",self.expression[cont])
            if self.expression[cont] == '(':
                self.operators.append(self.expression[cont])
            elif self.expression[cont] == ')':
                while((self.operators) and self.operators[-1] != '('):
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
                print('\t' * indent + str(key))
                if isinstance(value, dict):
                    pretty(value, indent+1)
                else:
                    print('\t' * (indent+1) + str(value))

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

        print("Verificacion -> ",self.verification)
        print('Estados ->',self.all_states)

        for key,value in self.all_states.items():
            self.states_inverse[value] = key

        print('Inverso ',self.states_inverse)
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

        print("Estados de tokens->",self.states_tokens)
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
        print("Finales ",self.states_final)

        
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

    
        # self.Simulacion()
        pos = 0
        while pos < len(self.word):
            token, pos, identificador = self.simulacionTokens(self.word,pos)
            if identificador:
                acepta = True
                for exp in self.excepciones[identificador]:
                    if token == exp:
                        acepta = False
                        print('[======',repr(exp),'es el keyword', exp,' ======]')
                        break
                if acepta:
                    print("[====== El simbolo es ",repr(token),' y es de tipo ->',identificador,'======]')
            else:
                print('[======',repr(token),'es un simbolo no esperado ======]')




# Metodo que agrega el valor de . a la expresion
# para facilitar la lectura de la concatenacion
def add_concat(expresion):
    new_word = ""
    operators = [chr(708),chr(741),'(','?']
    cont = 0
    while cont < len(expresion):
        if cont+1 >= len(expresion):
            new_word += expresion[-1]
            break

        if expresion[cont] == chr(708) and not (expresion[cont+1] in operators) and expresion[cont+1] != ')':
            new_word += expresion[cont]+chr(765)
            cont += 1
        elif expresion[cont] == chr(708) and expresion[cont+1] == '(':
            new_word += expresion[cont]+chr(765)
            cont += 1
        elif expresion[cont] == '?' and not (expresion[cont+1] in operators) and expresion[cont+1] != ')':
            new_word += expresion[cont]+chr(765)
            cont += 1
        elif expresion[cont] == '?' and expresion[cont+1] == '(':
            new_word += expresion[cont]+chr(765)
            cont += 1
        elif not (expresion[cont] in operators) and expresion[cont+1] == ')':
            new_word += expresion[cont]
            cont += 1
        elif (not (expresion[cont] in operators) and not (expresion[cont+1] in operators)) or (not (expresion[cont] in operators) and (expresion[cont+1] == '(')):
            new_word += expresion[cont]+chr(765)
            cont += 1
        else:
            new_word += expresion[cont]
            cont += 1
    
    return new_word


##========================= Menu =================
def replace(r):
     #ε
    i = 0
    expr = ''
    par = []
    sub = ''
    resta = []
    while i <len(r):
        if(r[i] =='('):
            par.append(i)
        # if r[i] == '+':
            
        #     if(r[i-1] == ')'):

        #         sub = r[par.pop():i]
                
        #         expr = expr + chr(708) + sub
        #     else:
        #         expr = expr + chr(708) + r[i-1]
        if r[i] == '?':
            if(r[i-1] == ')'):
    
                sub = r[par.pop():i]
                subl = len(sub)-1
                expr = expr[:-subl]
                expr = expr + sub
                expr = expr  +  chr(741) + 'ε)'
            else:
                letra = expr[-1]
                expr = expr[:-1]
                expr = expr + '(' + letra + chr(741) + 'ε)'
        else:
            expr = expr + r[i]
        i+=1

    return expr

palabrafile = open("palabras.txt",'r',encoding='utf-8')
palabra = palabrafile.read()#input('Palabra a guardar: ')

expression = {expresion_regular}
word = palabra

res = replace(expression)
res_final = add_concat(res)
print("Nueva expresion",res_final)


# try:
afd = AFD(res_final,word)
# except:
#     print("La cadena ingresa no es válida")

    """.format(expresion_regular = expresion_final, tokens=tokens,excepciones=excepciones)

    scanner = open("scanner.py","w",encoding='utf-8')
    scanner.write(automata_DFA)
    scanner.close()

