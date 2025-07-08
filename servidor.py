import socket
import threading

HOST = 'localhost'
PORT = 5000

estoque = {}  # Exemplo: {'arroz': {'quantidade': 10, 'preco': 5.0}}
assinantes_por_item = {}
inscricoes_por_conexao = {}
admin_conn = None  # Conexão do administrador

def lidar_com_clientes(conn, addr):
    global admin_conn

    print(f'[Novo Cliente] Conectado por {addr}')
    inscricoes_por_conexao[conn] = set()

    if admin_conn is None:
        admin_conn = conn
        conn.sendall("[ADMIN] Você é o administrador do sistema.".encode())
        print(f'[INFO] Cliente {addr} designado como ADMIN')

    try:
        while True:
            mensagem = conn.recv(1024).decode().strip()
            if not mensagem:
                break

            print(f'[Recebido de {addr}] - {mensagem}')

            if mensagem.startswith("SUBSCRIBE:"):
                item = mensagem.split(":", 1)[1].strip()
                assinantes_por_item.setdefault(item, []).append(conn)
                inscricoes_por_conexao[conn].add(item)
                conn.sendall(f"[Servidor] Inscrito no item '{item}'".encode())

            elif mensagem.startswith("UNSUBSCRIBE:"):
                item = mensagem.split(":", 1)[1].strip()
                assinantes_por_item.get(item, []).remove(conn)
                inscricoes_por_conexao[conn].discard(item)
                conn.sendall(f"[Servidor] Cancelada inscrição em '{item}'".encode())

            elif mensagem == "LIST":
                itens = inscricoes_por_conexao.get(conn, set())
                lista = ", ".join(itens) if itens else "Nenhum"
                conn.sendall(f"[Servidor] Você está inscrito em: {lista}".encode())

            elif mensagem.startswith("UPDATE:"):
                partes = mensagem.split(":", 2)
                if len(partes) == 3:
                    _, item, conteudo = partes
                    for cliente in assinantes_por_item.get(item.strip(), []):
                        if cliente != conn:
                            cliente.sendall(f"[{item.strip()}] {conteudo.strip()}".encode())

            elif mensagem == "LIST_STOCK":
                if estoque:
                    lista = "\n".join(
                        [f"📦 {k}: {v['quantidade']} unidades - R$ {v['preco']:.2f}" for k, v in estoque.items()]
                    )
                    conn.sendall(f"[Estoque Atual]\n{lista}".encode())
                else:
                    conn.sendall("[Estoque] Nenhum item no estoque.".encode())

            # 🔐 ADMIN COMMANDS
            elif conn == admin_conn:
                if mensagem.startswith("ADD:"):
                    nome, qtd, preco = mensagem.split(":")[1:]
                    nome = nome.strip()
                    estoque[nome] = {
                        "quantidade": int(qtd),
                        "preco": float(preco)
                    }
                    print(f"[ESTOQUE] Adicionado: {nome}")
                    conn.sendall(f"[Admin] Item '{nome}' adicionado ao estoque.".encode())

                elif mensagem.startswith("REMOVE:"):
                    nome = mensagem.split(":", 1)[1].strip()
                    if nome in estoque:
                        del estoque[nome]
                        conn.sendall(f"[Admin] Item '{nome}' removido.".encode())
                    else:
                        conn.sendall(f"[Admin] Item '{nome}' não encontrado.".encode())

                elif mensagem.startswith("UPDATE_QTY:"):
                    nome, qtd = mensagem.split(":")[1:]
                    if nome.strip() in estoque:
                        estoque[nome.strip()]["quantidade"] = int(qtd)
                        for sub in assinantes_por_item.get(nome.strip(), []):
                            sub.sendall(f"[{nome}] Quantidade atualizada: {qtd}".encode())
                        conn.sendall(f"[Admin] Quantidade de '{nome}' atualizada.".encode())
                    else:
                        conn.sendall(f"[Admin] Item '{nome}' não encontrado.".encode())

                elif mensagem.startswith("UPDATE_PRICE:"):
                    partes = mensagem.split(":")
                    if len(partes) == 3:
                        nome, preco = partes[1].strip(), float(partes[2].strip())
                        if nome in estoque:
                            preco_antigo = estoque[nome]["preco"]
                            estoque[nome]["preco"] = preco

                            direcao = "reduzido" if preco < preco_antigo else "aumentado" if preco > preco_antigo else "mantido"
                            mensagem_assinantes = (
                                f"[{nome}] Preço {direcao.upper()}! Era R$ {preco_antigo:.2f}, agora R$ {preco:.2f}"
                            )

                            for sub in assinantes_por_item.get(nome, []):
                                try:
                                    sub.sendall(mensagem_assinantes.encode())
                                except:
                                    print(f"[Erro] Não foi possível enviar atualização para {sub}")

                            conn.sendall(f"[Admin] Preço de '{nome}' atualizado de R$ {preco_antigo:.2f} para R$ {preco:.2f}".encode())
                        else:
                            conn.sendall(f"[Admin] Item '{nome}' não encontrado.".encode())
                    else:
                        conn.sendall("[Admin] Formato inválido. Use: UPDATE_PRICE:<item>:<novo_preco>".encode())

            else:
                conn.sendall("[Servidor] Comando inválido ou sem permissão.".encode())

    except Exception as e:
        print(f"[Erro] {addr}: {e}")
    finally:
        print(f'[Desconectado] {addr}')
        for item in inscricoes_por_conexao.get(conn, set()):
            if conn in assinantes_por_item.get(item, []):
                assinantes_por_item[item].remove(conn)
        inscricoes_por_conexao.pop(conn, None)
        if conn == admin_conn:
            print("[Admin] saiu. O próximo cliente será o novo admin.")
            admin_conn = None
        conn.close()

def iniciar_server():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, PORT))
    servidor.listen()
    print(f"[Servidor Iniciado] Aguardando conexões em {HOST}:{PORT}...")

    try:
        while True:
            conn, addr = servidor.accept()
            thread = threading.Thread(target=lidar_com_clientes, args=(conn, addr))
            thread.start()
    except KeyboardInterrupt:
        print("\n[Servidor Encerrado]")
        servidor.close()

if __name__ == "__main__":
    iniciar_server()
