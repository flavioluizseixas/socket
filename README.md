# Socket

Material de apoio para o laboratório de implementação de sockets da disciplina `TCC00359 - Redes de Computadores`.

O objetivo deste repositório é mostrar, com exemplos pequenos e diretos, como criar aplicações cliente-servidor usando sockets em Python, inicialmente com `TCP` e depois com `UDP`.

## Arquivos do repositório

- `1-serverTCP.py`: servidor TCP básico.
- `2-clientTCP.py`: cliente TCP básico.
- `3-serverUDP.py`: servidor UDP básico.
- `4-clientUDP.py`: cliente UDP básico.
- `5-serverTCP-ping.py`: servidor TCP com comportamento de eco.
- `6-clientTCP-ping.py`: cliente TCP para o exemplo de eco.
- `7-serverTCP-thread.py`: servidor HTTP simples usando threads para atender múltiplas conexões.

## Pré-requisitos

- Python 3 instalado.
- Terminal para executar os programas.
- Noções básicas de IP, porta, processo e comunicação cliente-servidor.

## Como executar os exemplos TCP

Abra dois terminais no diretório do projeto.

No primeiro terminal, execute o servidor:

```bash
python3 1-serverTCP.py
```

No segundo terminal, execute o cliente:

```bash
python3 2-clientTCP.py
```

Depois disso:

1. Digite mensagens no cliente.
2. Observe as mensagens sendo recebidas no servidor.
3. Para encerrar a comunicação, digite `CTRL+X` no cliente.

## Visão geral do fluxo TCP

No modelo TCP, cliente e servidor não se comunicam "soltando pacotes" de forma independente, como no UDP. Antes da troca de dados, é necessário estabelecer uma conexão.

O fluxo básico é este:

1. O servidor cria um socket.
2. O servidor associa esse socket a um endereço IP e a uma porta.
3. O servidor entra em modo de escuta.
4. O cliente cria um socket.
5. O cliente tenta se conectar ao endereço e à porta do servidor.
6. O servidor aceita a conexão.
7. Cliente e servidor trocam bytes pela conexão estabelecida.
8. Um dos lados encerra a conexão.

Essa ordem explica por que, neste laboratório, o servidor deve ser executado antes do cliente: o cliente só consegue completar `connect()` se houver um processo servidor escutando na porta desejada.

## Passo a passo do `1-serverTCP.py`

Arquivo: [1-serverTCP.py](/Users/fseixas/Dev/socket/1-serverTCP.py)

### 1. Importação da biblioteca

```python
from socket import *
```

O programa importa os recursos da biblioteca `socket`, que fornece a API de comunicação de rede usada pelo sistema operacional.

### 2. Definição do host e da porta

```python
meuHost = ''
minhaPorta = 5001
```

- `meuHost = ''` indica que o servidor aceitará conexões em todas as interfaces de rede disponíveis na máquina.
- `minhaPorta = 5001` define a porta de transporte usada pelo processo servidor.

Em laboratório, usamos uma porta alta, acima de `1024`, para evitar restrições de permissão e conflito com serviços do sistema.

### 3. Criação do socket TCP

```python
sockobj = socket(AF_INET, SOCK_STREAM)
```

Aqui são feitas duas escolhas importantes:

- `AF_INET`: a aplicação usará endereçamento IPv4.
- `SOCK_STREAM`: a comunicação será orientada a conexão, isto é, via TCP.

Em outras palavras, esse socket representa um ponto final de comunicação TCP sobre IPv4.

### 4. Associação do socket ao endereço local

```python
orig = (meuHost, minhaPorta)
sockobj.bind(orig)
```

O método `bind()` registra no sistema operacional onde o servidor ficará disponível.

Sem esse passo, o servidor não "ocupa" a porta e não pode receber conexões destinadas a ela.

### 5. Colocando o servidor em escuta

```python
sockobj.listen(2)
```

O método `listen()` marca o socket como passivo, isto é, pronto para aceitar conexões de clientes.

O número `2` representa o tamanho da fila de conexões pendentes. Isso não significa "atender exatamente dois clientes", mas sim quantas conexões podem aguardar aceitação antes de o sistema começar a recusá-las.

### 6. Espera por uma conexão

```python
conn, cliente = sockobj.accept()
```

O `accept()` é bloqueante. Isso significa que o servidor fica parado nessa chamada até que algum cliente tente se conectar.

Quando a conexão acontece:

- `conn` recebe um novo socket, específico daquela conexão com o cliente.
- `cliente` recebe o endereço remoto do cliente, normalmente no formato `(ip, porta)`.

Esse ponto é importante conceitualmente:

- `sockobj` continua sendo o socket do servidor, usado para escutar.
- `conn` é o socket da sessão ativa com um cliente específico.

### 7. Recepção dos dados

```python
recvMsg = conn.recv(1024)
```

O método `recv(1024)` tenta ler até `1024` bytes da conexão TCP.

Como TCP é um protocolo orientado a fluxo de bytes, o programa recebe bytes, não "mensagens" rigidamente delimitadas. Em exemplos simples, tratamos cada leitura como se fosse uma mensagem, mas tecnicamente o TCP entrega um fluxo contínuo.

### 8. Condição de encerramento

```python
if recvMsg == b'\x18' or not recvMsg:
    break
```

Há dois casos de parada:

- `recvMsg == b'\x18'`: o cliente enviou o byte correspondente ao `CTRL+X`.
- `not recvMsg`: a conexão foi encerrada pelo outro lado e não há mais dados para ler.

O prefixo `b` indica que o valor é um objeto do tipo `bytes`.

