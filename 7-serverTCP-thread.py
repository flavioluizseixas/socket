from socket import *
from threading import Thread

meuHost = ''
minhaPorta = 8080


def tratar_cliente(conn, cliente):
    print('Conectado por:', cliente)

    try:
        requisicao = conn.recv(1024).decode('utf-8', errors='ignore')
        if not requisicao:
            return

        print('Requisicao recebida de', cliente)
        print(requisicao.splitlines()[0])

        corpo = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Servidor HTTP com Threads</title>
</head>
<body>
    <h1>Servidor HTTP com Threads</h1>
    <p>Conexao atendida com sucesso para o cliente {cliente[0]}:{cliente[1]}.</p>
    <p>Cada conexao e processada em uma thread separada.</p>
</body>
</html>
'''

        resposta = (
            'HTTP/1.1 200 OK\r\n'
            'Content-Type: text/html; charset=utf-8\r\n'
            f'Content-Length: {len(corpo.encode("utf-8"))}\r\n'
            'Connection: close\r\n'
            '\r\n'
            f'{corpo}'
        )

        conn.sendall(resposta.encode('utf-8'))
    finally:
        print('Finalizando conexão do cliente', cliente)
        conn.close()


# Cria um objeto socket
# AF_INET == protocolo de endereco IP
# SOCK_STREAM == protocolo de transferencia TCP
sockobj = socket(AF_INET, SOCK_STREAM)
sockobj.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

orig = (meuHost, minhaPorta)
sockobj.bind(orig)
sockobj.listen(5)

print(f'Servidor HTTP aguardando conexoes na porta {minhaPorta}...')

while True:
    conn, cliente = sockobj.accept()
    nova_thread = Thread(target=tratar_cliente, args=(conn, cliente))
    nova_thread.daemon = True
    nova_thread.start()
