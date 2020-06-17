from enum import Enum

class TIPO_DATO(Enum) :
    INT     = 1
    FLOAT   = 2
    CADENA  = 3
    ARRAY   = 4
    PILA    = 5


class Simbolo() :
    'Esta clase representa un simbolo dentro de nuestra tabla de simbolos'

    def __init__(self, id, tipo, valor, amb) :
        self.id = id
        self.tipo = tipo
        self.valor = valor
        self.amb =  amb


class TablaDeSimbolos() :
    'Esta clase representa la tabla de simbolos'

    def __init__(self, simbolos = {}) :
        self.simbolos = simbolos

    def agregar(self, simbolo) :
        self.simbolos[simbolo.id] = simbolo
    
    def obtener(self, id) :
        if not id in self.simbolos :
            print('Error: variable ', id, ' no definida.')

        return self.simbolos[id]


    def obtenerPuntero(self,id):
        cont =0
        if not id in self.simbolos :
            print('Error: variable ', id, ' no definida. Puntero no accesible')
        else:
            for i in self.simbolos:
                if(str(i)==id):
                    return cont
                else:
                    cont = cont +1

    def actualizar(self, simbolo) :
        if not simbolo.id in self.simbolos :
            print('Error: variable ', simbolo.id, ' no definida.')
        else :
            self.simbolos[simbolo.id] = simbolo

    def existeSimbolo(self,simbolo):

        if not simbolo.id in self.simbolos:
            return False
        else:
            return True

    def eliminar(self,id):

        if not id in self.simbolos :
            print('Error: variable ', id, ' no definida.')
        else:
            del self.simbolos[id]

