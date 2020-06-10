class Instruccion:
    '''This is an abstract class'''

class Imprimir(Instruccion) :
    '''
        Esta clase representa la instrucción imprimir.
        La instrucción imprimir únicamente tiene como parámetro una cadena
    '''

    def __init__(self,  exp) :
        self.exp = exp

class Mientras(Instruccion) :
    '''
        Esta clase representa la instrucción mientras.
        La instrucción mientras recibe como parámetro una expresión lógica y la lista
        de instrucciones a ejecutar si la expresión lógica es verdadera.
    '''

    def __init__(self, expLogica, instrucciones = []) :
        self.expLogica = expLogica
        self.instrucciones = instrucciones

class Definicion(Instruccion) :
    '''
        Esta clase representa la instrucción de definición de variables.
        Recibe como parámetro el nombre del identificador a definir
    '''

    def __init__(self, id) :
        self.id = id

class Asignacion(Instruccion) :
    '''
        Esta clase representa la instrucción de asignación de variables
        Recibe como parámetro el identificador a asignar y el valor que será asignado.
    '''

    def __init__(self, id, expNumerica) :
        self.id = id
        self.expNumerica = expNumerica

class If(Instruccion) : 
    '''
        Esta clase representa la instrucción if.
        La instrucción if recibe como parámetro una expresión lógica y la lista
        de instrucciones a ejecutar si la expresión lógica es verdadera.
    '''

    def __init__(self, expLogica, instrucciones = []) :
        self.expLogica = expLogica
        self.instrucciones = instrucciones

class IfElse(Instruccion) : 
    '''
        Esta clase representa la instrucción if-else.
        La instrucción if-else recibe como parámetro una expresión lógica y la lista
        de instrucciones a ejecutar si la expresión lógica es verdadera y otro lista de instrucciones
        a ejecutar si la expresión lógica es falsa.
    '''

    def __init__(self, expLogica, instrIfVerdadero = [], instrIfFalso = []) :
        self.expLogica = expLogica
        self.instrIfVerdadero = instrIfVerdadero
        self.instrIfFalso = instrIfFalso

class Unset(Instruccion):
    '''
        Esta clase representa la instrucción unset.
        La instrucción unset únicamente tiene como parámetro un registro
    '''

    def __init__(self,  exp) :
        self.exp = exp    

class ErrorSin(Instruccion):
    '''
        Esta clase representa la instrucción error sintactico.
        La instrucción unset únicamente tiene como parámetro un registro
    '''
    '''
    def __init__(self,  exp) :
        self.exp = exp  '''    

class IniciaPila (Instruccion):
    '''
        Inicia una pila
    '''
    def __init__(self,  id) :
        self.id = id  

class AsignaPunteroPila(Instruccion):
    '''
        Asigna puntero de  una pila
    '''
    def __init__(self,  id, exp) :
        self.id = id 
        self.exp = exp 

class AsignaValorPila(Instruccion):
    '''
        Asigna un valor a una posicion de  una pila
    '''
    def __init__(self,  id, exp, puntero) :
        self.id = id 
        self.exp = exp
        self.puntero = puntero 

class AsignacionExtra(Instruccion):
    '''
        Asigna un valor a un registro parametro, ra y retorno
    '''
    def __init__(self,  id, exp) :
        self.id = id 
        self.exp = exp

class Main (Instruccion):
    '''
        Nodo de tipo main
   
    '''

class Asigna_arreglo(Instruccion):
    '''
        Nodo de tipo asignacion de arreglo
   
    '''
    def __init__(self,id,lista,exp) :
        self.id = id 
        self.lista = lista
        self.exp = exp

class Label(Instruccion):
    '''
        Nodo de tipo Label
   
    '''
    def __init__(self,id) :
        self.id = id 

class Goto(Instruccion):
    '''
        Nodo de tipo Label
   
    '''
    def __init__(self,id) :
        self.id = id 

class Exit():
    '''
        Nodo de tipo Exit
   
    '''
