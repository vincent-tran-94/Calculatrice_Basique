import math

def calculatrice(expression):
    # Remplacer le symbole '√' par 'math.sqrt'
    expression = expression.replace('√', 'math.sqrt')
    expression = expression.replace('^', '**')
    

    try:
        result = eval(expression, {'__builtins__': None, 'math': math, 'sin': math.sin, 'cos': math.cos, 'tan': math.tan})
        return result
    except Exception as e:
        return str(e)
    
class Converter:
    @staticmethod
    def binary_to_hexadecimal(binary):
        return str(hex(int(binary, 2))[2:].upper())

    @staticmethod
    def binary_to_decimal(binary):
        return str(int(binary, 2))

    @staticmethod
    def decimal_to_binary(decimal):
        return str(bin(decimal)[2:])

    @staticmethod
    def decimal_to_hexadecimal(decimal):
        return str(hex(decimal)[2:].upper())

    @staticmethod
    def hexadecimal_to_binary(hexadecimal):
        return str(bin(int(hexadecimal, 16))[2:])

    @staticmethod
    def hexadecimal_to_decimal(hexadecimal):
        return str(int(hexadecimal, 16))

# # Exemple d'utilisation :
converter = Converter()

# binary = "101010"
# hexadecimal = converter.binary_to_hexadecimal(binary)
# print(f"Binaire {binary} en hexadécimal : {hexadecimal}")

# binary = "101010"
# decimal = converter.binary_to_decimal(binary)
# print(f"Binaire {binary} en décimal : {decimal}")

# decimal = 42
# binary = converter.decimal_to_binary(decimal)
# print(f"Décimal {decimal} en binaire : {type(binary)}")

# decimal = 42
# hexadecimal = converter.decimal_to_hexadecimal(decimal)
# print(f"Décimal {decimal} en hexadécimal : {hexadecimal}")

# hexadecimal = "2A"
# binary = converter.hexadecimal_to_binary(hexadecimal)
# print(f"Hexadécimal {hexadecimal} en binaire : {binary}")

# hexadecimal = "2A"
# decimal = converter.hexadecimal_to_decimal(hexadecimal)
# print(f"Hexadécimal {hexadecimal} en décimal : {decimal}")





    
# def calculatrice(expression):
#     def precedence(operateur):
#         if operateur == "+" or operateur == "-":
#             return 1
#         elif operateur == "*" or operateur == "/" or operateur == "%":
#             return 2
#         else:
#             return 0

#     def appliquer_operation(operateur, operandes):
#         y, x = operandes.pop(), operandes.pop()
#         if operateur == "+":
#             operandes.append(x + y)
#         elif operateur == "-":
#             operandes.append(x - y)
#         elif operateur == "*":
#             operandes.append(x * y)
#         elif operateur == "/":
#             operandes.append(x / y)
#         elif operateur == "%":
#             operandes.append(x % y)

#     pile_operateurs = []
#     pile_operandes = []

#     elements = expression.split()

#     for element in elements:
#         if element.isdigit() or (element[0] == '-' and element[1:].isdigit()):
#             pile_operandes.append(float(element))
#         elif element == "(":
#             pile_operateurs.append(element)
#         elif element == ")":
#             while pile_operateurs and pile_operateurs[-1] != "(":
#                 appliquer_operation(pile_operateurs.pop(), pile_operandes)
#             pile_operateurs.pop()  # Pop "("
#         else:
#             while pile_operateurs and precedence(pile_operateurs[-1]) >= precedence(element):
#                 appliquer_operation(pile_operateurs.pop(), pile_operandes)
#             pile_operateurs.append(element)

#     while pile_operateurs:
#         appliquer_operation(pile_operateurs.pop(), pile_operandes)

#     return pile_operandes[0]