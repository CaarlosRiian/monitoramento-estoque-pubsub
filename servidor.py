import socket
import threading

HOST = 'localhost'
PORT = 5000

assinantes_por_item = {}

inscricoes_por_conexao = {}

def lidar_com_clientes(conn, addr):
    print(f'[Novo Cliente] conectado por {addr}')
    inscricoes_por_conexao[conn] = set()

    try:
        while True:
            mensagem = conn.recv(1024).decode().strip()
            if not mensagem:
                break

            print(f'[Recebido de {addr}] - {mensagem}')

            if mensagem.startswith("SUBSCRIBE:"):
                item = mensagem.split(":", 1)[1].strip()
                if item not in assinantes_por_item:
                    assinantes_por_item[item] = []
                if conn not in assinantes_por_item[item]:
                    assinantes_por_item[item].append(conn)
                    inscricoes_por_conexao[conn].add(item)
                print(f'[{addr}] se inscreveu no item "{item}"')
                conn.sendall(f'[Servidor] Inscrito no item "{item}"'.encode())

            elif mensagem.startswith("UNSUBSCRIBE:"):
                item = mensagem.split(":", 1)[1].strip()
                if item in assinantes_por_item and conn in assinantes_por_item[item]:
                    assinantes_por_item[item].remove(conn)
                    inscricoes_por_conexao[conn].discard(item)
                    print(f'[{addr}] cancelou inscrição no item "{item}"')
                    conn.sendall(f'[Servidor] Desinscrito do item "{item}"'.encode())
                else:
                    conn.sendall(f'[Servidor] Você não está inscrito no item "{item}"'.encode())

            elif mensagem == "LIST":
                itens = inscricoes_por_conexao.get(conn, set())
                lista_itens = ", ".join(itens) if itens else "Nenhum"
                conn.sendall(f'[Servidor] Você está inscrito em: {lista_itens}'.encode())

            elif mensagem.startswith("UPDATE:"):
                partes = mensagem.split(":", 2)
                if len(partes) == 3:
                    _, item, conteudo = partes
                    item = item.strip()
                    conteudo = conteudo.strip()
                    if item in assinantes_por_item:
                        for cliente in assinantes_por_item[item]:
                            if cliente != conn:  
                                try:
                                    cliente.sendall(f"[{item}] {conteudo}".encode())
                                except:
                                    print(f"[Erro] Falha ao enviar para {cliente}")
                        print(f'[UPDATE] Enviado para assinantes de "{item}": {conteudo}')
                    else:
                        print(f'[UPDATE] Ninguém inscrito no item "{item}"')
                else:
                    print(f'[Formato Inválido] Esperado: UPDATE:<item>:<mensagem>')

            else:
                conn.sendall(f'[Servidor] Comando desconhecido.'.encode())

    except:
        print(f'[Desconectado] {addr}')
    finally:
        for item in inscricoes_por_conexao.get(conn, []):
            if conn in assinantes_por_item.get(item, []):
                assinantes_por_item[item].remove(conn)
        inscricoes_por_conexao.pop(conn, None)
        conn.close()

def iniciar_server():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, PORT))
    servidor.listen()
    print(f'[Servidor Iniciado] Aguardando conexão em {HOST}:{PORT}...')

    try:
        while True:
            conn, addr = servidor.accept()
            thread = threading.Thread(target=lidar_com_clientes, args=(conn, addr))
            thread.start()
    except KeyboardInterrupt:
        print('\n[Servidor Encerrado] Encerrando conexões...')
        servidor.close()

if __name__ == "__main__":
    iniciar_server()
