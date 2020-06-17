#-------------------------------------------------ANALIZADOR LEXICO
reservadas = {
    'numero' : 'NUMERO',
    'mientras' : 'MIENTRAS',
    'if' : 'IF',
    'else' : 'ELSE',
    'main' : 'MAIN',
    'goto':'GOTO',
    'unset':'UNSET',
    'print':'PRINT',
    'read':'READ',
    'exit':'EXIT',
    'int':'INT',
    'float':'FLOAT',
    'char':'CHAR',
    'array':'ARRAY',
    'abs':'ABS',
    'xor':'XORLOG'
}

tokens  = [
    'PTCOMA',
    'LLAVIZQ',
    'LLAVDER',
    'PARIZQ',
    'PARDER',
    'IGUAL',
    'MAS',
    'MENOS',
    'POR',
    'DIVIDIDO',
    'ANDBIT',
    'MENQUE',
    'MAYQUE',
    'IGUALQUE',
    'NIGUALQUE',
    'DECIMAL',
    'ENTERO',
    'CADENA',
    'ID',
    'RES',
    'DOSP',
    'TEMPORAL',
    'NOTLOG',
    'ANDLOG',
    'ORLOG',
    'NOTBIT',
    'ORBIT',
    'XORBIT',
    'IZQBIT',
    'DERBIT',
    'MAYORIG',
    'MENORIG',
    'PTEMPORAL',
    'CADE',
    'CORIZQ',
    'CORDER',
    'PILAPOS',
    'PILAPUNTERO',
    'PARAMETRO',
    'VALORDEVUELTO',
    'DIRRETORNO'

    
    
] + list(reservadas.values())

# Tokens
t_PTCOMA    = r';'
t_LLAVIZQ   = r'{'
t_LLAVDER   = r'}'
t_PARIZQ    = r'\('
t_PARDER    = r'\)'
t_IGUAL     = r'='
t_MAS       = r'\+'
t_MENOS     = r'-'
t_POR       = r'\*'
t_DIVIDIDO  = r'/'
t_RES       = r'%'
t_MAYORIG   = r'>='
t_MENORIG   = r'<='
t_MENQUE    = r'<'
t_MAYQUE    = r'>'
t_IGUALQUE  = r'=='
t_NIGUALQUE = r'!='
t_DOSP      = r':'
t_NOTLOG    = r'!'
t_ANDLOG    = r'&&'
t_ORLOG     = r'\|\|'
t_NOTBIT    = r'~'
t_ANDBIT    = r'&'
t_ORBIT     = r'\|'
t_XORBIT    = r'\^'
t_IZQBIT    = r'<<'
t_DERBIT    = r'>>'
t_CORIZQ    = r'\['
t_CORDER    = r'\]'


