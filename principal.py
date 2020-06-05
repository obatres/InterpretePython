import gramatica as g
import ts as TS
from expresiones import *
from instrucciones import *
from graphviz import Digraph
#-----------------------------------------------------------INICIA ANALISIS SEMANTICO
def procesar_imprimir(instr, ts) :
    #print('> ', resolver_cadena(instr.cad, ts))
    #print(type(instr))
    print('>',resolver_registro(instr.exp,ts))


def resolver_registro(exp,ts):
    print(type(exp))

def procesar_definicion(instr, ts) :
    simbolo = TS.Simbolo(instr.id, TS.TIPO_DATO.NUMERO, 0)      # inicializamos con 0 como valor por defecto
    ts.agregar(simbolo)

#Asignacion de temporal en la TS
def procesar_asignacion(instr, ts) :
    val = resolver_expresion_aritmetica(instr.expNumerica, ts)
    simbolo = TS.Simbolo(instr.id, instr.expNumerica.tipo, val)
    if ts.existeSimbolo(simbolo) :
        ts.actualizar(simbolo)
    else:
        ts.agregar(simbolo)

def procesar_mientras(instr, ts) :
    while resolver_expreision_logica(instr.expLogica, ts) :
        ts_local = TS.TablaDeSimbolos(ts.simbolos)
        procesar_instrucciones(instr.instrucciones, ts_local)

def procesar_if(instr, ts) :
    val = resolver_expreision_logica(instr.expLogica, ts)
    if val :
        ts_local = TS.TablaDeSimbolos(ts.simbolos)
        procesar_instrucciones(instr.instrucciones, ts_local)

def procesar_if_else(instr, ts) :
    val = resolver_expreision_logica(instr.expLogica, ts)
    if val :
        ts_local = TS.TablaDeSimbolos(ts.simbolos)
        procesar_instrucciones(instr.instrIfVerdadero, ts_local)
    else :
        ts_local = TS.TablaDeSimbolos(ts.simbolos)
        procesar_instrucciones(instr.instrIfFalso, ts_local)

def resolver_cadena(exp, ts) :
    if isinstance(exp, ExpresionConcatenar) :
        exp1 = resolver_cadena(exp.exp1, ts)
        exp2 = resolver_cadena(exp.exp2, ts)
        return exp1 + exp2
    elif isinstance(exp, ExpresionDobleComilla) :
        return exp.val
    elif isinstance(exp, ExpresionCadenaNumerico) :
        return str(resolver_expresion_aritmetica(exp.exp, ts))
    elif isinstance(exp,ExpresionIdentificador):
        return str(ts.obtener(exp.id).valor)
    else :
        print('Error: Expresión cadena no válida')

def resolver_expreision_logica(expLog, ts) :
    exp1 = resolver_expresion_aritmetica(expLog.exp1, ts)
    exp2 = resolver_expresion_aritmetica(expLog.exp2, ts)
    if expLog.operador == OPERACION_LOGICA.MAYOR_QUE : return exp1 > exp2
    if expLog.operador == OPERACION_LOGICA.MENOR_QUE : return exp1 < exp2
    if expLog.operador == OPERACION_LOGICA.IGUAL : return exp1 == exp2
    if expLog.operador == OPERACION_LOGICA.DIFERENTE : return exp1 != exp2

def resolver_expresion_aritmetica(expNum, ts) :
    if isinstance(expNum, ExpresionBinaria) :
        #VALIDAR TIPOS
        exp1 = resolver_expresion_aritmetica(expNum.exp1, ts)
        exp2 = resolver_expresion_aritmetica(expNum.exp2, ts)
        if expNum.operador == OPERACION_ARITMETICA.MAS : 
            expNum.val =exp1+exp2
            expNum.tipo = TS.TIPO_DATO.INT
            return expNum.val
        if expNum.operador == OPERACION_ARITMETICA.MENOS : return exp1 - exp2
        if expNum.operador == OPERACION_ARITMETICA.POR : return exp1 * exp2
        if expNum.operador == OPERACION_ARITMETICA.DIVIDIDO : return exp1 / exp2
    elif isinstance(expNum, ExpresionNegativo) :
        exp = resolver_expresion_aritmetica(expNum.exp, ts)
        return exp * -1
    elif isinstance(expNum, ExpresionNumero) :
        return expNum.val
    elif isinstance(expNum, ExpresionIdentificador) :
        return ts.obtener(expNum.id).valor


def procesar_instrucciones(instrucciones, ts) :
    ## lista de instrucciones recolectadas
    for instr in instrucciones :
        if isinstance(instr, Imprimir) : procesar_imprimir(instr, ts)
        elif isinstance(instr, Definicion) : procesar_definicion(instr, ts)
        elif isinstance(instr, Asignacion) : procesar_asignacion(instr, ts)
        elif isinstance(instr, Mientras) : procesar_mientras(instr, ts)
        elif isinstance(instr, If) : procesar_if(instr, ts)
        elif isinstance(instr, IfElse) : procesar_if_else(instr, ts)
        else : print('Error: instrucción no válida')
#-----------------------------------------------------------TERMINA ANALISIS SEMANTICO

#-----------------------------------------------------------INICIA GRAFICACION DEL AST

def dibujar_asignacion(instr,root,cont):
    cont=cont+1
    nodo = 'nodo'+ str(cont)
    dot.node(nodo,'Asignacion')
    dot.edge(root, nodo)
    cont = cont +1
    nodo1= 'nodo'+str(cont)
    dot.node(nodo1,instr.id)
    dot.edge(nodo,nodo1)
    return cont

def DibujarAST(instrucciones):
    cont = 1
    root = 'nodo'+ str(cont)
    dot.node(root, 'AUGUS')
    for instr in instrucciones:
        if isinstance(instr,Asignacion) : cont = dibujar_asignacion(instr,root,cont)
        else : 
            print('')
    #print(dot.source)

#-----------------------------------------------------------TERMINA GRAFICACION DEL AST
f = open("./entrada.txt", "r")
input = f.read()

instrucciones = g.parse(input)
ts_global = TS.TablaDeSimbolos()

dot = Digraph(comment='AUGUS')
DibujarAST(instrucciones)
procesar_instrucciones(instrucciones, ts_global)