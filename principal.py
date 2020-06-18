
import ts as TS
import sys
from expresiones import *
from instrucciones import *
from graphviz import Digraph
from ts import TIPO_DATO as td
from _pydecimal import Decimal
import copy
from Interfaz import MainWindow as M
import re

true = 1
false = 0
Etiqueta = ''

#-----------------------------------------------------------INICIA ANALISIS SEMANTICO
def procesar_imprimir(instr, ts) :

    try:
            
        if not ts.obtener(instr.exp.id).tipo == td.ARRAY or ts.obtener(instr.exp.id).tipo == td.PILA:
            #salida = resolver_registro(instr.exp,ts)
            salida = resolver_expresion_aritmetica(instr.exp,ts)
            print('>', salida)
            global resultado
            
            resultado += '>'+str(salida)+'\n'
            return  str(salida) + '\n'
        else:
            #print('Error, no se puede imprimir un arreglo')
            err = 'Error de tipo, no se puede imprimir el valor',instr.exp.id ,'En la linea: ',instr.linea,'En la columna: ',instr.columna, 'Tipo: SEMANTICO'
            errores.append(err)
    except:
        print('error de impresion, valor o variabe no encontrados: ',instr.exp.id ) 
        print(instr.linea,instr.columna)
        err = 'Error de impresion, valor o variabe no encontrados: ',instr.exp.id ,'En la linea: ',instr.linea,'En la columna: ',instr.columna, 'Tipo: SEMANTICO'
        errores.append(err)
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
        simbolo = TS.Simbolo(instr.id, instr.expNumerica.tipo, val,Etiqueta)
        if ts.existeSimbolo(simbolo) :
            ts.actualizar(simbolo)
        else:
            ts.agregar(simbolo)
    except :
        print('No se puede realizar la asignacionde',instr.id, instr.linea, instr.columna)
        err = 'Error No se puede realizar la asignacionde ',instr.id ,' En la linea: ',instr.linea,' En la columna: ',instr.columna, 'Tipo: SEMANTICO'
        errores.append(err)
        pass
        
def procesar_mientras(instr, ts) :
    while resolver_expresion_logica(instr.expLogica, ts) :
        ts_local = TS.TablaDeSimbolos(ts.simbolos)
        procesar_instrucciones(instr.instrucciones, ts_local)

def procesar_if(instr, ts) :
    try:
        condicion = resolver_expresion_logica(instr.exp,ts)
    except :
        err = 'Error No se puede resolver la expresion a comparar en el if ',instr.exp ,' En la linea: ',instr.linea,' En la columna: ',instr.columna, 'Tipo: SEMANTICO'
        errores.append(err)

    if condicion == 1: Llamada_goto(instr.goto,ts,instrucciones)

def procesar_if_else(instr, ts) :
    val = resolver_expresion_logica(instr.expLogica, ts)
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