def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_ID(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = reservadas.get(t.value.lower(),'ID')    # Check for reserved words
     return t

def t_TEMPORAL(t):
    r'\$(t[0-9]+)'
    t.value = str(t.value)
    return t

def t_PTEMPORAL(t):
    r'\&\$(t[0-9]+)'
    t.value = str(t.value)
    return t

def t_PARAMETRO(t):
    r'\$[a][0-9]+'
    t.value = str(t.value)
    return t

def t_VALORDEVUELTO(t):
    r'\$[v][0-9]+'
    t.value = str(t.value)
    return t

def t_DIRRETORNO(t):
    r'\$[r][a]'
    t.value = str(t.value)
    return t

def t_PILAPOS(t):
    r'\$[s][0-9]+'
    t.value = str(t.value)
    return t

def t_PILAPUNTERO(t):
    r'\$[s][p]'
    t.value = str(t.value)
    return t

def t_FUNCION(t):
    r'[f][0-9]+'
    t.value = str(t.value)
    return t

def t_RETORNO(t):
    r'[r][0-9]+'
    t.value = str(t.value)
    return t

def t_CADENA(t):
    r'\'.*?\''
    t.value = t.value[1:-1] # remuevo las comillas
    return t 

def t_CADE(t):
    r'\".*?\"'
    t.value = t.value[1:-1] # remuevo las comillas
    return t 


def t_LABEL(t):
    r'[a-zA-Z]+'
    t.value = str(t.value)
    return t 

# Comentario de múltiples líneas /* .. */
def t_COMENTARIO_MULTILINEA(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')

# Comentario simple #...
def t_COMENTARIO_SIMPLE(t):
    r'\#.*\n'
    t.lexer.lineno += 1

# Caracteres ignorados
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Error Lexico en el token: '%s'" % t.value[0])
    err = "Error Lexico en el token: '%s'" % t.value[0]
    lista_errores.append(err)
    t.lexer.skip(1)

#OBTENIENDO LA COLUMNA 
def get_clomuna(input, token):
    line_star = input.rfind('\n', 0 ,token.lexpos) + 1
    return (token.lexpos - line_star)+1

# Construyendo el analizador léxico
import ply.lex as lex
lexer = lex.lex()


# Asociación de operadores y precedencia
precedence = (
    ('right','NOTLOG'),
    ('left','ANDLOG','ORLOG','XORLOG'),
    ('left','IGUALQUE','NIGUALQUE'),
    ('left','MENQUE','MAYQUE'),
    ('left','MAYORIG','MENORIG'),
    ('right','NOTBIT'),
    ('left','XORBIT'),
    ('left','ANDBIT','ORBIT'),
    ('left','IZQBIT','DERBIT'),
    ('left','MAS','MENOS'),
    ('left','POR','DIVIDIDO'),
    ('left','RES','ABS'),
    ('right','UMENOS')
    )

# Definición de la gramática

from expresiones import *
from instrucciones import *

asc=[]
def p_init(t) :
    'init            : instrucciones'
    l = list(reversed(t[1]))
    t[0] = l
    asc.append("init - instrucciones")
def p_instrucciones_lista(t) :
    'instrucciones    :  instruccion instruccionesP'
    t[0]=t[2]
    t[0].append(t[1])
    asc.append('instrucciones - instruccion instruccionesP')
def p_instrucciones_instruccion(t) :
    'instruccionesP    : instruccion instruccionesP'
    t[0]=t[2]
    t[0].append(t[1])
    asc.append('instruccionesP - instruccion instruccionesP')
def p_instrucciones_empty(t):
    'instruccionesP : VACIO'
    t[0]=[]
    asc.append('instruccionesP - VACIO')
def p_vacio(t):
    'VACIO : '
    asc.append('VACIO - Epsilon')
    pass

def p_instruccion(t) :
    '''instruccion      : imprimir_instr
                        | asignacion_instr
                        | if_instr
                        | INICIO
                        | UNSETF
                        | EXITF
                        | ASIGNAARREGLO
                        | INICIAPILA
                        | ASIGNAPUNTERO
                        | ASIGNAPILA
                        | ASIGNACIONEXTRA
                        | DEFINEL
                        | DEFINEGOTO'''
    t[0] = t[1]
    if isinstance(t[1],Label): asc.append("instruccion - DEFINEL")
    elif isinstance(t[1],Imprimir): asc.append('instruccion - imprimir_instr')
    elif isinstance(t[1],Asignacion): asc.append('instruccion - asignacion_instr')
    elif isinstance(t[1],If): asc.append('instruccion - if_instr')
    elif isinstance(t[1],Main): asc.append('instruccion - INICIO')
    elif isinstance(t[1],Unset): asc.append('instruccion - UNSETF')
    elif isinstance(t[1],Exit): asc.append('instruccion - EXITF')
    elif isinstance(t[1],Asigna_arreglo): asc.append('instruccion - ASIGNAARREGLO')
    elif isinstance(t[1],IniciaPila): asc.append('instruccion - INICIAPILA')
    elif isinstance(t[1],AsignaPunteroPila): asc.append('instruccion - ASIGNAPUNTERO')
    elif isinstance(t[1],AsignaValorPila): asc.append('instruccion - ASIGNAPILA')
    elif isinstance(t[1],AsignacionExtra): asc.append('instruccion - ASIGNACIONEXTRA')
    elif isinstance(t[1],Goto): asc.append('instruccion - DEFINEGOTO')
    else:
        asc.append('instruccion - OTRO')

#RECIBE main:
def p_INICIO(t):
    'INICIO : MAIN DOSP'
    t[0] = Main(t.lineno(1),get_clomuna(entry,t.slice[1]))
    asc.append('INICIO - MAIN DOSP')
#Recibe: exit;
def p_EXITF(t):
    'EXITF : EXIT PTCOMA'
    t[0]= Exit(t.lineno(1),get_clomuna(entry,t.slice[1]))
    asc.append('EXITF - EXIT PTCOMA')
#Recibe: print($t1);
def p_instruccion_imprimir(t) :
    'imprimir_instr     : PRINT PARIZQ expresion PARDER PTCOMA'
    t[0] =Imprimir(t[3],t.lineno(1),get_clomuna(entry,t.slice[1]))
    asc.append('imprimir_instr  - PRINT PARIZQ expresion_log_relacional PARDER PTCOMA')


#RECIBE: expresiones aritmeticas y bit a bit
def p_expresion_binaria(t):
    '''expresion :        expresion_numerica MAS expresion_numerica
                        | expresion_numerica MENOS expresion_numerica
                        | expresion_numerica POR expresion_numerica
                        | expresion_numerica DIVIDIDO expresion_numerica
                        | expresion_numerica RES expresion_numerica
                        | expresion_numerica ANDBIT expresion_numerica
                        | expresion_numerica ORBIT expresion_numerica
                        | expresion_numerica XORBIT expresion_numerica
                        | expresion_numerica IZQBIT expresion_numerica
                        | expresion_numerica DERBIT expresion_numerica
    '''
    if t[2] == '+'  : 
        t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.MAS,t.lineno(1),get_clomuna(entry,t.slice[2]))
        asc.append('expresion - expresion_numerica MAS expresion_numerica')
    elif t[2] == '-': 
        t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.MENOS,t.lineno(1),get_clomuna(entry,t.slice[2]))
        asc.append('expresion - expresion_numerica MENOS expresion_numerica')    
    elif t[2] == '*': 
        t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.POR,t.lineno(1),get_clomuna(entry,t.slice[2]))
        asc.append('expresion - expresion_numerica POR expresion_numerica')    
    elif t[2] == '/': 
        t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.DIVIDIDO,t.lineno(1),get_clomuna(entry,t.slice[2]))
        asc.append('expresion - expresion_numerica DIVISION expresion_numerica') 
    elif t[2] == '%':
        t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.RESIDUO,t.lineno(1),get_clomuna(entry,t.slice[2]))
        asc.append('expresion - expresion_numerica RES expresion_numerica') 
    elif t[2] == '&': 
        t[0] = ExpresionBitAnd(t[1], t[3],t.lineno(1),get_clomuna(entry,t.slice[2]))
        asc.append('expresion - expresion_numerica ANDBIT expresion_numerica') 
    elif t[2] == '|': 
        t[0] = ExpresionBitOr(t[1], t[3],t.lineno(1),get_clomuna(entry,t.slice[2]))
        asc.append('expresion - expresion_numerica ORBIT expresion_numerica') 
    elif t[2] == '^': 
        t[0] = ExpresionBitXor(t[1], t[3],t.lineno(1),get_clomuna(entry,t.slice[2]))
        asc.append('expresion - expresion_numerica NOTBIT expresion_numerica') 
    elif t[2] == '<<': 
        t[0] = ExpresionBitIzq(t[1], t[3],t.lineno(1),get_clomuna(entry,t.slice[2]))
        asc.append('expresion - expresion_numerica CORRIZQ expresion_numerica') 
    elif t[2] == '>>': 
        t[0] = ExpresionBitDer(t[1], t[3],t.lineno(1),get_clomuna(entry,t.slice[2]))
        asc.append('expresion - expresion_numerica CORRDER expresion_numerica') 

