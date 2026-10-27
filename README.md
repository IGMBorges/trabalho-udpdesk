# UDPdesk

Sistema acadêmico de gerenciamento de chamados de suporte usando uma fila FIFO e comunicação cliente-servidor por UDP.

## Sobre o projeto

O UDPdesk simula um helpdesk distribuído com duas aplicações:

- **Servidor/usuário:** recebe novos chamados pelo terminal e mantém a fila em memória.
- **Cliente/técnico:** envia comandos UDP para consultar e atender os chamados.

A fila foi implementada manualmente com nós encadeados e dicionários Python, mantendo as referências `head`, `tail` e `size`. As operações principais de inserção e remoção têm complexidade `O(1)`.

## Tecnologias

- Python 3
- Sockets UDP (`socket.AF_INET` e `socket.SOCK_DGRAM`)
- Estrutura de dados fila FIFO
- Comunicação local em `127.0.0.1:5000`

O projeto utiliza apenas a biblioteca padrão do Python e não exige dependências externas.

## Como executar

### 1. Clone o repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd trabalho-udpdesk
```

### 2. Opcionalmente, crie e ative um ambiente virtual

No Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

No Linux ou macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Inicie o servidor

Em um terminal:

```bash
python socket_udp.py
```

Digite as descrições dos chamados no terminal do servidor. Para encerrar a aplicação, digite `sair`.

### 4. Inicie o cliente

Em outro terminal, dentro da mesma pasta:

```bash
python socket_udp_client.py
```

O cliente exibirá o painel interativo do técnico.

## Operações disponíveis

| Opção | Comando UDP | Ação |
| --- | --- | --- |
| `1` | `ATENDER` | Remove e atende o primeiro chamado da fila |
| `2` | `TAMANHO` | Exibe a quantidade atual de chamados |
| `3` | `ESPIAR` | Consulta o próximo chamado sem removê-lo |
| `4` | `IMPRIMIR` | Lista todos os chamados na ordem de chegada |
| `0` | — | Encerra o cliente |

## Exemplo de fluxo

1. Inicie o servidor e cadastre alguns chamados, como `Computador não liga` e `Erro de acesso ao sistema`.
2. Inicie o cliente em outro terminal.
3. Use a opção `4` para visualizar a fila.
4. Use a opção `3` para consultar o próximo chamado.
5. Use a opção `1` para atendê-lo e removê-lo da fila.

Os chamados são atendidos no modelo **FIFO** (*First In, First Out*): o primeiro chamado inserido é o primeiro a ser atendido.

## Estrutura do projeto

```text
.
├── TADs.py                 # Estruturas de nó e fila
├── operations.py           # Operações push, pop, peek e get_all
├── socket_udp.py           # Servidor UDP e entrada de chamados
├── socket_udp_client.py    # Cliente UDP e painel do técnico
├── documenta_o_do_projeto.md
└── .gitignore
```

## Observações

- O servidor deve ser iniciado antes do cliente.
- A fila existe apenas durante a execução do servidor; os chamados não são persistidos em arquivo ou banco de dados.
- A configuração padrão aceita conexões somente localmente (`127.0.0.1`). Para executar em máquinas diferentes, altere `HOST` no servidor e no cliente conforme a rede utilizada.
- Como o projeto usa UDP, a comunicação não possui conexão persistente nem garantia de entrega; o cliente possui um tempo limite de 5 segundos para respostas.

## Contexto acadêmico

Projeto desenvolvido para demonstrar a aplicação de uma fila encadeada, tipos abstratos de dados e comunicação entre processos por sockets UDP.