def resolver_expresion_logica(expLog, ts) :

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
            print('Error de tipos ',exp1,'y ',exp2,' no pueden ser operados en una operacion relacional, se espera que ambos tengan el mismo tipo')
            err = 'Error de tipos ',exp1,'y ',exp2,' no pueden ser operados en una operacion relacional, se espera que ambos tengan el mismo tipo' ,' En la linea: ',expLog.linea,' En la columna: ',expLog.columna, 'Tipo: SEMANTICO'
            errores.append(err)  
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
            err = 'Error de tipos ',exp1,'y ',exp2,' no pueden ser operados en una operacion relacional, se espera que ambos tengan el mismo tipo' ,' En la linea: ',expLog.linea,' En la columna: ',expLog.columna, 'Tipo: SEMANTICO'
            errores.append(err)  

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
                    err = 'Error de operacion: el operador '+str(expNum.exp1.val)+' y el operador'+str(expNum.exp2.val)+' no reconocen este tipo de operacion' ,' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
                    errores.append(err)  
            else:
                print('Error de tipos: el operador ',expNum.exp2.val,' no es de tipo INT o FLOAT y no puede ser operado ')
                err = 'Error de tipos: el operador ',expNum.exp2.val,' no es de tipo INT o FLOAT y no puede ser operado' ,' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
                errores.append(err)  

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
                    err = 'Error de operacion: el operador '+str(expNum.exp1.val)+' y el operador'+str(expNum.exp2.val)+' no reconocen este tipo de operacion' ,' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
                    errores.append(err)  
            else:
                print('Error de tipos: el operador '+str(expNum.exp2.val)+' no es de tipo INT o FLOAT y no puede ser operado ')   
                err = 'Error de tipos: el operador '+str(expNum.exp2.val)+' no es de tipo INT o FLOAT y no puede ser operado ' ,' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
                errores.append(err)  

        elif (expNum.exp1.tipo==td.CADENA):
            if(expNum.exp2.tipo==td.CADENA):
                if expNum.operador == OPERACION_ARITMETICA.MAS : 
                    expNum.val =exp1+exp2
                    expNum.tipo = TS.TIPO_DATO.CADENA
                    return expNum.val
                else:
                    print('Error de operacion: el operador '+str(expNum.exp1.val)+' y el operador'+str(expNum.exp2.val)+' no reconocen este tipo de operacion')
                    err = 'Error de operacion: el operador '+str(expNum.exp1.val)+' y el operador'+str(expNum.exp2.val)+' no reconocen este tipo de operacion ' ,' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
                    errores.append(err)  
            else:
                print('Error de tipos: el operador '+str(expNum.exp2.val)+' no es de tipo CADENA y no puede ser operado ')
                err = 'Error de tipos: el operador '+str(expNum.exp2.val)+' no es de tipo CADENA y no puede ser operado' ,' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
                errores.append(err)
    
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
            err = 'Error, no es posible obtener el valor absoluto de: ',expNum.val ,' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
            errores.append(err)
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
                err = 'Error la conversion a (int) de ',temp,'no se puede realizar por error de tipo',' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
                errores.append(err)
        
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
            err = 'Error: Valor',temp,' no asociado a una condicion logica',' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
            errores.append(err)
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
                    err = 'Error de valor ',exp2,'no puede ser comparado en un XOR',' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
                    errores.append(err)        
            elif exp1==false:
                if exp2==true:
                    return true
                elif exp2==false:
                    return false
                else:
                    print("error de valor ",exp2,", no puede ser comparado en un XOR")
                    err = 'Error de valor ',exp2,'no puede ser comparado en un XOR',' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
                    errores.append(err)    
            else:
                print("error de valor ",exp1," no puede ser comparado en un XOR")    
                err = 'Error de valor ',exp1,'no puede ser comparado en un XOR',' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
                errores.append(err)    
        else:
            print('error de tipos ',exp2,'y ',exp2,' no pueden operarse en un XOR, ambos deben ser INT')
            err = 'Error de tipos ',exp2,'y ',exp2,' no pueden operarse en un XOR, ambos deben ser INT',' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
            errores.append(err)  
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
                    err = 'Error de valor ',exp2,' no puede ser comparado en un OR',' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
                    errores.append(err)         
            elif exp1==false:
                if exp2==true:
                    return true
                elif exp2==false:
                    return false
                else:
                    print("error de valor ",exp2,", no puede ser comparado en un OR") 
                    err = 'Error de valor ',exp2,' no puede ser comparado en un OR',' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
                    errores.append(err)  
            else:
                print("error de valor ",exp1," no puede ser comparado en un OR")    
                err = 'Error de valor ',exp1,' no puede ser comparado en un OR',' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
                errores.append(err)  
        else:
            print('error de tipos ',exp2,'y ',exp2,' no pueden operarse en un OR, ambos deben ser INT')
            err = 'Error de tipos ',exp1,'y ',exp2,' no pueden operarse en un OR, ambos deben ser INT',' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
            errores.append(err) 
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
                    err = 'Error de valor ',exp2,' no puede ser comparado en un AND',' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
                    errores.append(err)   
            elif exp1==false:
                if exp2==true:
                    return false
                elif exp2==false:
                    return true
                else:
                    print("error de valor ",exp2,", no puede ser comparado en un AND") 
                    err = 'Error de valor ',exp2,' no puede ser comparado en un AND',' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
                    errores.append(err)  
            else:
                print("error de valor ",exp1,", no puede ser comparado en un AND") 
                err = 'Error de valor ',exp1,' no puede ser comparado en un AND',' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
                errores.append(err)       
        else:
            print('error de tipos ',exp1,' y "=',exp2,' no pueden operarse en un AND, ambos deben ser INT')
            err = 'Error de tipos ',exp1,' y "=',exp2,' no pueden operarse en un AND, ambos deben ser INT',' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
            errores.append(err)   
    
    elif isinstance (expNum, ExpresionBitNot):
        temp = resolver_expresion_aritmetica(expNum.exp,ts)
        if expNum.exp.tipo == TS.TIPO_DATO.INT or expNum.exp.tipo == TS.TIPO_DATO.FLOAT:       
            t = int(Decimal(temp))
            expNum.val=~t
            expNum.tipo = TS.TIPO_DATO.INT
            return expNum.val
        else:
            print('El valor ',temp,'no pude ser operado en binario por un NOT, se esperaba un tipo INT o FLOAT')
            err = 'Error el valor ',temp,'no pude ser operado en binario por un NOT, se esperaba un tipo INT o FLOAT',' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
            errores.append(err)   
   
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
                err = 'Error de tipos ',exp1,' y ',exp2,'no se pueden operar en un AND bit a bit se espera que ambos sean INT o FLOAT',' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
                errores.append(err) 
        else:
            print ('error de tipos ',exp1,' y ',exp2,'no se pueden operar en un AND bit a bit se espera que ambos sean INT o FLOAT')
            err = 'Error de tipos ',exp1,' y ',exp2,'no se pueden operar en un AND bit a bit se espera que ambos sean INT o FLOAT',' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
            errores.append(err) 
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
                err = 'Error de tipos ',exp1,' y ',exp2,'no se pueden operar en un OR bit a bit se espera que ambos sean INT o FLOAT',' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
                errores.append(err) 
        else:
            print ('error de tipos ',exp1,' y ',exp2,'no se pueden operar en un OR bit a bit se espera que ambos sean INT o FLOAT')
            err = 'Error de tipos ',exp1,' y ',exp2,'no se pueden operar en un OR bit a bit se espera que ambos sean INT o FLOAT',' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
            errores.append(err) 
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
                err = 'Error de tipos ',exp1,' y ',exp2,'no se pueden operar en un XOR bit a bit se espera que ambos sean INT o FLOAT',' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
                errores.append(err) 
        else:
            print ('error de tipos ',exp1,' y ',exp2,'no se pueden operar en un XOR bit a bit se espera que ambos sean INT o FLOAT')
            err = 'Error de tipos ',exp1,' y ',exp2,'no se pueden operar en un XOR bit a bit se espera que ambos sean INT o FLOAT',' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
            errores.append(err) 
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
                err = 'Error de tipos ',exp1,' y ',exp2,'no se pueden operar en un CORR IZQ bit a bit se espera que ambos sean INT o FLOAT',' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
                errores.append(err) 
        else:
            print ('error de tipos ',exp1,' y ',exp2,'no se pueden operar en un CORR IZQ bit a bit se espera que ambos sean INT o FLOAT')
            err = 'Error de tipos ',exp1,' y ',exp2,'no se pueden operar en un CORR IZQ bit a bit se espera que ambos sean INT o FLOAT',' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
            errores.append(err) 
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
                err = 'Error de tipos ',exp1,' y ',exp2,'no se pueden operar en un CORR DER bit a bit se espera que ambos sean INT o FLOAT',' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
                errores.append(err) 
        else:
            print ('error de tipos ',exp1,' y ',exp2,'no se pueden operar en un CORR DER bit a bit se espera que ambos sean INT o FLOAT')
            err = 'Error de tipos ',exp1,' y ',exp2,'no se pueden operar en un CORR DER bit a bit se espera que ambos sean INT o FLOAT',' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
            errores.append(err) 
    elif isinstance (expNum,ExpresionLogica):
        return resolver_expresion_logica(expNum,ts)
    
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
    
    elif isinstance(expNum,AccesoValorArray):

        temporal = ts.obtener(expNum.id).valor

        for j in range(len(expNum.lista)):
            ind = resolver_expresion_aritmetica(expNum.lista[j],ts)
            if (j==(len(expNum.lista)-1)):

                temporal = temporal.get(ind)
                if temporal == None:
                    print('Error, no existe un valor en el indice: ',ind)
                    err = 'Error, no existe un valor en el indice: ',ind,' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
                    errores.append(err) 
            else:
                temporal_aux = temporal.get(ind)
                if temporal_aux == None:
                    print('Error, no existe un valor en el indice: ',ind)
                    err = 'Error, no existe un valor en el indice: ',ind,' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
                    errores.append(err) 
                else:
                    temporal = temporal.get(ind)

        if isinstance (temporal,str): expNum.tipo = td.CADENA
        elif isinstance(temporal,int): expNum.tipo = td.INT
        elif isinstance(temporal,float): expNum.tipo = td.FLOAT
        elif isinstance (temporal,dict): expNum.tipo = td.ARRAY
        return temporal            
    
    elif isinstance(expNum,Read):
        val = M()
        res = val.getInteger()
        val.cerrar()
        patronFloat = re.compile('([0-9]+(\.)[0-9]+){1}')
        patronNum = re.compile('[0-9]+')
        if patronFloat.match(res):
            expNum.val = float(res)
            expNum.tipo = td.FLOAT
        elif patronNum.match(res):
            expNum.val = int(res)
            expNum.tipo = td.INT
        else:
            expNum.val = str(res)
            expNum.tipo = td.CADENA
        return expNum.val
    
    else:
        print(expNum)
        err = 'Error, no existe un valor en el indice: ',ind,' En la linea: ',expNum.linea,' En la columna: ',expNum.columna, 'Tipo: SEMANTICO'
        errores.append(err) 

