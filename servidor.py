import socket
import threading

HOST = 'localhost'
PORT = 5000

clientes = []

def lidar_com_clientes(conn, addr):
    print(f'[Novo Cliente] conectado por {addr}')
    clientes.append(conn)

    try:
        while True:
            mensagem = conn.recv(1024).decode()
            if not mensagem:
                break
            print(f'[Recebido de {addr}] - {mensagem}')

            for cliente in clientes:
                if cliente != conn:
                    cliente.sendall(f'Atualização - {mensagem}'.encode())
    except:
        print(f'[Desconectado] {addr}')
    finally:
        clientes.remove(conn)
        conn.close()

def iniciar_server():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, PORT))
    servidor.listen()
    print(f'[Servidor Iniciado] Aguardando conexão em {HOST}:{PORT}...')

    while True:
        conn, addr = servidor.accept()
        thread = threading.Thread(target=lidar_com_clientes, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    iniciar_server()