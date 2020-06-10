t={}
l=[4,5,'nombre','orlando']
exp =5
exp2=6
cont = 0
can_accesos = len(l)
temp1= t
for i in range(len(l)):
    indice = l[i]
    if i == can_accesos-1:
        #Es el ultimo
        temp1[indice]=exp
    else:
        temp = temp1.get(indice)
        if temp == None:
            temp1[indice]={}
            temp1=temp1.get(indice)
        else:
            temp1=temp1.get(indice)
print('asignacion:',t)


for j in range(len(l)):
    indice = l[j]
    if i == can_accesos-1:
        #Es el ultimo
        temp1 = temp1.get(indice)


print('recuperacion',t)