### 9. Conversão de bytes para texto

```python
print(cliente, recvMsg.decode())
```

Como a rede transmite bytes, o programa precisa converter os dados recebidos para `string` antes de exibir no terminal. O método `decode()` faz essa conversão.

### 10. Encerramento da conexão

```python
conn.close()
```

Ao final, o socket da conexão é fechado. Isso libera recursos do sistema operacional e encerra corretamente a sessão TCP daquele cliente.

## Passo a passo do `2-clientTCP.py`

Arquivo: [2-clientTCP.py](/Users/fseixas/Dev/socket/2-clientTCP.py)

### 1. Definição do destino

```python
meuHost = '127.0.0.1'
minhaPorta = 5001
```

- `127.0.0.1` é o endereço de loopback, isto é, a própria máquina local.
- A porta `5001` deve ser a mesma configurada no servidor.

Se cliente e servidor estiverem em máquinas diferentes, o IP do servidor deve ser colocado aqui.

### 2. Criação do socket

```python
sockobj = socket(AF_INET, SOCK_STREAM)
```

O cliente também usa um socket IPv4 com TCP. A diferença é o papel desempenhado:

- o servidor escuta conexões;
- o cliente inicia a conexão.

### 3. Tentativa de conexão

```python
dest = (meuHost, minhaPorta)
sockobj.connect(dest)
```

O método `connect()` solicita ao sistema operacional a abertura de uma conexão TCP com o servidor.

Se o servidor não estiver em execução ou se a porta estiver incorreta, essa operação falha.

### 4. Tratamento de erro de conexão

```python
except ConnectionRefusedError:
    print("Erro: Não foi possível conectar ao servidor. Verifique se o servidor está rodando.")
    exit(1)
```

Esse tratamento melhora a experiência de uso do programa e torna explícita uma situação comum em laboratório: tentar executar o cliente antes do servidor.

### 5. Leitura da entrada do usuário

```python
msg = input()
```

O cliente lê uma linha digitada pelo usuário no terminal.

### 6. Conversão da mensagem para bytes e envio

```python
sockobj.send(msg.encode())
```

O método `encode()` converte a `string` digitada em bytes. Em seguida, `send()` transmite esses bytes ao servidor pela conexão TCP.

### 7. Repetição até o comando de saída

```python
while msg != '\x18':
```

O cliente permanece lendo e enviando mensagens até que o usuário informe `CTRL+X`, utilizado neste exemplo como marcador de encerramento.

### 8. Fechamento do socket

```python
sockobj.close()
```

Esse fechamento encerra a conexão do lado cliente e libera os recursos associados ao socket.

## Relação entre os dois programas

Os dois códigos foram escritos para trabalhar em conjunto:

- o servidor fica bloqueado em `accept()` aguardando um cliente;
- o cliente executa `connect()` para iniciar a sessão;
- depois da conexão estabelecida, o cliente envia dados com `send()`;
- o servidor recebe os dados com `recv()`;
- quando o encerramento ocorre, a conexão é fechada.

Esse par de programas representa o padrão mais básico de aplicação de rede orientada a conexão.

## Pontos técnicos importantes para discutir em aula

- TCP é orientado a conexão, enquanto UDP é não orientado a conexão.
- TCP oferece confiabilidade, ordenação e controle de fluxo.
- As aplicações lidam com bytes; texto precisa de `encode()` e `decode()`.
- `accept()` cria um novo socket por conexão.
- O servidor e o cliente precisam concordar sobre IP, porta e protocolo.
- Uma porta identifica o serviço dentro do host; o IP identifica a máquina na rede.
- `recv(1024)` não garante receber "uma mensagem completa"; ele lê até aquele limite de bytes disponíveis.

## Sugestões de experimentos em sala

1. Execute o cliente antes do servidor e observe o erro gerado. Explique tecnicamente por que ele acontece.
2. Altere a porta no cliente ou no servidor e verifique o que muda no comportamento.
3. Modifique o cliente para enviar várias mensagens curtas em sequência e observe a recepção no servidor.
4. Troque `127.0.0.1` pelo IP da máquina em rede local e teste a comunicação entre dois computadores.
5. Adicione logs com horário para visualizar melhor o ciclo de vida da conexão.

## Atividades

1. Diferente do UDP, no TCP é necessário executar primeiro o servidor e depois o cliente. Explique isso com base nas chamadas `bind()`, `listen()`, `accept()` e `connect()`.
2. Melhore o programa do servidor TCP para aceitar múltiplas conexões. Uma abordagem possível é criar uma thread para cada cliente aceito. Mostre e explique a implementação.
3. Implemente um serviço de eco sobre TCP. Adapte os códigos do servidor e do cliente para que toda mensagem enviada pelo cliente seja devolvida pelo servidor. Mostre a implementação e explique o fluxo dos dados.
4. Implemente um servidor Web simples. Adapte o servidor TCP para responder a uma requisição HTTP com um conteúdo HTML mínimo. Explique a estrutura da resposta HTTP enviada.
5. Compare os exemplos TCP e UDP do repositório. Discuta diferenças de uso, confiabilidade, overhead e cenários de aplicação.

## Próximos passos

Depois de compreender os arquivos `1-serverTCP.py` e `2-clientTCP.py`, o caminho natural é avançar para:

- `5-serverTCP-ping.py` e `6-clientTCP-ping.py`, para entender o serviço de eco.
- `7-serverTCP-thread.py`, para observar atendimento concorrente com threads.
- `3-serverUDP.py` e `4-clientUDP.py`, para comparar com o modelo sem conexão do UDP.
