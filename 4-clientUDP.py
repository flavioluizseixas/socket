from socket import *

meuHost = '127.0.0.1'
minhaPorta = 5000

sockobj = socket(AF_INET, SOCK_DGRAM)
dest = (meuHost, minhaPorta)

print('Para sair use CTRL+X\n')
msg = ''
while msg != '\x18':
    msg = input()
    sockobj.sendto(msg.encode(), dest)

sockobj.close()