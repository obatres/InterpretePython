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

    def __init__(self, exp1, exp2, operador,  linea =0, columna=0) :
        self.exp1 = exp1
        self.exp2 = exp2
        self.operador = operador
        self.linea = linea
        self.columna = columna

class ExpresionNegativo(ExpresionNumerica) :
    '''
        Esta clase representa la Expresión Aritmética Negativa.
        Esta clase recibe la expresion
    '''
    def __init__(self, exp,  linea=0 , columna=0) :
        self.exp = exp
        self.linea = linea
        self.columna = columna

class ExpresionBitNot (ExpresionNumerica):
    '''
        Esta clase representa la Expresión logica bit a bit de NOT 
    '''
    def __init__(self, exp,  linea=0 , columna=0) :
        self.exp = exp
        self.linea = linea
        self.columna = columna


class ExpresionBitAnd (ExpresionNumerica):
    '''
        Esta clase representa la Expresión logica bit a bit de AND 
    '''
    def __init__(self, exp1, exp2,  linea=0 , columna=0):
        self.exp1 = exp1
        self.exp2 = exp2
        self.linea = linea
        self.columna = columna


class ExpresionBitOr (ExpresionNumerica):
    '''
        Esta clase representa la Expresión logica bit a bit de OR 
    '''
    def __init__(self, exp1, exp2,  linea=0 , columna=0):
        self.exp1 = exp1
        self.exp2 = exp2
        self.linea = linea
        self.columna = columna
 

class ExpresionBitXor (ExpresionNumerica):
    '''
        Esta clase representa la Expresión logica bit a bit de XOR 
    '''
    def __init__(self, exp1, exp2,  linea=0 , columna=0):
        self.exp1 = exp1
        self.exp2 = exp2      
        self.linea = linea
        self.columna = columna


class ExpresionBitIzq(ExpresionNumerica):
    '''
        Esta clase representa la Expresión logica bit a bit de corrimiento a la izquierda 
    '''
    def __init__(self, exp1, exp2,  linea=0 , columna=0):
        self.exp1 = exp1
        self.exp2 = exp2    
        self.linea = linea
        self.columna = columna
       

class ExpresionBitDer(ExpresionNumerica):
    '''
        Esta clase representa la Expresión logica bit a bit de corrimiento a la derecha 
    '''
    def __init__(self, exp1, exp2,  linea=0 , columna=0):
        self.exp1 = exp1
        self.exp2 = exp2 
        self.linea = linea
        self.columna = columna

class ExpresionPunteroTemp(ExpresionNumerica):
    '''
        Esta clase representa el puntero un temporal.
    '''

    def __init__(self, id ,  linea =0, columna=0) :
        self.id = id
        self.linea = linea
        self.columna = columna
 

class ExpresionConversion (ExpresionNumerica):
    '''
        Esta clase representa la conversion de tipo de un valor.
    '''

    def __init__(self, tipo , exp,  linea =0, columna=0) :
        self.tipo = tipo 
        self.exp = exp
        self.linea = linea
        self.columna = columna


class ExpresionNumero(ExpresionNumerica) :
    '''
        Esta clase representa una expresión numérica entera o decimal.
    '''

    def __init__(self, val , tipo,  linea =0, columna=0) : #AGREGAR TIPO A LA EXPRESION
        self.val = val
        self.tipo = tipo
        self.linea = linea
        self.columna = columna


class ExpresionIdentificador(ExpresionNumerica) :
    '''
        Esta clase representa un identificador.
    '''

    def __init__(self, id,  linea =0, columna =0) :
        self.id = id
        self.linea = linea
        self.columna = columna


class ExpresionPila(ExpresionNumerica):
    '''
        Esta clase representa un identificador de pila.
    '''

    def __init__(self, id ,  linea=0 , columna=0) :
        self.id = id   
        self.linea = linea
        self.columna = columna


class ExpresionPunteroPila(ExpresionNumerica):
    '''
        Esta clase representa el puntero de pila.
    '''

    def __init__(self, id ,  linea =0, columna=0) :
        self.id = id  
        self.linea = linea
        self.columna = columna

