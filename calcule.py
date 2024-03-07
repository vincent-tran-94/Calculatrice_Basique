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

