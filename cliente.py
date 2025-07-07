import socket
import threading

HOST = 'localhost'
PORT = 5000

def receber_mensagens(sock):
    while True:
        try:
            mensagem = sock.recv(1024).decode()
            if mensagem:
                print(f'\n📦 {mensagem}')
            else:
                break
        except:
            print('\n[Erro] Conexão encerrada.')
            break

def iniciar_cliente():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        cliente.connect((HOST, PORT))
        print(f'[Conectado] ao servidor {HOST}:{PORT}')
    except ConnectionRefusedError:
        print('[Erro] Não foi possível conectar ao servidor.')
        return

    thread = threading.Thread(target=receber_mensagens, args=(cliente,))
    thread.daemon = True
    thread.start()

    try:
        while True:
            msg = input()
            if msg.lower() in ('sair', 'exit'):
                break
            cliente.sendall(msg.encode())
    except KeyboardInterrupt:
        print('\n[Encerrando conexão]')
    finally:
        cliente.close()

if __name__ == '__main__':
    iniciar_cliente()
