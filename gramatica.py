#-------------------------------------------------ANALIZADOR LEXICO
reservadas = {
    'numero' : 'NUMERO',
    'imprimir' : 'IMPRIMIR',
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
    'while':'WHILE',
    'end':'END',
    'abs':'ABS'
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
    'CONCAT',
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
    'TEMPORAL'
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
t_CONCAT    = r'&'
t_MENQUE    = r'<'
t_MAYQUE    = r'>'
t_IGUALQUE  = r'=='
t_NIGUALQUE = r'!='
t_DOSP      = r':'

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
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Construyendo el analizador léxico
import ply.lex as lex
lexer = lex.lex()


# Asociación de operadores y precedencia
precedence = (
    ('left','CONCAT'),
    ('left','MAS','MENOS'),
    ('left','POR','DIVIDIDO'),
    ('left','RES','ABS'),
    ('right','UMENOS'),
    )

# Definición de la gramática

from expresiones import *
from instrucciones import *


def p_init(t) :
    'init            : instrucciones'
    t[0] = t[1]

def p_instrucciones_lista(t) :
    'instrucciones    : instrucciones instruccion'
    t[1].append(t[2])
    t[0] = t[1]

def p_instrucciones_instruccion(t) :
    'instrucciones    : instruccion '
    t[0] = [t[1]]

def p_instruccion(t) :
    '''instruccion      : imprimir_instr
                        | definicion_instr
                        | asignacion_instr
                        | mientras_instr
                        | if_instr
                        | if_else_instr
                        | INICIO
                        | UNSETF
                        | EXITF'''
    t[0] = t[1]

#Recibe: destruccion de variable unset($t1);
def p_UNSETF(t):
    'UNSETF : UNSET PARIZQ expresion_numerica PARDER PTCOMA'
    print(t[3])

#RECIBE main:
def p_INICIO(t):
    'INICIO : MAIN DOSP'
    print(t[1])

#Recibe: exit;
def p_EXITF(t):
    'EXITF : EXIT PTCOMA'
    print(t[1])

def p_instruccion_imprimir(t) :
    'imprimir_instr     : PRINT PARIZQ expresion_numerica PARDER PTCOMA'
    #t[0] =Imprimir(t[3])
    print(t[3])

def p_instruccion_definicion(t) :
    'definicion_instr   : NUMERO TEMPORAL PTCOMA'
    #t[0] =Definicion(t[2])

def p_asignacion_instr(t) :
    'asignacion_instr   : TEMPORAL IGUAL expresion_numerica PTCOMA'
    #t[0] =Asignacion(t[1], t[3])

def p_mientras_instr(t) :
    'mientras_instr     : MIENTRAS PARIZQ expresion_logica PARDER LLAVIZQ instrucciones LLAVDER'
    t[0] =Mientras(t[3], t[6])

def p_if_instr(t) :
    'if_instr           : IF PARIZQ expresion_logica PARDER LLAVIZQ instrucciones LLAVDER'
    t[0] =If(t[3], t[6])

def p_if_else_instr(t) :
    'if_else_instr      : IF PARIZQ expresion_logica PARDER LLAVIZQ instrucciones LLAVDER ELSE LLAVIZQ instrucciones LLAVDER'
    t[0] =IfElse(t[3], t[6], t[10])

def p_expresion_binaria(t):
    '''expresion_numerica : expresion_numerica MAS expresion_numerica
                        | expresion_numerica MENOS expresion_numerica
                        | expresion_numerica POR expresion_numerica
                        | expresion_numerica DIVIDIDO expresion_numerica
                        | expresion_numerica RES expresion_numerica'''
    if t[2] == '+'  : t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.MAS)
    elif t[2] == '-': t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.MENOS)
    elif t[2] == '*': t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.POR)
    elif t[2] == '/': t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.DIVIDIDO)

def p_expresion_unaria(t):
    'expresion_numerica : MENOS expresion_numerica %prec UMENOS'
    t[0] = ExpresionNegativo(t[2])

def p_expresion_agrupacion(t):
    'expresion_numerica : PARIZQ expresion_numerica PARDER'
    t[0] = t[2]

def p_expresion_number(t):
    '''expresion_numerica : ENTERO
                        | DECIMAL'''
    #t[0] = ExpresionNumero(t[1])
    print(t[1])


def p_expresion_id(t):
    'expresion_numerica   : ID'
    #t[0] = ExpresionIdentificador(t[1])

# Recibe temporales $t2
def p_expresion_tempo(t):
    'expresion_numerica : TEMPORAL'
                       
    print(t[1])

# recibe: punteros  &$t1  
def p_expresion_puntero(t):
    'expresion_numerica : CONCAT expresion_numerica'
    print(t[2])

#recibe: cadena 'hola'
def p_expresion_cadena(t) :
    'expresion_numerica     : CADENA'
    #t[0] = ExpresionDobleComilla(t[1])
    print(t[1])

#recibe: read()
def p_expresion_read(t):
    'expresion_numerica : READ PARIZQ PARDER'
    print(t[1]) 


#recibe: conversiones TIPOCONVERSION $t1 
def p_expresion_conversion(t):
    'expresion_numerica : TIPOCONVERSION expresion_numerica'
    print("conversion: "+t[1])

#recibe: tipo de conversion (int) (float)
def p_expresion_tipoConversion(t):
    '''TIPOCONVERSION : PARIZQ INT PARDER
                    | PARIZQ FLOAT PARDER
                    | PARIZQ CHAR PARDER '''
    t[0]=t[2]

#Recibe: valor absoluto
def p_expresion_valorabs(t):
    'expresion_numerica : ABS PARIZQ expresion_numerica PARDER'
    print(t[3])

def p_expresion_logica(t) :
    '''expresion_logica : expresion_numerica MAYQUE expresion_numerica
                        | expresion_numerica MENQUE expresion_numerica
                        | expresion_numerica IGUALQUE expresion_numerica
                        | expresion_numerica NIGUALQUE expresion_numerica'''
    if t[2] == '>'    : t[0] = ExpresionLogica(t[1], t[3], OPERACION_LOGICA.MAYOR_QUE)
    elif t[2] == '<'  : t[0] = ExpresionLogica(t[1], t[3], OPERACION_LOGICA.MENOR_QUE)
    elif t[2] == '==' : t[0] = ExpresionLogica(t[1], t[3], OPERACION_LOGICA.IGUAL)
    elif t[2] == '!=' : t[0] = ExpresionLogica(t[1], t[3], OPERACION_LOGICA.DIFERENTE)

def p_error(t):
    print(t)
    print("Error sintáctico en '%s'" % t.value)

import ply.yacc as yacc
parser = yacc.yacc()


def parse(input) :
    return parser.parse(input)