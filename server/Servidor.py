import socket
import threading

# Configuração
IP_SERVIDOR = 'localhost'
PORTA_SERVIDOR = 42022
TAMANHO_BUFFER = 1024
MARCADOR_FIM_ARQUIVO = b'__FIM_DO_ARQUIVO__'


def lidar_com_cliente(socket_cliente):
  while True:
    # Exibe menu para o cliente
    socket_cliente.send(
        "Escolha uma opção:\n1. Enviar uma mensagem de chat\n2. Solicitar um arquivo\n3. Sair"
        .encode('utf-8'))
    escolha = socket_cliente.recv(TAMANHO_BUFFER).decode('utf-8')

    # Cliente escolhe enviar uma mensagem de chat
    if escolha == "1":
      mensagem = socket_cliente.recv(TAMANHO_BUFFER).decode('utf-8')
      print(f"Mensagem do cliente: {mensagem}")

    # Cliente escolhe solicitar um arquivo
    elif escolha == "2":
      nome_arquivo = socket_cliente.recv(TAMANHO_BUFFER).decode('utf-8')
      try:
        with open(nome_arquivo, 'rb') as arquivo:
          while True:
            dados = arquivo.read(TAMANHO_BUFFER)
            if not dados:
              break
            socket_cliente.send(dados)
        # Envia marcador para informar o cliente que a transferência do arquivo está completa
        socket_cliente.send(MARCADOR_FIM_ARQUIVO)
        print(f"Arquivo {nome_arquivo} enviado ao cliente.")
        # Aguarda confirmação do cliente após transferência do arquivo
        socket_cliente.recv(TAMANHO_BUFFER)
      except FileNotFoundError:
        print(f"Arquivo {nome_arquivo} não encontrado.")
        socket_cliente.send("Arquivo não encontrado.".encode('utf-8'))

    # Cliente escolhe sair
    elif escolha == "3":
      print(f"Cliente desconectou.")
      break

  socket_cliente.close()


# Cria o socket do servidor
socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_servidor.bind((IP_SERVIDOR, PORTA_SERVIDOR))
socket_servidor.listen(5)

print(
    f"Servidor iniciado na porta {PORTA_SERVIDOR}. Aguardando conexões de clientes..."
)

while True:
  socket_cliente, endereco = socket_servidor.accept()
  print(f"Conexão aceita de {endereco}.")
  # Inicia uma nova thread para lidar com a conexão do cliente
  tratador_cliente = threading.Thread(target=lidar_com_cliente,
                                      args=(socket_cliente, ))
  tratador_cliente.start()
