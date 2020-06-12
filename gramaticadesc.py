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
                        | EXITF'''
    t[0] = t[1]

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
    print(t[1],t[3])

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
    #print(t[1])


#Recibe expresiones logicas y relacionales
def p_expresion_log_relacional(t) :
    '''expresion : expresion_numerica MAYQUE expresion_numerica'''
    print(t[1],t[3])


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