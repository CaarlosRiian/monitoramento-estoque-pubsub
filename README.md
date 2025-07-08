# 🧠 Sistema de Monitoramento de Estoque - Arquitetura Publish/Subscribe

Este projeto implementa um sistema de **monitoramento de estoque em tempo real**, utilizando a arquitetura **Pub/Sub (Publish-Subscribe)** com **sockets e threading** em Python.

O sistema permite que diferentes clientes se inscrevam para receber notificações sobre **itens de estoque específicos**, visualizando atualizações instantaneamente à medida que ocorrem.

---

## 🧱 Arquitetura

```bash
+----------+        +-------------+        +----------+
| Cliente  |<----->| Servidor Pub|<-----> | Cliente  |
| (Socket) |        |     Sub     |        | (Socket) |
+----------+        +-------------+        +----------+
```

* **Servidor**: Mantém controle de inscrições, despacha mensagens para clientes conectados e gerencia a lógica Pub/Sub.
* **Clientes**: Conectam ao servidor, se inscrevem em itens e recebem atualizações em tempo real.
* **Canal de Comunicação**: Sockets TCP (via biblioteca `socket`).

---

## 📦 Funcionalidades

### 🔁 Publish/Subscribe

* **SUBSCRIBE:** Inscreve o cliente em um item para receber atualizações.
* **UNSUBSCRIBE:** Cancela a inscrição.
* **UPDATE:** Envia uma atualização sobre um item para todos os inscritos.
* **LIST:** Lista os itens nos quais o cliente está inscrito.

---

## 🚀 Como Executar

### ✅ Requisitos

* Python 3.8+
* Sistema operacional compatível com sockets (Linux, Windows, macOS)

---

### 1. Clonar o repositório

```bash
git clone https://github.com/CaarlosRiian/monitoramento-estoque-pubsub
cd monitoramento-estoque-pubsub
```

---

### 2. Rodar o servidor

```bash
python servidor.py
```

---

### 3. Rodar o cliente com interface de terminal

```bash
python cliente.py
```

Você pode abrir vários terminais para executar múltiplos clientes simultaneamente.

---

## 📁 Estrutura do Projeto

```
monitoramento-estoque-pubsub/
│
├── servidor.py              # Lógica principal do servidor Pub/Sub
├── cliente.py               # Cliente base (envia comandos direto)
├── README.md                # Este arquivo
```

---

## 💬 Comandos Internos do Sistema
Claro! Aqui está a versão atualizada da seção **“💬 Comandos Internos do Sistema”**, incluindo os comandos **exclusivos do administrador**:

---

## 💬 Comandos Internos do Sistema

### 📦 Comandos Gerais (Todos os Usuários)

| Comando         | Exemplo                             | Descrição                                                  |
| --------------- | ----------------------------------- | -----------------------------------------------------------|
| `SUBSCRIBE`     | `SUBSCRIBE:mouse`                   | Inscreve o cliente para atualizações do item `mouse`.      |
| `UNSUBSCRIBE`   | `UNSUBSCRIBE:mouse`                 | Cancela a inscrição do cliente no item `mouse`.            |
| `UPDATE`        | `UPDATE:mouse:Chegaram 20 unidades` | Envia uma atualização sobre o item para os assinantes.     |
| `LIST`          | `LIST`                              | Lista todos os itens que o cliente está monitorando.       |
| `LIST_STOCK`    | `LIST_STOCK`                        | Lista todos os produtos do estoque com quantidade e preço. |
| `sair` / `exit` |                                     | Encerra a conexão com o servidor.                          |

---

### 🔐 Comandos Exclusivos do Admin

| Comando        | Exemplo                       | Descrição                                                             |
| -------------- | ----------------------------- | --------------------------------------------------------------------- |
| `ADD`          | `ADD:teclado:100:150.00`      | Adiciona um novo item `teclado` com quantidade 100 e preço R\$150.00. |
| `REMOVE`       | `REMOVE:teclado`              | Remove o item `teclado` do estoque.                                   |
| `UPDATE_QTY`   | `UPDATE_QTY:teclado:80`       | Atualiza a quantidade do item `teclado` para 80 unidades.             |
| `UPDATE_PRICE` | `UPDATE_PRICE:teclado:135.90` | Atualiza o preço do item `teclado` para R\$135.90.                    |


---


## 🛠️ Tecnologias Utilizadas

* **Python**
* **Sockets TCP**
* **Threading (concorrência leve para múltiplos clientes)**

---

## 🎓 Aplicação Acadêmica

Esta aplicação foi desenvolvida como parte da **Atividade Prática 03 - Arquitetura Baseada em Mensagens** do curso de ADS. Ela demonstra como a arquitetura Pub/Sub pode ser implementada de forma simples e eficiente com sockets, sem a necessidade de ferramentas como Kafka ou RabbitMQ.

---

## 📚 Aprendizados

* Como funciona a arquitetura Publish/Subscribe.
* Implementação de sockets em Python.
* Controle de múltiplos clientes com threading.
* Estruturação de comandos e mensagens via protocolo textual simples.
* Aplicações práticas em sistemas distribuídos e de monitoramento.

## 🤝 Contribuidores

* Eduardo
* Rian
