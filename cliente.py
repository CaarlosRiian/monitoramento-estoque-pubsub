import socket
import threading
import time

HOST = 'localhost'
PORT = 5000

is_admin = False
admin_event = threading.Event()

def receber_mensagens(sock):
    global is_admin
    while True:
        try:
            mensagem = sock.recv(1024).decode()
            if not mensagem:
                break
            if mensagem.startswith("[ADMIN]"):
                is_admin = True
                admin_event.set()  # sinaliza que admin foi identificado
                print("\n🔐 Você é o ADMIN do sistema!")
            print(f'\n📦 {mensagem}\n')
        except:
            print('\n[Erro] Conexão encerrada.')
            break

def menu_usuario():
    print("\n📋 MENU DE USUÁRIO")
    print("1 - Inscrever-se em um item")
    print("2 - Cancelar inscrição")
    print("3 - Listar itens inscritos")
    print("4 - Listar itens Estoque")
    print("5 - Sair")

def menu_admin():
    print("\n🛠️ MENU DE ADMINISTRADOR")
    print("1 - Adicionar item ao estoque")
    print("2 - Remover item do estoque")
    print("3 - Atualizar quantidade de item")
    print("4 - Atualizar preço de item")
    print("5 - Listar estoque")
    print("6 - Sair")

def iniciar_cliente():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        cliente.connect((HOST, PORT))
        print(f'[Conectado] ao servidor {HOST}:{PORT}')
    except ConnectionRefusedError:
        print('[Erro] Não foi possível conectar ao servidor.')
        return

    # Thread para receber mensagens
    thread = threading.Thread(target=receber_mensagens, args=(cliente,))
    thread.daemon = True
    thread.start()

    # Aguarda até saber se é admin ou não (com timeout de segurança)
    admin_event.wait(timeout=2)

    try:
        while True:
            if is_admin:
                menu_admin()
                opcao = input("Escolha uma opção: ").strip()

                if opcao == '1':
                    nome = input("📦 Nome do item: ").strip()
                    qtd = input("🔢 Quantidade inicial: ").strip()
                    preco = input("💲 Preço: ").strip()
                    cliente.sendall(f"ADD:{nome}:{qtd}:{preco}".encode())

                elif opcao == '2':
                    nome = input("❌ Nome do item a remover: ").strip()
                    cliente.sendall(f"REMOVE:{nome}".encode())

                elif opcao == '3':
                    nome = input("🔁 Nome do item: ").strip()
                    qtd = input("📦 Nova quantidade: ").strip()
                    cliente.sendall(f"UPDATE_QTY:{nome}:{qtd}".encode())

                elif opcao == '4':
                    nome = input("💰 Nome do item: ").strip()
                    preco = input("💲 Novo preço: ").strip()
                    cliente.sendall(f"UPDATE_PRICE:{nome}:{preco}".encode())

                elif opcao == '5':
                    cliente.sendall("LIST_STOCK".encode())

                elif opcao == '6':
                    print("\n[Encerrando conexão]")
                    break

                else:
                    print("❌ Opção inválida. Tente novamente.")

            else:
                menu_usuario()
                opcao = input("Escolha uma opção: ").strip()

                if opcao == '1':
                    item = input("🔔 Nome do item para monitorar: ").strip()
                    cliente.sendall(f"SUBSCRIBE:{item}".encode())

                elif opcao == '2':
                    item = input("🚫 Nome do item para cancelar: ").strip()
                    cliente.sendall(f"UNSUBSCRIBE:{item}".encode())

                elif opcao == '3':
                    cliente.sendall("LIST".encode())

                elif opcao == '4':
                    cliente.sendall("LIST_STOCK".encode())


                elif opcao == '5':
                    print("\n[Encerrando conexão]")
                    break

                else:
                    print("❌ Opção inválida. Tente novamente.")

            time.sleep(0.5)

    except KeyboardInterrupt:
        print('\n[Encerrando conexão]')
    finally:
        cliente.close()

if __name__ == '__main__':
    iniciar_cliente()
