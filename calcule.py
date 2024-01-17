def calculatrice(expression):
    def precedence(operateur):
        if operateur == "+" or operateur == "-":
            return 1
        elif operateur == "*" or operateur == "/" or operateur == "%":
            return 2
        else:
            return 0

    def appliquer_operation(operateur, operandes):
        y, x = operandes.pop(), operandes.pop()
        if operateur == "+":
            operandes.append(x + y)
        elif operateur == "-":
            operandes.append(x - y)
        elif operateur == "*":
            operandes.append(x * y)
        elif operateur == "/":
            operandes.append(x / y)
        elif operateur == "%":
            operandes.append(x % y)

    pile_operateurs = []
    pile_operandes = []

    elements = expression.split()

    for element in elements:
        if element.isdigit() or (element[0] == '-' and element[1:].isdigit()):
            pile_operandes.append(float(element))
        elif element == "(":
            pile_operateurs.append(element)
        elif element == ")":
            while pile_operateurs and pile_operateurs[-1] != "(":
                appliquer_operation(pile_operateurs.pop(), pile_operandes)
            pile_operateurs.pop()  # Pop "("
        else:
            while pile_operateurs and precedence(pile_operateurs[-1]) >= precedence(element):
                appliquer_operation(pile_operateurs.pop(), pile_operandes)
            pile_operateurs.append(element)

    while pile_operateurs:
        appliquer_operation(pile_operateurs.pop(), pile_operandes)

    return pile_operandes[0]

# # Exemples d'utilisation :
# expression1 = "3 + 5 * ( 2 - 8 ) / 4"
# expression2 = "2 * ( 5 + 7 )"
# expression3 = "( 4 - 2 ) * ( 7 / ( 2 + 3 ) )"

# resultat1 = calculatrice(expression1)
# resultat2 = calculatrice(expression2)
# resultat3 = calculatrice(expression3)

# print("Résultat 1:", resultat1)
# print("Résultat 2:", resultat2)
# print("Résultat 3:", resultat3)
