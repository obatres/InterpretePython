import gramatica as g
import ts as TS
import sys
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
            
        #if not ts.obtener(instr.exp.id).tipo == td.ARRAY:
            salida = resolver_registro(instr.exp,ts)

            print('>', salida)
            return  str(salida) + '\n'
        #else:
            #print('Error, no se puede imprimir un arreglo')
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
        print('No se puede realizar la asignacionde',instr.id)
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
    if expLog.exp1.tipo == TS.TIPO_DATO.INT or expLog.exp1.tipo == TS.TIPO_DATO.FLOAT:
        if expLog.exp2.tipo == TS.TIPO_DATO.INT or expLog.exp2.tipo == TS.TIPO_DATO.FLOAT:
            expLog.tipo = TS.TIPO_DATO.INT
            if expLog.operador == OPERACION_LOGICA.MAYOR_QUE : 
                if exp1 > exp2: return true
                else:           return false 
            if expLog.operador == OPERACION_LOGICA.MENOR_QUE :
                if exp1 < exp2: return true
                else:           return false 
            if expLog.operador == OPERACION_LOGICA.IGUAL : 
                if exp1 == exp2: return true
                else:            return false 
            if expLog.operador == OPERACION_LOGICA.DIFERENTE : 
                if exp1 != exp2: return true
                else:            return false 
            if expLog.operador == OPERACION_LOGICA.MAYORQUE : 
                if exp1 >= exp2: return true
                else:            return false 
            if expLog.operador == OPERACION_LOGICA.MENORQUE : 
                if exp1 <= exp2: return true
                else:            return false 
        else:
            print('error de tipos ',exp1,'y ',exp2,' no pueden ser operados en una operacion relacional, \n se espera que ambos tengan el mismo tipo')
    elif expLog.exp1.tipo == TS.TIPO_DATO.CADENA:
        if expLog.exp2.tipo == TS.TIPO_DATO.CADENA:
            expLog.tipo = TS.TIPO_DATO.INT
            if expLog.operador == OPERACION_LOGICA.MAYOR_QUE : 
                if exp1 > exp2: return true
                else:           return false 
            if expLog.operador == OPERACION_LOGICA.MENOR_QUE :
                if exp1 < exp2: return true
                else:           return false 
            if expLog.operador == OPERACION_LOGICA.IGUAL : 
                if exp1 == exp2: return true
                else:            return false   
            if expLog.operador == OPERACION_LOGICA.DIFERENTE : 
                if exp1 != exp2: return true
                else:            return false        
            if expLog.operador == OPERACION_LOGICA.MAYORQUE : 
                if exp1 >= exp2: return true
                else:            return false  
            if expLog.operador == OPERACION_LOGICA.MENORQUE : 
                if exp1 <= exp2: return true
                else:            return false                                                                      
        else:
            print('error de tipos ',exp1,'y ',exp2,' no pueden ser operados en una operacion relacional, \n se espera que ambos tengan el mismo tipo')

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
                print ('error de tipos ',exp1,' y ',exp2,'no se pueden operar en un XOR bit a bit se espera que ambos sean INT o FLOAT')
        else:
            print ('error de tipos ',exp1,' y ',exp2,'no se pueden operar en un XOR bit a bit se espera que ambos sean INT o FLOAT')

    elif isinstance (expNum, ExpresionBitIzq):
        exp1 = resolver_expresion_aritmetica(expNum.exp1,ts)
        exp2 = resolver_expresion_aritmetica(expNum.exp2,ts)
        if expNum.exp1.tipo == TS.TIPO_DATO.INT or expNum.exp1.tipo == TS.TIPO_DATO.FLOAT: 
            t1 = int(Decimal(exp1))     
            if expNum.exp2.tipo == TS.TIPO_DATO.INT or expNum.exp2.tipo == TS.TIPO_DATO.FLOAT: 
                t2 = int(Decimal(exp2))
                expNum.tipo = TS.TIPO_DATO.INT
                return t1 << t2
            else:
                print ('error de tipos ',exp1,' y ',exp2,'no se pueden operar en un CORR IZQ bit a bit se espera que ambos sean INT o FLOAT')
        else:
            print ('error de tipos ',exp1,' y ',exp2,'no se pueden operar en un CORR IZQ bit a bit se espera que ambos sean INT o FLOAT')

    elif isinstance (expNum, ExpresionBitDer):
        exp1 = resolver_expresion_aritmetica(expNum.exp1,ts)
        exp2 = resolver_expresion_aritmetica(expNum.exp2,ts)
        if expNum.exp1.tipo == TS.TIPO_DATO.INT or expNum.exp1.tipo == TS.TIPO_DATO.FLOAT: 
            t1 = int(Decimal(exp1))     
            if expNum.exp2.tipo == TS.TIPO_DATO.INT or expNum.exp2.tipo == TS.TIPO_DATO.FLOAT: 
                t2 = int(Decimal(exp2))
                expNum.tipo = TS.TIPO_DATO.INT
                return t1 >> t2
            else:
                print ('error de tipos ',exp1,' y ',exp2,'no se pueden operar en un CORR DER bit a bit se espera que ambos sean INT o FLOAT')
        else:
            print ('error de tipos ',exp1,' y ',exp2,'no se pueden operar en un CORR DER bit a bit se espera que ambos sean INT o FLOAT')
    
    elif isinstance (expNum,ExpresionLogica):
        return resolver_expreision_logica(expNum,ts)
    
    elif isinstance (expNum, InicioArray):
        expNum.tipo = TS.TIPO_DATO.ARRAY
        expNum.val = {}
        return expNum.val
    
    elif isinstance(expNum,ExpresionPila):
        expNum.val = ts.obtener(expNum.id).valor
        expNum.tipo = ts.obtener(expNum.id).tipo
        return expNum.val
   
    elif isinstance (expNum,ExpresionPunteroPila):
        expNum.val = ts.obtener(expNum.id).valor
        expNum.tipo = td.INT
        return expNum.val

    elif isinstance(expNum,Expresion_Pop_pila):
        pila = ts.obtener(expNum.idPila).valor
        puntero = ts.obtener(expNum.puntero).valor
        
        expNum.val = pila[puntero]

        if isinstance(expNum.val,int): expNum.tipo = td.INT
        elif isinstance (expNum.val,str): expNum.tipo = td.CADENA
        elif isinstance(expNum.val,float): expNum.tipo = td.FLOAT
        return expNum.val

    elif isinstance(expNum,Expresion_param):
        expNum.val = ts.obtener(expNum.id).valor
        expNum.tipo = ts.obtener(expNum.id).tipo
        return expNum.val
    
    else:
        print(expNum)

