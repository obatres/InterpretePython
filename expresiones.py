from enum import Enum

class OPERACION_ARITMETICA(Enum) :
    MAS = 1
    MENOS = 2
    POR = 3
    DIVIDIDO = 4
    RESIDUO = 5

class OPERACION_LOGICA(Enum) :
    MAYOR_QUE = 1
    MENOR_QUE = 2
    IGUAL = 3
    DIFERENTE = 4
    MAYORQUE = 5
    MENORQUE = 6

class ExpresionNumerica:
    '''
        Esta clase representa una expresión numérica
    '''

class ExpresionBinaria(ExpresionNumerica) :
    '''
        Esta clase representa la Expresión Aritmética Binaria.
        Esta clase recibe los operandos y el operador
    '''

    def __init__(self, exp1, exp2, operador) :
        self.exp1 = exp1
        self.exp2 = exp2
        self.operador = operador

class ExpresionNegativo(ExpresionNumerica) :
    '''
        Esta clase representa la Expresión Aritmética Negativa.
        Esta clase recibe la expresion
    '''
    def __init__(self, exp) :
        self.exp = exp
class ExpresionBitNot (ExpresionNumerica):
    '''
        Esta clase representa la Expresión logica bit a bit de NOT 
    '''
    def __init__(self, exp) :
        self.exp = exp

class ExpresionBitAnd (ExpresionNumerica):
    '''
        Esta clase representa la Expresión logica bit a bit de AND 
    '''
    def __init__(self, exp1, exp2):
        self.exp1 = exp1
        self.exp2 = exp2

class ExpresionBitOr (ExpresionNumerica):
    '''
        Esta clase representa la Expresión logica bit a bit de OR 
    '''
    def __init__(self, exp1, exp2):
        self.exp1 = exp1
        self.exp2 = exp2

class ExpresionBitXor (ExpresionNumerica):
    '''
        Esta clase representa la Expresión logica bit a bit de XOR 
    '''
    def __init__(self, exp1, exp2):
        self.exp1 = exp1
        self.exp2 = exp2      

class ExpresionBitIzq(ExpresionNumerica):
    '''
        Esta clase representa la Expresión logica bit a bit de corrimiento a la izquierda 
    '''
    def __init__(self, exp1, exp2):
        self.exp1 = exp1
        self.exp2 = exp2            

class ExpresionBitDer(ExpresionNumerica):
    '''
        Esta clase representa la Expresión logica bit a bit de corrimiento a la derecha 
    '''
    def __init__(self, exp1, exp2):
        self.exp1 = exp1
        self.exp2 = exp2 
class ExpresionPunteroTemp(ExpresionNumerica):
    '''
        Esta clase representa el puntero un temporal.
    '''

    def __init__(self, id = "") :
        self.id = id

class ExpresionConversion (ExpresionNumerica):
    '''
        Esta clase representa la conversion de tipo de un valor.
    '''

    def __init__(self, tipo , exp) :
        self.tipo = tipo 
        self.exp = exp

class ExpresionNumero(ExpresionNumerica) :
    '''
        Esta clase representa una expresión numérica entera o decimal.
    '''

    def __init__(self, val = 0, tipo=0) : #AGREGAR TIPO A LA EXPRESION
        self.val = val
        self.tipo = tipo

class ExpresionIdentificador(ExpresionNumerica) :
    '''
        Esta clase representa un identificador.
    '''

    def __init__(self, id = "") :
        self.id = id

class ExpresionValorAbsoluto(ExpresionNumerica):
    '''
        Esta clase representa una expresión que recibe un valor numerico y devuelve su valor absoluto
    '''
    def __init__(self, exp) :
        self.exp = exp

class ExpresionTemporal(ExpresionNumerica) :
    '''
        Esta clase representa un temporal.
    '''

    def __init__(self, id = "") :
        self.id = id

class ExpresionCadena :
    '''
        Esta clase representa una Expresión de tipo cadena.
    '''

class ExpresionConcatenar(ExpresionCadena) :
    '''
        Esta clase representa una Expresión de tipo cadena.
        Recibe como parámetros las 2 expresiones a concatenar
    '''

    def __init__(self, exp1, exp2) :
        self.exp1 = exp1
        self.exp2 = exp2

class ExpresionDobleComilla(ExpresionCadena) :
    '''
        Esta clase representa una cadena entre comillas doble.
        Recibe como parámetro el valor del token procesado por el analizador léxico
    '''

    def __init__(self, val) :
        self.val = val

class ExpresionCadenaNumerico(ExpresionCadena) :
    '''
        Esta clase representa una expresión numérica tratada como cadena.
        Recibe como parámetro la expresión numérica
    '''
    def __init__(self, exp) :
        self.exp = exp

class ExpresionLogica() :
    '''
        Esta clase representa la expresión lógica.
        Esta clase recibe los operandos y el operador
    '''

    def __init__(self, exp1, exp2, operador) :
        self.exp1 = exp1
        self.exp2 = exp2
        self.operador = operador
class ExpresionLogicaXOR():
    '''
        Esta clase representa la expresión lógica XOR
    '''

    def __init__(self, exp1, exp2) :
        self.exp1 = exp1
        self.exp2 = exp2

class ExpresionLogicaAND():
    '''
        Esta clase representa la expresión lógica AND
    '''

    def __init__(self, exp1, exp2) :
        self.exp1 = exp1
        self.exp2 = exp2

class ExpresionLogicaOR():
    '''
        Esta clase representa la expresión lógica OR
    '''

    def __init__(self, exp1, exp2) :
        self.exp1 = exp1
        self.exp2 = exp2

class ExpresionLogicaNot ():
    '''
        Esta clase representa la expresión lógica.
        Esta clase recibe el operando NOT y el operador
    '''

    def __init__(self, exp) :
        self.exp = exp

