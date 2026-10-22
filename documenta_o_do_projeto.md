# UDPdesk — Sistema de Gerenciamento de Chamados de Suporte via Protocolo UDP

> **Instituição:** Projeto Acadêmico de Estrutura de Dados  
> **Integrantes:** Igor, Pyettro e Kayke Ribeiro  
> **Tema:** Fila (*Queue*) aplicada a um sistema de Helpdesk distribuído via Sockets UDP  

---

## 1. Visão Geral do Projeto

O **UDPdesk** é uma solução para o gerenciamento de chamados de suporte técnico em tempo real, baseada na arquitetura cliente-servidor descentralizada. O sistema utiliza a estrutura de dados linear **Fila (*Queue*)** implementada por meio de **Tipos Abstratos de Dados (TAD)** estruturados com dicionários e referências encadeadas (nós), operando sob o protocolo de transporte **UDP (*User Datagram Protocol*)**.

O projeto atende aos requisitos de sistemas assíncronos de atendimento, nos quais os chamados recebidos devem ser processados rigorosamente na ordem de chegada (**FIFO — *First-In, First-Out***), sem a necessidade de manter uma conexão persistente entre os clientes e o servidor central.

---

## 2. Fundamentação Teórica: A Estrutura de Dados Fila (*Queue*)

### 2.1 Conceito e Funcionamento
A **Fila** é uma estrutura de dados linear e dinâmica que segue o princípio do **FIFO (*First-In, First-Out*)**: o primeiro elemento inserido é obrigatoriamente o primeiro a ser removido. 

Diferente de estruturas como a **Pilha (*Stack*)**, que segue a lógica **LIFO (*Last-In, First-Out*)**, a Fila possui dois pontos de acesso bem definidos:
* **`head` (Início/Cabeça):** Ponto por onde ocorrem as operações de remoção (*dequeue* / *pop*).
* **`tail` (Fim/Cauda):** Ponto por onde ocorrem as operações de inserção (*enqueue* / *push*).

```
Entrada (push)                                                 Saída (pop)
    ------->  [ Nó 3 ] ----> [ Nó 2 ] ----> [ Nó 1 ]  ------->
                (tail)                        (head)
```

### 2.2 Análise Computacional e Complexidade Asseptótica

Em implementações ingênuas baseadas em vetores estáticos ou listas contíguas em memória (como o `list` nativo em Python), a remoção do primeiro elemento (`pop(0)`) exige o deslocamento de todos os $n-1$ elementos subsequentes, resultando em uma complexidade de tempo de **$O(n)$**.

Para solucionar essa ineficiência, este projeto adota uma **Fila Encadeada orientada a Nós (*Node-based Linked Queue*)**, mantendo referências diretas para o `head` e o `tail`.

| Operação | Função | Descrição | Complexidade de Tempo |
| :--- | :--- | :--- | :---: |
| **`initialize_queue`** | Inicialização | Aloca a estrutura da fila com `head=None`, `tail=None` e `size=0`. | $O(1)$ |
| **`push`** | Enfileirar (*Enqueue*) | Insere um novo nó no final da fila (`tail`). | $O(1)$ |
| **`pop`** | Desenfileirar (*Dequeue*) | Remove e retorna o nó do início da fila (`head`). | $O(1)$ |
| **`peek`** | Espiar (*Front*) | Consulta o valor armazenado no `head` sem alterá-lo. | $O(1)$ |
| **`is_empty`** | Validação | Verifica se a quantidade de elementos é igual a zero. | $O(1)$ |
| **`get_all`** | Travessia | Percorre os ponteiros `next` do `head` até o `tail` para listagem. | $O(n)$ |

### 2.3 Vantagens e Desvantagens da Fila Encadeada via TADs

#### Vantagens:
* **Garantia de Ordem Histórica (Fairness):** Garante a ordem de chegada dos chamados de suporte.
* **Eficiência Operacional $O(1)$:** As operações fundamentais (`push` e `pop`) são executadas em tempo constante, independentemente da quantidade de elementos.
* **Alocação Dinâmica:** Permite o crescimento da fila de acordo com a demanda do sistema sem alocação prévia de blocos fixos de memória.
* **Baixa Abstração e Transparência Pedagógica:** A implementação sem o uso de Orientação a Objetos (classes) expõe explicitamente o manuseio dos ponteiros (`next`/`previous`) e estruturas em dicionários.

#### Desvantagens:
* **Sem Acesso Aleatório:** Para acessar o $k$-ésimo elemento da fila, é necessário percorrer sequencialmente $k$ nós ($O(n)$).
* **Overhead de Memória:** Cada elemento necessita armazenar referências adicionais de ponteiros (`next` e `previous`) além do próprio dado (*payload*).

---

## 3. Arquitetura de Rede e Comunicação (Protocolo UDP)

O sistema utiliza o protocolo **UDP (*User Datagram Protocol*)** na camada de transporte (modelo OSI/TCP-IP).