def procesar_unset(exp, ts):
    
    if isinstance(exp.exp,ExpresionTemporal):
        temp = exp.exp.id
        ts.eliminar(temp)
    else:
        print('El valor ',exp.exp,'no puede ser ejecutado por unset(), se esperaba un registro')

def procesar_inicioPila(instr,ts):
    pila = TS.Simbolo(instr.id,td.PILA,[])
    if ts.existeSimbolo(pila):
        print('La pila ya existe')
    else:
        ts.agregar(pila)

def procesar_asignacion_punteropila(instr,ts):
    valor=resolver_expresion_aritmetica(instr.exp,ts)
    punteropila = TS.Simbolo(instr.id,td.INT,valor)
    if ts.existeSimbolo(punteropila):
        ts.actualizar(punteropila)
    else:
        ts.agregar(punteropila)

def procesar_asignacion_pila (instr,ts):
    try:
        pila = ts.obtener(instr.id).valor
        pos = ts.obtener(instr.puntero).valor
        valor = resolver_expresion_aritmetica(instr.exp,ts)
        pila.insert(pos,valor)

        nuevapila = TS.Simbolo(instr.id,td.PILA,pila)

        if ts.existeSimbolo(nuevapila):
            ts.actualizar(nuevapila)
        else:
            print('error pila',instr.id,'no existe')
    except :
        print('error en asignacion de valor a la pila')

def procesar_asignacion_extra (instr,ts):
    try:
        val = resolver_expresion_aritmetica(instr.exp, ts)
        simbolo = TS.Simbolo(instr.id, instr.exp.tipo, val)
        if ts.existeSimbolo(simbolo) :
            ts.actualizar(simbolo)
        else:
            ts.agregar(simbolo)
    except :
        print('No se puede realizar la asignacion de',instr.id)
        pass