def procesar_unset(exp, ts):
    
    if isinstance(exp.exp,ExpresionTemporal):
        temp = exp.exp.id
        ts.eliminar(temp)
    else:
        print('El valor ',exp.exp.id,'no puede ser ejecutado por unset(), se esperaba un registro')
        err = 'Error el valor ',exp.exp.id,'no puede ser ejecutado por unset(), se esperaba un registro',' En la linea: ',exp.linea,' En la columna: ',exp.columna, 'Tipo: SEMANTICO'
        errores.append(err) 

def procesar_inicioPila(instr,ts):
    pila = TS.Simbolo(instr.id,td.PILA,[],Etiqueta)
    if ts.existeSimbolo(pila):
        print('La pila ya existe')
        err = 'Error el valor ',instr.id,'La pila ya existe',' En la linea: ',instr.linea,' En la columna: ',instr.columna, 'Tipo: SEMANTICO'
        errores.append(err) 
    else:
        ts.agregar(pila)

def procesar_asignacion_punteropila(instr,ts):
    valor=resolver_expresion_aritmetica(instr.exp,ts)
    punteropila = TS.Simbolo(instr.id,td.INT,valor,Etiqueta)
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

        nuevapila = TS.Simbolo(instr.id,td.PILA,pila,Etiqueta)

        if ts.existeSimbolo(nuevapila):
            ts.actualizar(nuevapila)
        else:
            print('error pila',instr.id,'no existe')
            err = 'Error pila',instr.id,'no existe',' En la linea: ',instr.linea,' En la columna: ',instr.columna, 'Tipo: SEMANTICO'
            errores.append(err) 
    except :
        print('error en asignacion de valor a la pila')

