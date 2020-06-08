t={}
l1=[0]
t.setdefault(0,l1)
l2=[1]
t.setdefault(1,l2)
print(t.get(1))
l3 = 'carla'
t.setdefault('nombre',l3)

#$t1['nombre'][4]='o'

clave='nombre'
posicion=4

listatemp = t.get('nombre')

try:
    print(listatemp[4])
except :
    print(' no se puede acceder a la memoria')



print(listatemp)
'''p=['tercera posicion']
j=[p]
t.setdefault(2,j)'''

print(t)
#print(t.get(2)[0][0][0])