def procesar_asignacion_arreglo (instr,ts):
    diccionario = ts.obtener(instr.id).valor
    lista = instr.lista
    niveles = len(lista)
    valor_a_asignar = resolver_expresion_aritmetica(instr.exp,ts)

    for i in range(len(lista)):
        indice = resolver_expresion_aritmetica(lista[i],ts)
        if i== niveles-1:
            diccionario[indice]=valor_a_asignar
        else:
            diccionario_aux = diccionario.get(indice)
            if diccionario_aux == None:
                diccionario[indice]={}
                diccionario=diccionario.get(indice)
            else:
                diccionario=diccionario.get(indice)

def procesa_Label(instr,ts):
    print(instr.id)

def Llamada_goto(instr,ts,listasiguientes):

  
    siguientes = []
    i = 0
    for ins in listasiguientes:
        if isinstance(ins,Label):
            if ins.id == instr.id:
                siguientes = listasiguientes[i+1:]
                ejecutar_expresiones_label(siguientes,ts,listasiguientes)
                return
        i = i+1
    return

def ejecutar_expresiones_label(listainstrucciones,ts,listaglobal):
        for instr in listainstrucciones :
            if isinstance(instr, Imprimir) : procesar_imprimir(instr, ts)
            elif isinstance(instr, Definicion) : procesar_definicion(instr, ts)
            elif isinstance(instr, Asignacion) : procesar_asignacion(instr, ts)
            elif isinstance(instr, Mientras) : procesar_mientras(instr, ts)
            elif isinstance(instr, If) : procesar_if(instr, ts)
            elif isinstance(instr, IfElse) : procesar_if_else(instr, ts)
            elif isinstance(instr, Unset) : procesar_unset(instr,ts)
            elif isinstance(instr,IniciaPila): procesar_inicioPila(instr,ts)
            elif isinstance(instr,AsignaPunteroPila): procesar_asignacion_punteropila(instr,ts)
            elif isinstance(instr,AsignaValorPila): procesar_asignacion_pila(instr,ts)
            elif isinstance(instr, AsignacionExtra): procesar_asignacion_extra(instr,ts)
            elif isinstance(instr, Main): print('')
            elif isinstance(instr,Asigna_arreglo): procesar_asignacion_arreglo(instr,ts)
            elif isinstance(instr,Label): procesa_Label(instr,ts)
            elif isinstance(instr,Exit): sys.exit()
            elif isinstance(instr,Goto):
                Llamada_goto(instr,ts, listaglobal)
                return
            else : print('Error: instrucción no válida', instr)

def procesar_instrucciones(instrucciones, ts) :
    ## lista de instrucciones recolectadas
    if isinstance(instrucciones[0],Main):
        for instr in instrucciones :
            if isinstance(instr, Imprimir) : procesar_imprimir(instr, ts)
            elif isinstance(instr, Definicion) : procesar_definicion(instr, ts)
            elif isinstance(instr, Asignacion) : procesar_asignacion(instr, ts)
            elif isinstance(instr, Mientras) : procesar_mientras(instr, ts)
            elif isinstance(instr, If) : procesar_if(instr, ts)
            elif isinstance(instr, IfElse) : procesar_if_else(instr, ts)
            elif isinstance(instr, Unset) : procesar_unset(instr,ts)
            elif isinstance(instr,IniciaPila): procesar_inicioPila(instr,ts)
            elif isinstance(instr,AsignaPunteroPila): procesar_asignacion_punteropila(instr,ts)
            elif isinstance(instr,AsignaValorPila): procesar_asignacion_pila(instr,ts)
            elif isinstance(instr, AsignacionExtra): procesar_asignacion_extra(instr,ts)
            elif isinstance(instr, Main): print('')
            elif isinstance(instr,Asigna_arreglo): procesar_asignacion_arreglo(instr,ts)
            elif isinstance(instr,Label): procesa_Label(instr,ts)
            elif isinstance(instr,Exit): sys.exit()
            elif isinstance(instr,Goto): 
                Llamada_goto(instr,ts, instrucciones)
                return
            
            else : print('Error: instrucción no válida', instr)
    else:
        print('Error la etiqueta main no esta al inicio del programa o no existe')
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
try:
    DibujarAST(instrucciones)
except :
    pass

try:
    procesar_instrucciones(instrucciones, ts_global)
except :
    pass


class objetopila():

    def __init__(self, valor, tipo):
        self.valor = valor
        self.tipo = tipo