def procesar_asignacion_extra (instr,ts):
    try:
        val = resolver_expresion_aritmetica(instr.exp, ts)
        simbolo = TS.Simbolo(instr.id, instr.exp.tipo, val,Etiqueta)
        if ts.existeSimbolo(simbolo) :
            ts.actualizar(simbolo)
        else:
            ts.agregar(simbolo)
    except :
        print('No se puede realizar la asignacion de',instr.id)
        err = 'Error No se puede realizar la asignacion de',instr.id,' En la linea: ',instr.linea,' En la columna: ',instr.columna, 'Tipo: SEMANTICO'
        errores.append(err) 
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
    global Etiqueta
    Etiqueta=str(instr.id)

def Llamada_goto(instr,ts,listasiguientes):  
    siguientes = []
    i = 0
    for ins in listasiguientes:
        if isinstance(ins,Label):
            global Etiqueta
            Etiqueta = str(instr.id)
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
            elif isinstance(instr, Main): Etiqueta = 'Main'
            elif isinstance(instr,Asigna_arreglo): procesar_asignacion_arreglo(instr,ts)
            elif isinstance(instr,Label): procesa_Label(instr,ts)
            elif isinstance(instr,Exit): return
            elif isinstance(instr,Goto):
                Llamada_goto(instr,ts, listaglobal)
                return
            else : 
                print('Error: instrucción no válida', instr)
                err = 'Error: instrucción no válida', instr,' En la linea: ',instr.linea,' En la columna: ',instr.columna, 'Tipo: SEMANTICO'
                errores.append(err) 


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
            elif isinstance(instr, Main): 
                global Etiqueta
                Etiqueta = 'Main'
            elif isinstance(instr,Asigna_arreglo): procesar_asignacion_arreglo(instr,ts)
            elif isinstance(instr,Label): procesa_Label(instr,ts)
            elif isinstance(instr,Exit): return
            elif isinstance(instr,Goto): 
                Llamada_goto(instr,ts, instrucciones)
                return
            
            else : 
                err = 'Error: instrucción no válida', instr,' En la linea: ',instr.linea,' En la columna: ',instr.columna, 'Tipo: SEMANTICO'
                errores.append(err) 

    else:
        print('Error la etiqueta main no esta al inicio del programa o no existe')
        err = 'Error la etiqueta main no esta al inicio del programa o no existe',' En la linea: ',instr.linea,' En la columna: ',instr.columna, 'Tipo: SEMANTICO'
        errores.append(err) 
