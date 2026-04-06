from socket import *

meuHost = '127.0.0.1'
minhaPorta = 5001

sockobj = socket(AF_INET, SOCK_STREAM)
dest = (meuHost, minhaPorta)
try:
    sockobj.connect(dest)
except ConnectionRefusedError:
    print("Erro: Não foi possível conectar ao servidor. Verifique se o servidor está rodando.")
    exit(1)

print('Para sair use CTRL+X\n')
msg = ''
while msg != '\x18':
    msg = input()
    sockobj.send(msg.encode())

sockobj.close()
