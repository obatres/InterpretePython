import gramatica as g
import ts as TS
from expresiones import *
from instrucciones import *
from graphviz import Digraph
from ts import TIPO_DATO as td
from _pydecimal import Decimal

true = 1
false = 0
#-----------------------------------------------------------INICIA ANALISIS SEMANTICO
def procesar_imprimir(instr, ts) :
    try:
        salida = resolver_registro(instr.exp,ts)
        print('>', salida)
        return  str(salida) + '\n'
    except:
        print('error de impresion, valor o variabe no encontrados: ',instr.exp.id)
        pass

def resolver_registro(exp,ts):

    return ts.obtener(exp.id).valor

def procesar_definicion(instr, ts) :
    simbolo = TS.Simbolo(instr.id, TS.TIPO_DATO.NUMERO, 0)      # inicializamos con 0 como valor por defecto
    ts.agregar(simbolo)

#Asignacion de temporal en la TS
def procesar_asignacion(instr, ts) :
    try:
        val = resolver_expresion_aritmetica(instr.expNumerica, ts)
        simbolo = TS.Simbolo(instr.id, instr.expNumerica.tipo, val)
        if ts.existeSimbolo(simbolo) :
            ts.actualizar(simbolo)
        else:
            ts.agregar(simbolo)
    except :
        print('No se puede realizar la asignacion')
        pass
        
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

        if (expNum.exp1.tipo==td.INT):

            if(expNum.exp2.tipo==td.INT):


                if expNum.operador == OPERACION_ARITMETICA.MAS : 
                    expNum.val =exp1+exp2
                    expNum.tipo = TS.TIPO_DATO.INT
                    return expNum.val
                if expNum.operador == OPERACION_ARITMETICA.MENOS : 
                    expNum.val =exp1-exp2
                    expNum.tipo = TS.TIPO_DATO.INT
                    return expNum.val
                if expNum.operador == OPERACION_ARITMETICA.POR : 
                    expNum.val =exp1*exp2
                    expNum.tipo = TS.TIPO_DATO.INT
                    return expNum.val
                if expNum.operador == OPERACION_ARITMETICA.DIVIDIDO : 
                    expNum.val =exp1/exp2
                    expNum.tipo = TS.TIPO_DATO.INT
                    return expNum.val
                if expNum.operador == OPERACION_ARITMETICA.RESIDUO : 
                    expNum.val =exp1%exp2
                    expNum.tipo = TS.TIPO_DATO.INT
                    return expNum.val
                       
            elif (expNum.exp2.tipo==td.FLOAT):


                if expNum.operador == OPERACION_ARITMETICA.MAS : 
                    expNum.val =exp1+exp2
                    expNum.tipo = TS.TIPO_DATO.FLOAT
                    return expNum.val
                if expNum.operador == OPERACION_ARITMETICA.MENOS : 
                    expNum.val =exp1-exp2
                    expNum.tipo = TS.TIPO_DATO.FLOAT
                    return expNum.val
                if expNum.operador == OPERACION_ARITMETICA.POR : 
                    expNum.val =exp1*exp2
                    expNum.tipo = TS.TIPO_DATO.FLOAT
                    return expNum.val
                if expNum.operador == OPERACION_ARITMETICA.DIVIDIDO : 
                    expNum.val =exp1/exp2
                    expNum.tipo = TS.TIPO_DATO.FLOAT
                    return expNum.val
                if expNum.operador == OPERACION_ARITMETICA.RESIDUO : 
                    expNum.val =exp1%exp2
                    expNum.tipo = TS.TIPO_DATO.FLOAT
                    return expNum.val
                else:
                    print('Error de operacion: el operador '+str(expNum.exp1.val)+' y el operador'+str(expNum.exp2.val)+' no reconocen este tipo de operacion')
            
            else:
                print('Error de tipos: el operador ',expNum.exp2.val,' no es de tipo INT o FLOAT y no puede ser operado ')

        elif (expNum.exp1.tipo==td.FLOAT):
    
            if(expNum.exp2.tipo==td.INT or expNum.exp2.tipo==td.FLOAT):
                if expNum.operador == OPERACION_ARITMETICA.MAS : 
                    expNum.val =exp1+exp2
                    expNum.tipo = TS.TIPO_DATO.FLOAT
                    return expNum.val
                if expNum.operador == OPERACION_ARITMETICA.MENOS : 
                    expNum.val =exp1-exp2
                    expNum.tipo = TS.TIPO_DATO.FLOAT
                    return expNum.val
                if expNum.operador == OPERACION_ARITMETICA.POR : 
                    expNum.val =exp1*exp2
                    expNum.tipo = TS.TIPO_DATO.FLOAT
                    return expNum.val
                if expNum.operador == OPERACION_ARITMETICA.DIVIDIDO : 
                    expNum.val =exp1/exp2
                    expNum.tipo = TS.TIPO_DATO.FLOAT
                    return expNum.val
                if expNum.operador == OPERACION_ARITMETICA.RESIDUO : 
                    expNum.val =exp1%exp2
                    expNum.tipo = TS.TIPO_DATO.FLOAT
                    return expNum.val
                else:
                    print('Error de operacion: el operador '+str(expNum.exp1.val)+' y el operador'+str(expNum.exp2.val)+' no reconocen este tipo de operacion')
            else:
                print('Error de tipos: el operador '+str(expNum.exp2.val)+' no es de tipo INT o FLOAT y no puede ser operado ')   

        elif (expNum.exp1.tipo==td.CADENA):
            if(expNum.exp2.tipo==td.CADENA):
                if expNum.operador == OPERACION_ARITMETICA.MAS : 
                    expNum.val =exp1+exp2
                    expNum.tipo = TS.TIPO_DATO.CADENA
                    return expNum.val
                else:
                    print('Error de operacion: el operador '+str(expNum.exp1.val)+' y el operador'+str(expNum.exp2.val)+' no reconocen este tipo de operacion')
            else:
                print('Error de tipos: el operador '+str(expNum.exp2.val)+' no es de tipo CADENA y no puede ser operado ')

    elif isinstance(expNum, ExpresionNegativo) :
        exp = resolver_expresion_aritmetica(expNum.exp, ts)
        expNum.val=exp*-1
        expNum.tipo = expNum.exp.tipo
        return expNum.val

    elif isinstance(expNum, ExpresionNumero) :
        expNum.tipo = expNum.tipo
        return expNum.val

    elif isinstance(expNum, ExpresionIdentificador) :
        return ts.obtener(expNum.id).valor

    elif isinstance(expNum, ExpresionTemporal):
        expNum.val = ts.obtener(expNum.id).valor
        expNum.tipo = ts.obtener(expNum.id).tipo
        return expNum.val

    elif isinstance (expNum, ExpresionPunteroTemp):
        temp = str(expNum.id).lstrip('&')
        expNum.val = ts.obtenerPuntero(temp)
        expNum.tipo = TS.TIPO_DATO.INT
        return expNum.val

    elif isinstance (expNum,ExpresionValorAbsoluto):
        temp=resolver_expresion_aritmetica(expNum.exp,ts)
        if expNum.exp.tipo== TS.TIPO_DATO.INT or expNum.exp.tipo == TS.TIPO_DATO.FLOAT:
            print(temp)
            expNum.val = abs(temp)
            expNum.tipo = expNum.exp.tipo
        else:
            expNum.val=temp
            expNum.tipo = expNum.exp.tipo
            print('No es posible obtener el valor absoluto de: ',expNum.val)
        return expNum.val

    elif isinstance (expNum,ExpresionConversion):
        temp = resolver_expresion_aritmetica(expNum.exp,ts) 
        conv = expNum.tipo
        if conv=='int':
            if expNum.exp.tipo==TS.TIPO_DATO.CADENA:
                expNum.val = ord(temp[0])
                expNum.tipo = TS.TIPO_DATO.INT
                return expNum.val 
            elif expNum.exp.tipo==TS.TIPO_DATO.FLOAT:
                expNum.val = int(Decimal(temp))
                expNum.tipo = TS.TIPO_DATO.INT
                return expNum.val 
            elif expNum.exp.tipo==TS.TIPO_DATO.INT:
                expNum.val = temp
                expNum.tipo = TS.TIPO_DATO.INT
                return expNum.val
            else:
                print('la conversion a (int) de ',temp,'no se puede realizar por error de tipo')
        
        elif conv=='float':
            if expNum.exp.tipo==TS.TIPO_DATO.CADENA:
                temp1 = ord(temp[0])
                expNum.val = str(temp1) + '.0'
                expNum.tipo = TS.TIPO_DATO.FLOAT
                return float(expNum.val)
            elif expNum.exp.tipo==TS.TIPO_DATO.FLOAT:
                expNum.val = temp
                expNum.tipo = TS.TIPO_DATO.FLOAT
                return expNum.val 
            elif expNum.exp.tipo==TS.TIPO_DATO.INT:
                expNum.val = str(temp) + '.0'
                expNum.tipo = TS.TIPO_DATO.FLOAT
                return float(expNum.val) 
            else:
                print('la conversion a (float) de ',temp,'no se puede realizar por error de tipo')
        
        elif conv=='char':
            if expNum.exp.tipo==TS.TIPO_DATO.CADENA:
                expNum.val = temp[0]
                expNum.tipo = TS.TIPO_DATO.CADENA
                return expNum.val
            elif expNum.exp.tipo==TS.TIPO_DATO.FLOAT:
                temp2 = int(Decimal(temp))
                if temp2>=0 and temp2<255: expNum.val = chr(temp2)                    
                elif temp2>=256:          expNum.val = chr(temp2%256)

                expNum.tipo = TS.TIPO_DATO.CADENA
                return expNum.val
            elif expNum.exp.tipo==TS.TIPO_DATO.INT:
                
                if temp>=0 and temp<255: expNum.val = chr(temp)                    
                elif temp>=256:          expNum.val = chr(temp%256)

                expNum.tipo = TS.TIPO_DATO.CADENA
                return expNum.val
            else:
                print('la conversion a (char) de ',temp,'no se puede realizar por error de tipo')
        
        else:
            print('La conversion de tipo',expNum.tipo,'No es posible ejecutarla')
        
    elif isinstance (expNum, ExpresionLogicaNot):
        temp = resolver_expresion_aritmetica(expNum.exp,ts)
        if temp==false: expNum.val=true
        elif temp==true: expNum.val=false
        else: 
            expNum.val=1964
            print('Valor',temp,' no asociado a una condicion logica')
        expNum.tipo=TS.TIPO_DATO.INT
        return expNum.val
   
    elif isinstance (expNum, ExpresionLogicaXOR):
        exp1 = resolver_expresion_aritmetica(expNum.exp1,ts)
        exp2 = resolver_expresion_aritmetica(expNum.exp2,ts)
        if expNum.exp1.tipo==TS.TIPO_DATO.INT and expNum.exp1.tipo==TS.TIPO_DATO.INT :
            expNum.tipo = TS.TIPO_DATO.INT
            if exp1==true:
                if exp2==true:
                    return false
                elif exp2==false:
                    return true
                else:
                    print("error de valor ",exp2," no puede ser comparado en un XOR")          
            elif exp1==false:
                if exp2==true:
                    return true
                elif exp2==false:
                    return false
                else:
                    print("error de valor ",exp2,", no puede ser comparado en un XOR") 
            else:
                print("error de valor ",exp1," no puede ser comparado en un XOR")       
        else:
            print('error de tipos ',exp2,'y ',exp2,' no pueden operarse en un XOR, ambos deben ser INT')

    elif isinstance (expNum, ExpresionLogicaOR):
        exp1 = resolver_expresion_aritmetica(expNum.exp1,ts)
        exp2 = resolver_expresion_aritmetica(expNum.exp2,ts)
        if expNum.exp1.tipo==TS.TIPO_DATO.INT and expNum.exp1.tipo==TS.TIPO_DATO.INT :
            expNum.tipo = TS.TIPO_DATO.INT
            if exp1==true:
                if exp2==true:
                    return true
                elif exp2==false:
                    return true
                else:
                    print("error de valor ",exp2," no puede ser comparado en un OR")          
            elif exp1==false:
                if exp2==true:
                    return true
                elif exp2==false:
                    return false
                else:
                    print("error de valor ",exp2,", no puede ser comparado en un OR") 
            else:
                print("error de valor ",exp1," no puede ser comparado en un OR")       
        else:
            print('error de tipos ',exp2,'y ',exp2,' no pueden operarse en un OR, ambos deben ser INT')
    
    elif isinstance (expNum, ExpresionLogicaAND):   
        exp1 = resolver_expresion_aritmetica(expNum.exp1,ts)
        exp2 = resolver_expresion_aritmetica(expNum.exp2,ts)
        if expNum.exp1.tipo==TS.TIPO_DATO.INT and expNum.exp1.tipo==TS.TIPO_DATO.INT :
            expNum.tipo = TS.TIPO_DATO.INT
            if exp1==true:
                if exp2==true:
                    return true
                elif exp2==false:
                    return false
                else:
                    print("error de valor ",exp2," no puede ser comparado en un AND")          
            elif exp1==false:
                if exp2==true:
                    return false
                elif exp2==false:
                    return true
                else:
                    print("error de valor ",exp2,", no puede ser comparado en un AND") 
            else:
                print("error de valor ",exp1,", no puede ser comparado en un AND")       
        else:
            print('error de tipos ',exp1,' y "=',exp2,' no pueden operarse en un AND, ambos deben ser INT')
    
    elif isinstance (expNum, ExpresionBitNot):
        temp = resolver_expresion_aritmetica(expNum.exp,ts)
        if expNum.exp.tipo == TS.TIPO_DATO.INT or expNum.exp.tipo == TS.TIPO_DATO.FLOAT:       
            t = int(Decimal(temp))
            expNum.val=~t
            expNum.tipo = TS.TIPO_DATO.INT
            return expNum.val
        else:
            print('El valor ',temp,'no pude ser operado en binario por un NOT, se esperaba un tipo INT o FLOAT')

    elif isinstance (expNum, ExpresionBitAnd):
        exp1 = resolver_expresion_aritmetica(expNum.exp1,ts)
        exp2 = resolver_expresion_aritmetica(expNum.exp2,ts)
        if expNum.exp1.tipo == TS.TIPO_DATO.INT or expNum.exp1.tipo == TS.TIPO_DATO.FLOAT: 
            t1 = int(Decimal(exp1))     
            if expNum.exp2.tipo == TS.TIPO_DATO.INT or expNum.exp2.tipo == TS.TIPO_DATO.FLOAT: 
                t2 = int(Decimal(exp2))
                expNum.tipo = TS.TIPO_DATO.INT
                return t1 & t2
            else:
                print ('error de tipos ',exp1,' y ',exp2,'no se pueden operar en un AND bit a bit se espera que ambos sean INT o FLOAT')
        else:
            print ('error de tipos ',exp1,' y ',exp2,'no se pueden operar en un AND bit a bit se espera que ambos sean INT o FLOAT')

    elif isinstance (expNum, ExpresionBitOr):
        exp1 = resolver_expresion_aritmetica(expNum.exp1,ts)
        exp2 = resolver_expresion_aritmetica(expNum.exp2,ts)
        if expNum.exp1.tipo == TS.TIPO_DATO.INT or expNum.exp1.tipo == TS.TIPO_DATO.FLOAT: 
            t1 = int(Decimal(exp1))     
            if expNum.exp2.tipo == TS.TIPO_DATO.INT or expNum.exp2.tipo == TS.TIPO_DATO.FLOAT: 
                t2 = int(Decimal(exp2))
                expNum.tipo = TS.TIPO_DATO.INT
                return t1 | t2
            else:
                print ('error de tipos ',exp1,' y ',exp2,'no se pueden operar en un OR bit a bit se espera que ambos sean INT o FLOAT')
        else:
            print ('error de tipos ',exp1,' y ',exp2,'no se pueden operar en un OR bit a bit se espera que ambos sean INT o FLOAT')

    elif isinstance (expNum, ExpresionBitXor):
        exp1 = resolver_expresion_aritmetica(expNum.exp1,ts)
        exp2 = resolver_expresion_aritmetica(expNum.exp2,ts)
        if expNum.exp1.tipo == TS.TIPO_DATO.INT or expNum.exp1.tipo == TS.TIPO_DATO.FLOAT: 
            t1 = int(Decimal(exp1))     
            if expNum.exp2.tipo == TS.TIPO_DATO.INT or expNum.exp2.tipo == TS.TIPO_DATO.FLOAT: 
                t2 = int(Decimal(exp2))
                expNum.tipo = TS.TIPO_DATO.INT
                return t1 ^ t2
            else:
                print ('error de tipos ',exp1,' y ',exp2,'no se pueden operar en un AND bit a bit se espera que ambos sean INT o FLOAT')
        else:
            print ('error de tipos ',exp1,' y ',exp2,'no se pueden operar en un AND bit a bit se espera que ambos sean INT o FLOAT')

    elif isinstance (expNum, ExpresionBitIzq):
        print('ES CORRIEMIENTO A LA IZQUI')  

    elif isinstance (expNum, ExpresionBitDer):
        print('ES CORRIEMIENTO A LA DER')  
    else:
        print(expNum)