#-----------------------------------------------------------TERMINA ANALISIS SEMANTICO
#------------------------------------------DEBUGGER
def procesar_instrucciones_debugger(instrucciones, ts, i) :
    ## lista de instrucciones recolectadas
    if isinstance(instrucciones[0],Main):
        if i <= len(instrucciones):
            if isinstance(instrucciones[i], Imprimir) : procesar_imprimir(instrucciones[i], ts)
            elif isinstance(instrucciones[i], Definicion) : procesar_definicion(instrucciones[i], ts)
            elif isinstance(instrucciones[i], Asignacion) : procesar_asignacion(instrucciones[i], ts)
            elif isinstance(instrucciones[i], Mientras) : procesar_mientras(instrucciones[i], ts)
            elif isinstance(instrucciones[i], If) : procesar_if(instrucciones[i], ts)
            elif isinstance(instrucciones[i], IfElse) : procesar_if_else(instrucciones[i], ts)
            elif isinstance(instrucciones[i], Unset) : procesar_unset(instrucciones[i],ts)
            elif isinstance(instrucciones[i],IniciaPila): procesar_inicioPila(instrucciones[i],ts)
            elif isinstance(instrucciones[i],AsignaPunteroPila): procesar_asignacion_punteropila(instrucciones[i],ts)
            elif isinstance(instrucciones[i],AsignaValorPila): procesar_asignacion_pila(instrucciones[i],ts)
            elif isinstance(instrucciones[i], AsignacionExtra): procesar_asignacion_extra(instrucciones[i],ts)
            elif isinstance(instrucciones[i], Main):
                global Etiqueta
                Etiqueta = 'Main'
            elif isinstance(instrucciones[i],Asigna_arreglo): procesar_asignacion_arreglo(instrucciones[i],ts)
            elif isinstance(instrucciones[i],Label): procesa_Label(instrucciones[i],ts)
            elif isinstance(instrucciones[i],Exit): return
            elif isinstance(instrucciones[i],Goto): 
                Llamada_goto(instrucciones[i],ts, instrucciones)
                return
            
            else : 
                err = 'Error: instrucción no válida', instrucciones[i],' En la linea: ',instrucciones[i].linea,' En la columna: ',instrucciones[i].columna, 'Tipo: SEMANTICO'
                errores.append(err) 
        else:
            insta = M()
            insta.OkMessage()
            insta.cerrar()
            return
    else:
        print('Error la etiqueta main no esta al inicio del programa o no existe')
        err = 'Error la etiqueta main no esta al inicio del programa o no existe',' En la linea: ',instrucciones[i].linea,' En la columna: ',instrucciones[i].columna, 'Tipo: SEMANTICO'
        errores.append(err) 

#-----------------------------------------FINALIZA DEBUGGER
#-----------------------------------------------------------INICIA GRAFICACION DEL AST
def dibujar_exit(instr,root,cont):
    cont=cont+1
    nodo = 'nodo'+ str(cont)
    dot.node(nodo,'Exit')
    dot.edge(root, nodo)

    return cont

def dibujar_Goto(instr,root,cont):
    cont=cont+1
    nodo = 'nodo'+ str(cont)
    dot.node(nodo,'Goto')
    dot.edge(root, nodo)

    cont=cont+1
    nodo1 = 'nodo'+ str(cont)
    dot.node(nodo1,str(instr.id))
    dot.edge(nodo, nodo1)
    return cont

def dibujar_Label(instr,root,cont):
    cont=cont+1
    nodo = 'nodo'+ str(cont)
    dot.node(nodo,'Etiqueta')
    dot.edge(root, nodo)

    cont=cont+1
    nodo1 = 'nodo'+ str(cont)
    dot.node(nodo1,str(instr.id))
    dot.edge(nodo, nodo1)
    return cont

def dibujar_Asigna_arreglo(instr,root,cont):
    cont=cont+1
    nodo = 'nodo'+ str(cont)
    dot.node(nodo,'AsignaArreglo')
    dot.edge(root, nodo)

    cont=cont+1
    nodo1 = 'nodo'+ str(cont)
    dot.node(nodo1,str(instr.id))
    dot.edge(nodo, nodo1)

    dot.node(nodo1,instr.id)
    cont = cont +1
    nodo2= 'nodo'+str(cont)
    dot.node(nodo2,"acceso")
    dot.edge(nodo,nodo2)

    for i in instr.lista:
        cont = dibujar_expresion(i,nodo2,cont)
    cont = dibujar_expresion(instr.exp,nodo,cont)
    return cont  

def dibujar_main(instr,root,cont):
    cont=cont+1
    nodo = 'nodo'+ str(cont)
    dot.node(nodo,'Etiqueta')
    dot.edge(root, nodo)

    cont=cont+1
    nodo1 = 'nodo'+ str(cont)
    dot.node(nodo1,'Main')
    dot.edge(nodo, nodo1)

    return cont