def p_expresion_unaria(t):
    'expresion_numerica : MENOS expresion %prec UMENOS'
    t[0] = ExpresionNegativo(t[2],t.lineno(1),get_clomuna(entry,t.slice[1]))
    asc.append('expresion_numerica - MENOS expresion_numerica UMENOS')

def p_simp(t):
    'expresion : expresion_numerica'
    t[0]=t[1]
    asc.append('expresion - expresion_numerica')

#Recibe (Expresion)
def p_expresion_agrupacion(t):
    'expresion_numerica : PARIZQ expresion PARDER'
    t[0] = t[2]
    asc.append('expresion_numerica - PARIZQ expresion_log_relacional PARDER')

def p_expresion_number(t):
    '''expresion_numerica : ENTERO  '''
    t[0] = ExpresionNumero(t[1],TS.TIPO_DATO.INT,t.lineno(1),get_clomuna(entry,t.slice[1]))
    asc.append('expresion_numerica - ENTERO ')

def p_expresion_decimal(t):
    'expresion_numerica : DECIMAL'
    t[0] = ExpresionNumero(t[1],TS.TIPO_DATO.FLOAT,t.lineno(1),get_clomuna(entry,t.slice[1]))
    asc.append('expresion_numerica - DECIMAL ')

def p_expresion_id(t):
    'expresion_numerica   : ID'
    t[0] = ExpresionNumero(t[1],t.lineno(1),get_clomuna(entry,t.slice[1]))
    asc.append('expresion_numerica - ID ')

