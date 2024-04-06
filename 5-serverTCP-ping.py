from socket import *

meuHost = ''
minhaPorta = 5001

# Cria um objeto socket
# AF_INET == protocolo de endereco IP
# SOCK_STREAM == protocolo de transferência TCP
sockobj = socket(AF_INET, SOCK_STREAM)
orig = (meuHost, minhaPorta)
sockobj.bind(orig)
sockobj.listen(1)

while True:
    conn, cliente = sockobj.accept()
    print('Conectado por:', cliente)

    while True:
        recvMsg = conn.recv(1024)
        if recvMsg == b'\x18' or not recvMsg:   # interrompe quando receber ctrl-X (em bytes)
            break
        print(cliente, recvMsg.decode())
        conn.send(recvMsg)
    break

print('Finalizando conexão do cliente', cliente)
conn.close()