def dibujar_AsignaRegistro(instr,root,cont):
    cont=cont+1
    nodo = 'nodo'+ str(cont)
    dot.node(nodo,'AsignaRegistro')
    dot.edge(root, nodo)

    cont=cont+1
    nodo1 = 'nodo'+ str(cont)
    dot.node(nodo1,str(instr.id))
    dot.edge(nodo, nodo1)

    cont = dibujar_expresion(instr.exp,nodo,cont)

    return cont

def dibujar_AsignaValorPila(instr,root,cont):
    cont=cont+1
    nodo = 'nodo'+ str(cont)
    dot.node(nodo,'AsignaValorPila')
    dot.edge(root, nodo)

    cont=cont+1
    nodo1 = 'nodo'+ str(cont)
    dot.node(nodo1,str(instr.id))
    dot.edge(nodo, nodo1)

    cont=cont+1
    nodo2 = 'nodo'+ str(cont)
    dot.node(nodo2,str(instr.puntero))
    dot.edge(nodo, nodo2)

    cont = dibujar_expresion(instr.exp,nodo,cont)
    return cont

def dibujar_AsignaPunteroPila(instr,root,cont):
    cont=cont+1
    nodo = 'nodo'+ str(cont)
    dot.node(nodo,'AsignaPunteroPila')
    dot.edge(root, nodo)

    cont=cont+1
    nodo1 = 'nodo'+ str(cont)
    dot.node(nodo1,str(instr.id))
    dot.edge(nodo, nodo1)

    cont = dibujar_expresion(instr.exp,nodo,cont)

    return cont

def dibujar_unset(instr,root,cont):
    cont=cont+1
    nodo = 'nodo'+ str(cont)
    dot.node(nodo,'Unset')
    dot.edge(root, nodo)

    cont = dibujar_expresion(instr.exp,nodo,cont)

    return cont

def dibujar_IniciaPila(instr,root,cont):
    cont=cont+1
    nodo = 'nodo'+ str(cont)
    dot.node(nodo,'IniciaPila')
    dot.edge(root, nodo)

    cont=cont+1
    nodo1 = 'nodo'+ str(cont)
    dot.node(nodo1,str(instr.id))
    dot.edge(nodo, nodo1)
    return cont

def dibujar_if(instr,root,cont):
    cont=cont+1
    nodo = 'nodo'+ str(cont)
    dot.node(nodo,'If')
    dot.edge(root, nodo)

    cont = dibujar_expresion(instr.exp,nodo,cont)

    cont= dibujar_Goto(instr.goto,nodo,cont)

    return cont

def dibujar_asignacion(instr,root,cont):
    cont=cont+1
    nodo = 'nodo'+ str(cont)
    dot.node(nodo,'Asignacion')
    dot.edge(root, nodo)
    cont = cont +1
    nodo1= 'nodo'+str(cont)
    dot.node(nodo1,instr.id)
    dot.edge(nodo,nodo1)
    cont = dibujar_expresion(instr.expNumerica,nodo,cont)
    return cont

def dibujar_print(instr,root,cont):
    cont=cont+1
    nodo = 'nodo'+ str(cont)
    dot.node(nodo,'Print')
    dot.edge(root, nodo)

    cont = dibujar_expresion(instr.exp,nodo,cont)

    return cont

