from socket import *

meuHost = '127.0.0.1'
minhaPorta = 5001

sockobj = socket(AF_INET, SOCK_STREAM)
dest = (meuHost, minhaPorta)
sockobj.connect(dest)

print('Para sair use CTRL+X\n')
msg = ''
while msg != '\x18':
    msg = input()
    sockobj.send(msg.encode())
    
    recvMsg = sockobj.recv(1024)
    print('Resposta: ', recvMsg.decode())

sockobj.close()
