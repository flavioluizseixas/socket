from socket import *

meuHost = ''
minhaPorta = 5000

# Cria um objeto socket
# AF_INET == protocolo de endereco IP
# SOCK_DGRAM == protocolo de transferência UDP
sockobj = socket(AF_INET, SOCK_DGRAM)
orig = (meuHost, minhaPorta)
sockobj.bind(orig)

while True:
    recvMsg, cliente = sockobj.recvfrom(1024)
    if recvMsg == b'\x18' or not recvMsg:   # interrompe quando receber ctrl-X (em bytes)
        break
    print(cliente, recvMsg.decode())

sockobj.close()