def p_expresion_pila(t):
    'expresion_numerica   : PILAPOS'
    t[0] = ExpresionPila(t[1],t.lineno(1),get_clomuna(entry,t.slice[1]))
    asc.append('expresion_numerica - PILAPOS ')

def p_puntero_pila(t):
    'expresion_numerica : PILAPUNTERO'
    t[0] = ExpresionPunteroPila(t[1],t.lineno(1),get_clomuna(entry,t.slice[1]))
    asc.append('expresion_numerica - PILAPUNTERO ')

def p_pop_pila(t):
    'expresion_numerica : PILAPOS CORIZQ PILAPUNTERO CORDER'
    t[0] = Expresion_Pop_pila(t[1],t[3],t.lineno(1),get_clomuna(entry,t.slice[1]))
    asc.append('expresion_numerica - PILAPOS CORIZQ PILAPUNTERO CORDER ')

def p_expresion_parametro(t):
    '''expresion_numerica :    PARAMETRO
                            | VALORDEVUELTO
                            | DIRRETORNO'''
    t[0] = Expresion_param(t[1],t.lineno(1),get_clomuna(entry,t.slice[1]))
    asc.append('expresion_numerica - REGISTRO ')

# Recibe temporales $t2
def p_expresion_tempo(t):
    'expresion_numerica : TEMPORAL'
    t[0] = ExpresionTemporal(t[1],t.lineno(1),get_clomuna(entry,t.slice[1]))                   
    asc.append('expresion_numerica - TEMPORAL ')

# recibe: punteros  &$t1  
def p_expresion_puntero(t):
    'expresion_numerica : PTEMPORAL'
    t[0] = ExpresionPunteroTemp(t[1],t.lineno(1),get_clomuna(entry,t.slice[1]))
    asc.append('expresion_numerica - PTEMPORAL ')

#recibe: cadena 'hola'
def p_expresion_cadena(t) :
    'expresion_numerica     : CADENA'
    t[0] = ExpresionNumero(t[1], TS.TIPO_DATO.CADENA,t.lineno(1),get_clomuna(entry,t.slice[1]))
    asc.append('expresion_numerica - CADENA ')

#recibe: cadena "hola"
def p_expresion_cade(t) :
    'expresion_numerica     : CADE'
    t[0] = ExpresionNumero(t[1], TS.TIPO_DATO.CADENA,t.lineno(1),get_clomuna(entry,t.slice[1]))
    asc.append('expresion_numerica - CADE ')

#recibe: read()
def p_expresion_read(t):
    'expresion_numerica : READ PARIZQ PARDER'
    t[0] = Read(t.lineno(1),get_clomuna(entry,t.slice[1]))
    asc.append('expresion_numerica - READ PARIZQ PARDER ')

def p_inicializacion_array(t):
    'expresion_numerica : ARRAY PARIZQ PARDER'
    t[0]= InicioArray(t.lineno(1),get_clomuna(entry,t.slice[1]))
    asc.append('expresion_numerica - ARRAY PARIZQ PARDER')

def p_acceso_array_expresion(t):
    'expresion : TEMPORAL ACCESO'
    l = list(reversed(t[2]))
    t[0] = AccesoValorArray(t[1],l,t.lineno(1),get_clomuna(entry,t.slice[1]))
    asc.append('expresion - TEMPORAL ACCESO')

def p_acceso_lista_array(t):
    'ACCESO : CORIZQ expresion CORDER ACCESOP'
    t[0]=t[4]
    t[0].append(t[2])
    asc.append('ACCESO - CORIZQ expresion CORDER ACCESOP')
def p_acceso_array(t):
    'ACCESOP : CORIZQ expresion CORDER ACCESOP '
    t[0]=t[4]
    t[0].append(t[2])
    asc.append('ACCESOP - CORIZQ expresion CORDER ACCESOP ')
def p_acceso_array_empty(t):
    'ACCESOP : VACIO'
    t[0] = []
    asc.append('ACCESO - VACIO ')
#recibe: conversiones TIPOCONVERSION $t1 
def p_expresion_conversion(t):
    'expresion_numerica : TIPOCONVERSION expresion'
    t[0] = ExpresionConversion(t[1],t[2],t.lineno(1),get_clomuna(entry,t.slice[1]))
    asc.append('expresion_numerica - TIPOCONVERSION expresion ')

