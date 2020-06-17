import re
t = 'asdasd654'
patronFloat = re.compile('([0-9]+(\.)[0-9]+){1}')
patronNum = re.compile('[0-9]+')
if patronFloat.match(t):
    print('float')
elif patronNum.match(t):
    print('entero')
else:
    print('cadena')
    