```
+------------------------------------+         Protocolo UDP          +------------------------------------+
|  Aplicação 1: Servidor / Usuário   | <----------------------------> |   Aplicação 2: Painel do Técnico   |
|  (socket_udp.py)                   |    Socket DGRAM (Porta 5000)   |   (socket_udp_client.py)           |
|  - Gerencia Fila na Memória        |                                |   - Menu Interativo                |
|  - Abertura Local de Chamados      |                                |   - Envio de Comandos e Consultas  |
+------------------------------------+                                +------------------------------------+
```

### Por que UDP em vez de TCP neste projeto?
1. **Modelagem de Datagramas Independentes:** Cada comando transmitido (ex: `ATENDER`, `TAMANHO`, `ESPIAR`) é empacotado e enviado como uma unidade autônoma de mensagem.
2. **Sem Overhead de Conexão:** Elimina o processo de *three-way handshake* do TCP, tornando as trocas de mensagens instantâneas.
3. **Simulação de Comunicação Assíncrona:** Demonstra como sistemas de mensageria em tempo real interagem com estruturas de dados residentes em memória.

---

## 4. Detalhamento dos Arquivos do Projeto

### 4.1 `TADs.py` — Tipo Abstrato de Dados
Este arquivo define a estrutura das entidades fundamentais do sistema por meio de dicionários Python:

```python
def initialize_node(value):
    """
    Cria um nó contendo o valor do chamado e referências para
    os nós adjacentes (encadeamento duplo).
    """
    return {
        'value': value,
        'previous': None,
        'next': None
    }

def initialize_queue():
    """
    Inicializa a Fila mantendo o controle da cabeça (head),
    cauda (tail) e contagem total de itens.
    """
    return {
        'head': None,
        'tail': None,
        'size': 0
    }
```

### 4.2 `operations.py` — Regras de Negócio e Manipulação de Ponteiros
Contém as funções de manipulação da estrutura de dados:

* **`is_empty(queue)`**: Retorna `True` se `queue['size'] == 0`.
* **`push(queue, value)`**: Instancia um novo nó. Caso a fila esteja vazia, define o novo nó como `head` e `tail`. Caso contrário, ajusta o ponteiro `next` do `tail` atual para o novo nó e atualiza o `tail`.
* **`pop(queue)`**: Trata o cenário de *Underflow* (fila vazia). Se houver elementos, isola o nó em `head`, avança o ponteiro `head` para `head['next']`, ajusta os ponteiros do nó remanescente e decrementa o tamanho.
* **`peek(queue)`**: Retorna `queue['head']['value']` sem alterar a fila.
* **`get_all(queue)`**: Realiza uma varredura encadeada do `head` ao `tail`, acumulando os valores em uma lista para exibição.

### 4.3 `socket_udp.py` — Servidor e Aplicação 1 (Painel do Usuário)
Responsável por:
1. Manter a instância da Fila em memória ativa durante a execução.
2. Criar o socket UDP (`AF_INET`, `SOCK_DGRAM`) vinculado ao endereço `127.0.0.1:5000`.
3. Utilizar multiplexação E/S via módulo `select` com soquete não-bloqueante (`setblocking(False)`), permitindo que o servidor aceite digitação no terminal local para inserção de chamados ao mesmo tempo em que escuta solicitações de rede.
4. Processar comandos serializados em JSON recebidos dos clientes e enviar as respostas correspondentes.

### 4.4 `socket_udp_client.py` — Cliente e Aplicação 2 (Painel do Técnico)
Responsável por:
1. Fornecer a interface CLI interativa para o técnico de suporte.
2. Formatar e enviar mensagens de texto contendo os comandos operacionais (`ATENDER`, `TAMANHO`, `ESPIAR`, `IMPRIMIR`).
3. Implementar controle de tempo limite via tratamento de exceção `TimeoutError` para evitar o travamento da aplicação caso o servidor esteja inacessível.

---

## 5. Roteiro de Execução e Demonstração

### Passos para Execução no VS Code / Terminal PowerShell:

1. **Ativação do Ambiente Virtual:**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

2. **Inicialização do Servidor (Terminal 1 - Esquerda):**
   ```powershell
   python socket_udp.py
   ```

3. **Inicialização do Cliente (Terminal 2 - Direita):**
   ```powershell
   python socket_udp_client.py
   ```

4. **Sequência de Teste Operacional:**
   * **Inserção:** Cadastrar 3 chamados no Terminal 1.
   * **Listagem:** Digitar opção `4` no Terminal 2 para confirmar a ordem de inserção.
   * **Consulta de Frente:** Digitar opção `3` no Terminal 2 para verificar o próximo chamado a ser atendido.
   * **Remoção (FIFO):** Digitar opção `1` no Terminal 2 para atender o chamado e validar a remoção do primeiro elemento inserido.
   * **Tratamento de Borda (*Underflow*):** Esvaziar a fila e acionar a opção `1` novamente para demonstrar a mensagem de tratamento de erro sem falha de execução (*crash*).

---

## 6. Conclusão

O projeto **UDPdesk** demonstra a aplicação prática da estrutura de dados **Fila Encadeada** na solução de problemas reais de ordenação e atendimento de chamados. A escolha pela implementação fundamentada em Tipos Abstratos de Dados (TAD) e dicionários permitiu o domínio explícito da manipulação de ponteiros e alocação de memória, enquanto o protocolo UDP garantiu uma arquitetura de rede simples, rápida e eficiente.