def procesar_unset(exp, ts):
    
    if isinstance(exp.exp,ExpresionTemporal):
        temp = exp.exp.id
        ts.eliminar(temp)
    else:
        print('El valor ',exp.exp,'no puede ser ejecutado por unset(), se esperaba un registro')


def procesar_instrucciones(instrucciones, ts) :
    ## lista de instrucciones recolectadas
    for instr in instrucciones :
        if isinstance(instr, Imprimir) : procesar_imprimir(instr, ts)
        elif isinstance(instr, Definicion) : procesar_definicion(instr, ts)
        elif isinstance(instr, Asignacion) : procesar_asignacion(instr, ts)
        elif isinstance(instr, Mientras) : procesar_mientras(instr, ts)
        elif isinstance(instr, If) : procesar_if(instr, ts)
        elif isinstance(instr, IfElse) : procesar_if_else(instr, ts)
        elif isinstance(instr, Unset) : procesar_unset(instr,ts)
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

#-----------------------------------------------------------EJECUCION DEL ANALIZADOR
f = open("./entrada.txt", "r")
input = f.read()

instrucciones = g.parse(input)
ts_global = TS.TablaDeSimbolos()


dot = Digraph(comment='AUGUS')
DibujarAST(instrucciones)
procesar_instrucciones(instrucciones, ts_global)