def dibujar_expresion(instr,root,cont):
    cont +=1
    nodo = 'nodo'+str(cont)
    dot.node(nodo,'Exp')
    dot.edge(root,nodo)
    
    cont = cont +1
    nodo1= 'nodo'+str(cont)
    
    if isinstance(instr,ExpresionNumero):
        dot.node(nodo1,str(instr.val))  
    elif isinstance(instr, ExpresionTemporal):  
        dot.node(nodo1,instr.id)
    elif isinstance(instr,ExpresionBinaria):    
        cont = dibujar_expresion(instr.exp1,nodo1,cont) 
        dot.node(nodo1,str(instr.operador.name))
        cont = dibujar_expresion(instr.exp2,nodo1,cont)
    elif isinstance(instr,ExpresionNegativo):
        dot.node(nodo1,'-')
        cont = dibujar_expresion(instr.exp,nodo1,cont)
    elif isinstance(instr,ExpresionBitNot):
        dot.node(nodo1,'~')
        cont = dibujar_expresion(instr.exp,nodo1,cont)
    elif isinstance(instr,ExpresionBitAnd):
        cont = dibujar_expresion(instr.exp1,nodo1,cont) 
        dot.node(nodo1,'And bit')
        cont = dibujar_expresion(instr.exp2,nodo1,cont)
    elif isinstance(instr,ExpresionBitOr):
        cont = dibujar_expresion(instr.exp1,nodo1,cont) 
        dot.node(nodo1,'Or bit')
        cont = dibujar_expresion(instr.exp2,nodo1,cont)
    elif isinstance(instr,ExpresionBitXor):
        cont = dibujar_expresion(instr.exp1,nodo1,cont) 
        dot.node(nodo1,'Xor bit')
        cont = dibujar_expresion(instr.exp2,nodo1,cont)
    elif isinstance(instr,ExpresionBitIzq):
        cont = dibujar_expresion(instr.exp1,nodo1,cont) 
        dot.node(nodo1,'Corr Izq')
        cont = dibujar_expresion(instr.exp2,nodo1,cont)
    elif isinstance(instr,ExpresionBitDer):
        cont = dibujar_expresion(instr.exp1,nodo1,cont) 
        dot.node(nodo1,'Corr Der')
        cont = dibujar_expresion(instr.exp2,nodo1,cont)     
    elif isinstance(instr, ExpresionPunteroTemp):  
        dot.node(nodo1,instr.id)
    elif isinstance(instr,ExpresionConversion):
        dot.node(nodo1,'Conversion')
        dot.node(nodo1,str(instr.tipo))
        cont = dibujar_expresion(instr.exp,nodo,cont)
    elif isinstance(instr, ExpresionPila):  
        dot.node(nodo1,instr.id)
    elif isinstance(instr, ExpresionPunteroPila):  
        dot.node(nodo1,instr.id)
    elif isinstance(instr, Expresion_Pop_pila):  
        dot.node(nodo1,instr.idPila)
        dot.node(nodo1,instr.puntero)
    elif isinstance(instr, InicioArray):
        dot.node(nodo1,"Inicia Array") 
    elif isinstance(instr, ExpresionValorAbsoluto):
        dot.node(nodo1,'ABS')
        cont = dibujar_expresion(instr.exp,nodo1,cont) 
    elif isinstance(instr, ExpresionLogica):
        cont = dibujar_expresion(instr.exp1,nodo1,cont) 
        dot.node(nodo1,str(instr.operador.name))
        cont = dibujar_expresion(instr.exp2,nodo1,cont)
    elif isinstance(instr,ExpresionLogicaXOR):
        cont = dibujar_expresion(instr.exp1,nodo1,cont) 
        dot.node(nodo1,'Xor')
        cont = dibujar_expresion(instr.exp2,nodo1,cont)  
    elif isinstance(instr,ExpresionLogicaAND):
        cont = dibujar_expresion(instr.exp1,nodo1,cont) 
        dot.node(nodo1,'And')
        cont = dibujar_expresion(instr.exp2,nodo1,cont)    
    elif isinstance(instr,ExpresionLogicaOR):
        cont = dibujar_expresion(instr.exp1,nodo1,cont) 
        dot.node(nodo1,'Or')
        cont = dibujar_expresion(instr.exp2,nodo1,cont)  
    elif isinstance(instr,ExpresionLogicaNot):
        dot.node(nodo1,'!')
        cont = dibujar_expresion(instr.exp,nodo1,cont)
    elif isinstance(instr,Expresion_param):
        dot.node(nodo1,instr.id)
    elif isinstance(instr,AccesoValorArray):
        dot.node(nodo1,instr.id)
        cont = cont +1
        nodo2= 'nodo'+str(cont)
        dot.node(nodo2,"acceso")
        dot.edge(nodo,nodo2)

        for i in instr.lista:
            cont = dibujar_expresion(i,nodo2,cont)
    elif isinstance(instr,Read):
        dot.node(nodo1,"Read ( )") 

    dot.edge(nodo,nodo1)

    return cont

def DibujarAST(instrucciones):
    cont = 1
    root = 'nodo'+ str(cont)
    dot.node(root, 'AUGUS')
    for instr in instrucciones:
        if isinstance(instr,Asignacion) : cont = dibujar_asignacion(instr,root,cont)
        elif isinstance(instr,Imprimir) : cont = dibujar_print(instr,root,cont)
        elif isinstance(instr,If): cont = dibujar_if(instr,root,cont)
        elif isinstance(instr,Unset): cont = dibujar_unset(instr,root,cont)
        elif isinstance(instr,IniciaPila): cont = dibujar_IniciaPila(instr,root,cont)
        elif isinstance(instr,AsignaPunteroPila): cont = dibujar_AsignaPunteroPila(instr,root,cont)
        elif isinstance(instr,AsignaValorPila): cont = dibujar_AsignaValorPila(instr,root,cont)
        elif isinstance(instr,AsignacionExtra): cont = dibujar_AsignaRegistro(instr,root,cont)
        elif isinstance(instr,Main): cont = dibujar_main(instr,root,cont)
        elif isinstance(instr,Asigna_arreglo): cont=dibujar_Asigna_arreglo(instr,root,cont)
        elif isinstance(instr,Label): cont=dibujar_Label(instr,root,cont)
        elif isinstance(instr,Goto): cont=dibujar_Goto(instr,root,cont)
        elif isinstance(instr,Exit): cont=dibujar_exit(instr,root,cont)
        else : 
            print('')
    #print(dot.source)