#recibe: tipo de conversion (int) (float) (char)
def p_expresion_tipoConversion(t):
    '''TIPOCONVERSION : PARIZQ INT PARDER
                    | PARIZQ FLOAT PARDER
                    | PARIZQ CHAR PARDER '''
    t[0]=t[2]
    asc.append('TIPOCONVERSION  - PARIZQ TIPOC PARDER ')

#Recibe: valor absoluto
def p_expresion_valorabs(t):
    'expresion_numerica : ABS PARIZQ expresion PARDER'
    t[0] =  ExpresionValorAbsoluto(t[3],t.lineno(1),get_clomuna(entry,t.slice[1]))
    asc.append('expresion_numerica - ABS PARIZQ expresion PARDER ')

def p_Label(t):
    'DEFINEL : ID DOSP'
    t[0] = Label(t[1],t.lineno(1),get_clomuna(entry,t.slice[1]))
    asc.append('DEFINEL - ID DOSP')

def p_Goto(t):
    'DEFINEGOTO : GOTO ID PTCOMA'
    t[0] = Goto(t[2],t.lineno(1),get_clomuna(entry,t.slice[1]))
    asc.append('DEFINEGOTO - GOTO ID PTCOMA')

def p_asigna_para_valorRet_ra(t):
    'ASIGNACIONEXTRA :  VALORESPARAM IGUAL expresion PTCOMA'
    t[0] = AsignacionExtra(t[1],t[3],t.lineno(1),get_clomuna(entry,t.slice[2]))
    asc.append('ASIGNACIONEXTRA -  VALORESPARAM IGUAL expresion PTCOMA')

def p_valoresSimp (t):
    '''VALORESPARAM :  PARAMETRO
                    | VALORDEVUELTO
                    | DIRRETORNO'''
    t[0]=t[1]
    asc.append('VALORESPARAM - REGISTRO')

def p_acceso_a_pila(t):
    'ASIGNAPILA : PILAPOS CORIZQ PILAPUNTERO CORDER IGUAL expresion PTCOMA'
    t[0]=AsignaValorPila(t[1],t[6],t[3],t.lineno(1),get_clomuna(entry,t.slice[1]))
    asc.append('ASIGNAPILA - PILAPOS CORIZQ PILAPUNTERO CORDER IGUAL expresion PTCOMA')

def p_asigna_puntero(t):
    'ASIGNAPUNTERO : PILAPUNTERO IGUAL expresion PTCOMA'
    t[0] = AsignaPunteroPila(t[1],t[3],t.lineno(1),get_clomuna(entry,t.slice[1]))
    asc.append('ASIGNAPUNTERO - PILAPUNTERO IGUAL expresion PTCOMA')

def p_inicia_pila(t):
    'INICIAPILA : PILAPOS IGUAL ARRAY PARIZQ PARDER PTCOMA'
    t[0] = IniciaPila(t[1],t.lineno(1),get_clomuna(entry,t.slice[1]))
    asc.append('INICIAPILA - PILAPOS IGUAL ARRAY PARIZQ PARDER PTCOMA')

def p_asigna_arreglo(t):
    'ASIGNAARREGLO : TEMPORAL ACCESO IGUAL expresion PTCOMA'  
    l =list(reversed(t[2]))
    t[0] = Asigna_arreglo(t[1],l,t[4],t.lineno(1),get_clomuna(entry,t.slice[1]))
    asc.append('ASIGNAARREGLO - TEMPORAL ACCESO IGUAL expresion PTCOMA')

#Recibe: destruccion de variable unset($t1);
def p_UNSETF(t):
    'UNSETF : UNSET PARIZQ expresion PARDER PTCOMA'
    t[0] = Unset(t[3],t.lineno(1),get_clomuna(entry,t.slice[1]))
    asc.append('UNSETF - UNSET PARIZQ expresion PARDER PTCOMA')

#Recibe if ($t1) goto label;
def p_if_instr(t) :
    'if_instr           : IF expresion DEFINEGOTO'
    t[0] =If(t[2], t[3],t.lineno(1),get_clomuna(entry,t.slice[1]))
    asc.append('if_instr  - IF expresion DEFINEGOTO')

def p_asignacion_instr(t) :
    'asignacion_instr   : TEMPORAL IGUAL expresion PTCOMA'
    t[0] =Asignacion(t[1], t[3],t.lineno(1),get_clomuna(entry,t.slice[1]))
    asc.append('asignacion_instr   - TEMPORAL IGUAL expresion PTCOMA')

