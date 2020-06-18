class Instruccion:
    '''This is an abstract class'''

class Imprimir(Instruccion) :
    '''
        Esta clase representa la instrucción imprimir.
        La instrucción imprimir únicamente tiene como parámetro una cadena
    '''

    def __init__(self,  exp, linea=0 , columna=0 ) :
        self.exp = exp
        self.linea = linea
        self.columna = columna

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

    def __init__(self, id, expNumerica,  linea=0 , columna=0) :
        self.id = id
        self.expNumerica = expNumerica
        self.linea = linea
        self.columna = columna

class If(Instruccion) : 
    '''
        Esta clase representa la instrucción if.
        La instrucción if recibe como parámetro una expresión lógica y la lista
        de instrucciones a ejecutar si la expresión lógica es verdadera.
    '''

    def __init__(self, exp, goto,  linea =0, columna=0) :
        self.exp = exp
        self.goto = goto
        self.linea = linea
        self.columna = columna

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

    def __init__(self,  exp,  linea =0, columna=0) :
        self.exp = exp    
        self.linea = linea
        self.columna = columna

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
    def __init__(self,  id,  linea =0, columna=0) :
        self.id = id  
        self.linea = linea
        self.columna = columna

class AsignaPunteroPila(Instruccion):
    '''
        Asigna puntero de  una pila
    '''
    def __init__(self,  id, exp,  linea=0 , columna=0) :
        self.id = id 
        self.exp = exp 
        self.linea = linea
        self.columna = columna

class AsignaValorPila(Instruccion):
    '''
        Asigna un valor a una posicion de  una pila
    '''
    def __init__(self,  id, exp, puntero,  linea=0 , columna=0) :
        self.id = id 
        self.exp = exp
        self.puntero = puntero 
        self.linea = linea
        self.columna = columna

class AsignacionExtra(Instruccion):
    '''
        Asigna un valor a un registro parametro, ra y retorno
    '''
    def __init__(self,  id, exp,  linea=0 , columna=0) :
        self.id = id 
        self.exp = exp
        self.linea = linea
        self.columna = columna

class Main (Instruccion):
    '''
        Nodo de tipo main
   
    '''
    def __init__(self,  linea=0 , columna=0) :
        self.linea = linea
        self.columna = columna

class Asigna_arreglo(Instruccion):
    '''
        Nodo de tipo asignacion de arreglo
   
    '''
    def __init__(self,id,lista,exp,  linea=0 , columna=0) :
        self.id = id 
        self.lista = lista
        self.exp = exp
        self.linea = linea
        self.columna = columna

class Label(Instruccion):
    '''
        Nodo de tipo Label
   
    '''
    def __init__(self,id,  linea=0 , columna=0) :
        self.id = id 
        self.linea = linea
        self.columna = columna

class Goto(Instruccion):
    '''
        Nodo de tipo Label
   
    '''
    def __init__(self,id,  linea=0 , columna=0) :
        self.id = id 
        self.linea = linea
        self.columna = columna

class Exit():
    '''
        Nodo de tipo Exit
   
    '''
    def __init__(self,  linea=0 , columna=0) :
        self.linea = linea
        self.columna = columna

class Read():
    '''
        Nodo de tipo Read
   
    '''
    def __init__(self,  linea=0 , columna=0) :
        self.linea = linea
        self.columna = columna