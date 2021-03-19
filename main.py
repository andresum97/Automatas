import thompson
import subconjuntos
import AFD

# Metodo que agrega el valor de . a la expresion
# para facilitar la lectura de la concatenacion
def add_concat(expresion):
    new_word = ""
    operators = ['*','|','(','?','+']
    cont = 0
    while cont < len(expresion):
        if cont+1 >= len(expresion):
            new_word += expresion[-1]
            break

        if expresion[cont] == '*' and not (expresion[cont+1] in operators) and expresion[cont+1] != ')':
            new_word += expresion[cont]+"."
            cont += 1
        elif expresion[cont] == '*' and expresion[cont+1] == '(':
            new_word += expresion[cont]+"."
            cont += 1
        elif expresion[cont] == '?' and not (expresion[cont+1] in operators) and expresion[cont+1] != ')':
            new_word += expresion[cont]+"."
            cont += 1
        elif expresion[cont] == '?' and expresion[cont+1] == '(':
            new_word += expresion[cont]+"."
            cont += 1
        elif not (expresion[cont] in operators) and expresion[cont+1] == ')':
            new_word += expresion[cont]
            cont += 1
        elif (not (expresion[cont] in operators) and not (expresion[cont+1] in operators)) or (not (expresion[cont] in operators) and (expresion[cont+1] == '(')):
            new_word += expresion[cont]+"."
            cont += 1
        else:
            new_word += expresion[cont]
            cont += 1
    
    return new_word


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
        if r[i] == '+':
            
            if(r[i-1] == ')'):

                sub = r[par.pop():i]
                
                expr = expr + '*' + sub
            else:
                expr = expr + '*' + r[i-1]
        elif r[i] == '?':
            if(r[i-1] == ')'):
    
                sub = r[par.pop():i]
                subl = len(sub)-1
                expr = expr[:-subl]
                expr = expr + sub
                expr = expr  +  '|' + 'ε)'
            else:
                letra = expr[-1]
                expr = expr[:-1]
                expr = expr + '(' + letra + '|' + 'ε)'
        else:
            expr = expr + r[i]
        i+=1

    return expr


expression =  input("Ingresar expresion")
word = input("Ingrese palabra")

res = replace(expression)
res_final = add_concat(res)
print("Nueva expresion",res_final)


th = thompson.Thompson(res_final,word)
th_states, th_symbols, th_begin, th_end, th_transition = th.get_results()

sb = subconjuntos.Subconjuntos(th_states, th_symbols, th_begin, th_end, th_transition,word)

afd = AFD.AFD(res_final,word)