#Recibe expresiones logicas y relacionales
def p_expresion_log_relacional(t) :
    '''expresion :            expresion_numerica MAYQUE expresion_numerica
                            | expresion_numerica MENQUE expresion_numerica
                            | expresion_numerica IGUALQUE expresion_numerica
                            | expresion_numerica NIGUALQUE expresion_numerica
                            | expresion_numerica MAYORIG expresion_numerica
                            | expresion_numerica MENORIG expresion_numerica
                            | expresion_numerica ANDLOG expresion_numerica
                            | expresion_numerica ORLOG expresion_numerica
                            | expresion_numerica XORLOG expresion_numerica
            '''
    if t[2] == '>'    : 
        t[0] = ExpresionLogica(t[1], t[3], OPERACION_LOGICA.MAYOR_QUE,t.lineno(1),get_clomuna(entry,t.slice[2]))
        asc.append('expresion -  expresion_numerica MAYQUE expresion_numerica')
    elif t[2] == '<'  : 
        t[0] = ExpresionLogica(t[1], t[3], OPERACION_LOGICA.MENOR_QUE,t.lineno(1),get_clomuna(entry,t.slice[2]))
        asc.append('expresion -  expresion_numerica MENQUE expresion_numerica')
    elif t[2] == '==' : 
        t[0] = ExpresionLogica(t[1], t[3], OPERACION_LOGICA.IGUAL,t.lineno(1),get_clomuna(entry,t.slice[2]))
        asc.append('expresion -  expresion_numerica IGUALQUE expresion_numerica')
    elif t[2] == '!=' : 
        t[0] = ExpresionLogica(t[1], t[3], OPERACION_LOGICA.DIFERENTE,t.lineno(1),get_clomuna(entry,t.slice[2]))
        asc.append('expresion -  expresion_numerica NIGUALQUE expresion_numerica')
    elif t[2] == '>=' : 
        t[0] = ExpresionLogica(t[1], t[3], OPERACION_LOGICA.MAYORQUE,t.lineno(1),get_clomuna(entry,t.slice[2]))
        asc.append('expresion -  expresion_numerica MAYORIG expresion_numerica')
    elif t[2] == '<=' : 
        t[0] = ExpresionLogica(t[1], t[3], OPERACION_LOGICA.MENORQUE,t.lineno(1),get_clomuna(entry,t.slice[2]))
        asc.append('expresion -  expresion_numerica MENORIG expresion_numerica')
    elif t[2] == 'xor' : 
        t[0] = ExpresionLogicaXOR(t[1], t[3],t.lineno(1),get_clomuna(entry,t.slice[2]))
        asc.append('expresion -  expresion_numerica XORLOG expresion_numerica')
    elif t[2] == '&&' : 
        t[0] = ExpresionLogicaAND(t[1], t[3],t.lineno(1),get_clomuna(entry,t.slice[2]))
        asc.append('expresion -  expresion_numerica ANDLOG expresion_numerica')
    elif t[2] == '||' : 
        t[0] = ExpresionLogicaOR(t[1], t[3],t.lineno(1),get_clomuna(entry,t.slice[2]))
        asc.append('expresion -  expresion_numerica ORLOG expresion_numerica')

def p_expresion_bit_not(t):
    'expresion_numerica : NOTBIT expresion'
    t[0] = ExpresionBitNot(t[2],t.lineno(1),get_clomuna(entry,t.slice[1]))
    asc.append('expresion_numerica - NOTBIT expresion')

#RECIBE !$t3
def p_expresion_logica_not(t):
    'expresion_numerica : NOTLOG expresion'
    t[0] = ExpresionLogicaNot(t[2],t.lineno(1),get_clomuna(entry,t.slice[1]))
    asc.append('expresion_numerica - NOTLOG expresion') 

def p_error(t):
     # Read ahead looking for a terminating ";"
    while True:
        tok = parser.token()             # Get the next token
        if not tok or tok.type == 'PTCOMA': break
    parser.errok()
    err = "Error en el token \'" + str(t.value) +"\' en la linea: "+ str(t.lineno) + ' de tipo: SINTACTICO'
    lista_errores.append(err)
     # Return SEMI to the parser as the next lookahead token
    return tok 
    #print(t)
    #print("Error sintáctico en '%s'" % t.value,'> ',str(t.lineno))
  

   

import ts as TS
import ply.yacc as yacc
parser = yacc.yacc()

lista_errores = []
entry= ''
def parse(input) :
    lexer = lex.lex()
    parser = yacc.yacc()
    global entry
    entry = input
    return parser.parse(input)

def retornalista():
    return lista_errores

def verGramatica():
    return asc