# Metodo que agrega el valor de . a la expresion
# para facilitar la lectura de la concatenacion
def ingresar_concatenacion(expresion):
    new_word = ""
    operators = ['*','|','(','?']
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