class Expresion_Pop_pila(ExpresionNumerica):
    '''
        Esta clase representa el pop de pila.
    '''

    def __init__(self, idPila, puntero,  linea=0 , columna=0) :
        self.idPila = idPila 
        self.puntero = puntero
        self.linea = linea
        self.columna = columna



class InicioArray(ExpresionNumerica):
    '''
        Esta clase representa la inicializacion de un array.
    '''
    def __init__(self, linea=0 , columna=0) :
        self.linea = linea
        self.columna = columna

class ExpresionValorAbsoluto(ExpresionNumerica):
    '''
        Esta clase representa una expresión que recibe un valor numerico y devuelve su valor absoluto
    '''
    def __init__(self, exp,  linea =0, columna=0) :
        self.exp = exp
        self.linea = linea
        self.columna = columna


class ExpresionTemporal(ExpresionNumerica) :
    '''
        Esta clase representa un temporal.
    '''

    def __init__(self, id ,  linea =0, columna=0) :
        self.id = id
        self.linea = linea
        self.columna = columna


class ExpresionCadena :
    '''
        Esta clase representa una Expresión de tipo cadena.
    '''
    def __init__(self ,  linea =0, columna=0) :
        self.linea = linea
        self.columna = columna

class ExpresionConcatenar(ExpresionCadena) :
    '''
        Esta clase representa una Expresión de tipo cadena.
        Recibe como parámetros las 2 expresiones a concatenar
    '''

    def __init__(self, exp1, exp2,  linea=0 , columna=0) :
        self.exp1 = exp1
        self.exp2 = exp2
        self.linea = linea
        self.columna = columna


class ExpresionDobleComilla(ExpresionCadena) :
    '''
        Esta clase representa una cadena entre comillas doble.
        Recibe como parámetro el valor del token procesado por el analizador léxico
    '''

    def __init__(self, val,  linea=0 , columna=0) :
        self.val = val
        self.linea = linea
        self.columna = columna

class ExpresionCadenaNumerico(ExpresionCadena) :
    '''
        Esta clase representa una expresión numérica tratada como cadena.
        Recibe como parámetro la expresión numérica
    '''
    def __init__(self, exp,  linea=0 , columna=0) :
        self.exp = exp
        self.linea = linea
        self.columna = columna

class ExpresionLogica() :
    '''
        Esta clase representa la expresión lógica.
        Esta clase recibe los operandos y el operador
    '''

    def __init__(self, exp1, exp2, operador,  linea=0 , columna=0) :
        self.exp1 = exp1
        self.exp2 = exp2
        self.operador = operador
        self.linea = linea
        self.columna = columna

class ExpresionLogicaXOR():
    '''
        Esta clase representa la expresión lógica XOR
    '''

    def __init__(self, exp1, exp2,  linea =0, columna=0) :
        self.exp1 = exp1
        self.exp2 = exp2
        self.linea = linea
        self.columna = columna

class ExpresionLogicaAND():
    '''
        Esta clase representa la expresión lógica AND
    '''

    def __init__(self, exp1, exp2,  linea =0, columna=0) :
        self.exp1 = exp1
        self.exp2 = exp2
        self.linea = linea
        self.columna = columna

class ExpresionLogicaOR():
    '''
        Esta clase representa la expresión lógica OR
    '''

    def __init__(self, exp1, exp2,  linea =0, columna=0) :
        self.exp1 = exp1
        self.exp2 = exp2
        self.linea = linea
        self.columna = columna

class ExpresionLogicaNot ():
    '''
        Esta clase representa la expresión lógica.
        Esta clase recibe el operando NOT y el operador
    '''

    def __init__(self, exp,  linea =0, columna=0) :
        self.exp = exp
        self.linea = linea
        self.columna = columna

class Expresion_param(ExpresionNumerica):
    '''
        Esta clase representa la expresión parametro, ra o valor de retorno
    '''

    def __init__(self, id,  linea =0, columna=0) :
        self.id = id
        self.linea = linea
        self.columna = columna

class AccesoValorArray(ExpresionNumerica):
    '''
        Esta clase representa la expresión que accede a un valor de un arreglo declarado
    '''

    def __init__(self, id, lista,  linea=0 , columna=0) :
        self.id = id
        self.lista = lista
        self.linea = linea
        self.columna = columna
