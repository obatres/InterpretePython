t={}
l=[4,5,'nombre','orlando']
exp =5
exp2=6
cont = 0

def llenar(dicc,cont,exp):
    if cont>=(len(l)-1):
        ind = l[cont]
        if dicc.get(ind):
            print('existe ultimo')
            u={ind:exp}
            dicc.update(u)
            cont=0
        else:
            dicc[ind]=exp
            print('no existe el ultimo')
            cont =0
        print(ind,dicc)
        return dicc   
    else:
        ind = l[cont]
        cont = cont +1
        if not dicc.get(ind):
            print(ind,dicc)
            dicc.setdefault(ind,llenar({},cont,exp))

 


r= llenar(t,cont,exp)
#r=llenar(r,cont,exp2)
print('Este es r',r)