#------------------------------------------------------------REPORTES
def ReporteTS():
    generado = '<<table border=\'0\' cellborder=\'1\' color=\'blue\' cellspacing='+'\'0\''+'><tr><td colspan=\'5\'>TABLA DE SIMBOLOS</td></tr><tr><td>No.</td><td>identificador</td><td>valor</td><td>tipo</td><td>Etiqueta</td></tr>'
    cont = 0

    for i in ts_global.simbolos:
        generado += '<tr><td>'+str(cont)+'</td><td>'+str(ts_global.obtener(i).id)+'</td><td>'+str(ts_global.obtener(i).valor)+'</td><td>'+str(ts_global.obtener(i).tipo.name)+'</td><td>'+str(ts_global.obtener(i).amb)+'</td></tr>'
        cont +=1
    generado +=' </table>>'

    dotTS = Digraph('Tabla de simbolos',filename='TablaSimbolos')
    #print(generado)
    dotTS.attr('node',shape='plaintext')
    dotTS.node('node',label=generado)
    dotTS.view()

def ReporteErrores():
    generado = '<<table border=\'0\' cellborder=\'1\' color=\'blue\' cellspacing='+'\'0\''+'><tr><td colspan=\'2\'>LISTADO DE ERRORES</td></tr><tr><td>No.</td><td>Error</td></tr>'
    cont = 0

    for i in errores:
        generado +='<tr><td>'+str(cont)+'</td><td>'+str(i)+'</td></tr>'
        cont +=1
    
    generado +=' </table>>'
    dotErr = Digraph('Errores',filename='ListadoDeErrores')
    #print(generado)
    dotErr.attr('node',shape='plaintext')
    dotErr.node('node',label=generado)
    dotErr.view()

def ReporteGramatical():
    generado = '<<table border=\'0\' cellborder=\'1\' color=\'blue\' cellspacing='+'\'0\''+'><tr><td colspan=\'2\'>REPORTE GRAMATICAL</td></tr><tr><td>No.</td><td>Producciones</td></tr>'
    cont = 0

    aux = list(reversed(gram))
    for i in aux:
        generado += '<tr><td>'+str(cont)+'</td><td align = \'left\'>'+str(i)+'</td></tr>'
        cont +=1
    generado +=' </table>>'

    dotTS = Digraph('Reporte Gramatical',filename='ReporteGramatical')

    dotTS.attr('node',shape='plaintext')
    dotTS.node('node',label=generado)
    dotTS.view()
#-----------------------------------------------------------TERMINA GRAFICACION DEL AST

#-----------------------------------------------------------EJECUCION DEL ANALIZADOR




#INICIALIZACION DE VARIABLES
ts_global = TS.TablaDeSimbolos()
gram = []
instrucciones=[]
errores= []
dot = Digraph('AST',filename='AST')
resultado = ''
#ANALIZADOR ASCENDENTE
def ejecutar_asc(input):
    import gramatica as g
    global gram
    global instrucciones
    gram = g.verGramatica()
    instrucciones = g.parse(input) 
    procesar_instrucciones(instrucciones, ts_global)   

def errores_asc():
    import gramatica as g
    global errores
    errores = g.retornalista()
    return errores 

#ANALIZADOR DESCENDENTE
def ejecutar_desc(input):
    import gramaticadesc as gdes
    global gram
    global instrucciones
    instrucciones = gdes.parse(input)
    gram = gdes.verGramatica()
    procesar_instrucciones(instrucciones, ts_global)   
    return instrucciones

def errores_desc():
    import gramaticadesc as gdes
    global errores
    errores = gdes.retornalista()
    return errores

def GenerarAST():
    try:
        DibujarAST(instrucciones)
        dot.view()
    except :
        print('error al imprimir arbol')
        pass

def RecibirSalida():
    global resultado
    nuevo = copy.copy(resultado)
    return nuevo
   
def ejecutar_debug(input,i):
    import gramatica as l
    global gram
    global instrucciones
    try:
        gram = l.verGramatica()
        instrucciones = l.parse(input) 
        procesar_instrucciones_debugger(instrucciones,ts_global,i)
    except :
        s = M()
        s.OkMessage()
        s.cerrar()


class objetopila():

    def __init__(self, valor, tipo):
        self.valor = valor
        self.tipo = tipo


        