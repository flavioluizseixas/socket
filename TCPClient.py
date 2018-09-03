import socket
serverName = 'localhost'
serverPort = 12000
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
sentence = input('Entre com uma sequencia de caracteres em minúsculo:')
clientSocket.send(sentence.encode())
modifiedSentence = clientSocket.recv(1024)
print('Recebido do servidor:', modifiedSentence)
clientSocket.close()
