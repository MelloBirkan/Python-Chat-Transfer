import socket
import os

# Configuração
IP_SERVIDOR = 'localhost'
PORTA_SERVIDOR = 42022
TAMANHO_BUFFER = 1024
MARCADOR_FIM_ARQUIVO = b'__FIM_DO_ARQUIVO__'

# Conecta-se ao servidor
socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_cliente.connect((IP_SERVIDOR, PORTA_SERVIDOR))

while True:
  # Exibe o menu
  menu = socket_cliente.recv(TAMANHO_BUFFER).decode('utf-8')
  print(menu)
  escolha = input("Digite sua escolha: ")
  socket_cliente.send(escolha.encode('utf-8'))

  # Cliente escolhe enviar uma mensagem de chat
  if escolha == "1":
    mensagem = input("Digite sua mensagem: ")
    socket_cliente.send(mensagem.encode('utf-8'))

  # Cliente escolhe solicitar um arquivo
  elif escolha == "2":
    nome_arquivo = input(
        "Digite o nome do arquivo que você deseja solicitar: ")
    socket_cliente.send(nome_arquivo.encode('utf-8'))
    # Recebe e salva o arquivo
    with open(os.path.join("received", nome_arquivo), 'wb') as arquivo:
      while True:
        dados = socket_cliente.recv(TAMANHO_BUFFER)
        if MARCADOR_FIM_ARQUIVO in dados:
          arquivo.write(dados[:-len(MARCADOR_FIM_ARQUIVO)])
          break
        arquivo.write(dados)
    print(f"Arquivo {nome_arquivo} recebido e salvo na pasta 'received'.")
    # Envia confirmação para o servidor
    socket_cliente.send("Arquivo recebido.".encode('utf-8'))

  # Cliente escolhe sair
  elif escolha == "3":
    print("Saindo. Obrigado!")
    break

socket_cliente.close()
