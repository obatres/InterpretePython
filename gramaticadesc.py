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
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

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


def p_init(t) :
    'init            : instrucciones'
    
    l = list(reversed(t[1]))
    t[0] = l
    print(t[0])

def p_instrucciones_lista(t) :
    'instrucciones    :  instruccion instruccionesP'
    t[0]=t[2]
    t[0].append(t[1])

def p_instrucciones_instruccion(t) :
    'instruccionesP    : instruccion instruccionesP'
    t[0]=t[2]
    t[0].append(t[1])

def p_instrucciones_empty(t):
    'instruccionesP : VACIO'
    t[0]=[]

def p_vacio(t):
    'VACIO : '
    pass

def p_instruccion(t) :
    '''instruccion      : imprimir_instr
                        | EXITF
                        | INICIO'''
    t[0] = t[1]

#RECIBE main:
def p_INICIO(t):
    'INICIO : MAIN DOSP'
    t[0] = Main()

#Recibe: exit;
def p_EXITF(t):
    'EXITF : EXIT PTCOMA'
    t[0]= Exit()

#Recibe: print($t1);
def p_instruccion_imprimir(t) :
    'imprimir_instr     : PRINT PARIZQ expresion PARDER PTCOMA'
    t[0] =Imprimir(t[3])


#RECIBE: expresiones aritmeticas y bit a bit
def p_expresion_binaria(t):
    '''expresion : expresion_numerica MAS expresion_numerica'''
    if t[2] == '+'  : t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.MAS)

def p_expresion_unaria(t):
    'expresion_numerica : MENOS expresion %prec UMENOS'
    t[0] = ExpresionNegativo(t[2])

def p_simp(t):
    'expresion : expresion_numerica'
    t[0]=t[1]

#Recibe (Expresion)
def p_expresion_agrupacion(t):
    'expresion_numerica : PARIZQ expresion PARDER'
    t[0] = t[2]

def p_expresion_number(t):
    '''expresion_numerica : ENTERO  '''
    t[0] = ExpresionNumero(t[1],TS.TIPO_DATO.INT)

def p_expresion_decimal(t):
    'expresion_numerica : DECIMAL'
    t[0] = ExpresionNumero(t[1],TS.TIPO_DATO.FLOAT)

def p_expresion_id(t):
    'expresion_numerica   : ID'
    t[0] = ExpresionNumero(t[1])

def p_expresion_pila(t):
    'expresion_numerica   : PILAPOS'
    t[0] = ExpresionPila(t[1])

def p_puntero_pila(t):
    'expresion_numerica : PILAPUNTERO'
    t[0] = ExpresionPunteroPila(t[1])

def p_pop_pila(t):
    'expresion_numerica : PILAPOS CORIZQ PILAPUNTERO CORDER'
    t[0] = Expresion_Pop_pila(t[1],t[3])

def p_expresion_parametro(t):
    '''expresion_numerica :    PARAMETRO
                            | VALORDEVUELTO
                            | DIRRETORNO'''
    t[0] = Expresion_param(t[1])

# Recibe temporales $t2
def p_expresion_tempo(t):
    'expresion_numerica : TEMPORAL'
    t[0] = ExpresionTemporal(t[1])                   
    
# recibe: punteros  &$t1  
def p_expresion_puntero(t):
    'expresion_numerica : PTEMPORAL'
    t[0] = ExpresionPunteroTemp(t[1])

#recibe: cadena 'hola'
def p_expresion_cadena(t) :
    'expresion_numerica     : CADENA'
    t[0] = ExpresionNumero(t[1], TS.TIPO_DATO.CADENA)

#recibe: cadena "hola"
def p_expresion_cade(t) :
    'expresion_numerica     : CADE'
    t[0] = ExpresionNumero(t[1], TS.TIPO_DATO.CADENA)

#recibe: read()
def p_expresion_read(t):
    'expresion_numerica : READ PARIZQ PARDER'
    print(t[1]) 

def p_inicializacion_array(t):
    'expresion_numerica : ARRAY PARIZQ PARDER'
    t[0]= InicioArray()

#Recibe expresiones logicas y relacionales
def p_expresion_log_relacional(t) :
    '''expresion : expresion_numerica MAYQUE expresion_numerica'''
    if t[2] == '>'    : t[0] = ExpresionLogica(t[1], t[3], OPERACION_LOGICA.MAYOR_QUE)

def p_expresion_bit_not(t):
    'expresion_numerica : NOTBIT expresion'
    t[0] = ExpresionBitNot(t[2])

def p_error(t):
     # Read ahead looking for a terminating ";"
     while True:
         tok = parser.token()             # Get the next token
         if not tok or tok.type == 'PTCOMA': break
     parser.errok()
 
     # Return SEMI to the parser as the next lookahead token
     return tok 
    #print(t)
    #print("Error sintáctico en '%s'" % t.value,'> ',str(t.lineno))
  

   

import ts as TS
import ply.yacc as yacc
parser = yacc.yacc()


def parse(input) :
    return parser.parse(input)