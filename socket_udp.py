# Servidor UDP - Aplicação 1
import json
import select
import socket
import threading

import operations
import TADs

HOST = '127.0.0.1'
PORTA = 5000

# Inicializa a Fila
fila_suporte = TADs.initialize_queue()
id_counter = 1
encerrar = threading.Event()
fila_lock = threading.Lock()

servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servidor_socket.bind((HOST, PORTA))
servidor_socket.setblocking(False)

print('=' * 55)
print('     UDPdesk - APLICAÇÃO 1 (USUÁRIO / SERVIDOR)')
print(f' Escutando em {HOST}:{PORTA}')
print('=' * 55)


def receber_chamados_localmente():
    global id_counter

    while not encerrar.is_set():
        try:
            desc = input(
                "\nInsira a descricao do chamado (ou 'sair'): ").strip()
        except EOFError:
            encerrar.set()
            break

        if desc.lower() == 'sair':
            encerrar.set()
            break

        if desc:
            chamado = {
                'id': id_counter,
                'desc': desc
            }

            with fila_lock:
                operations.push(fila_suporte, chamado)

            print(f'Chamado #{id_counter} registrado na Fila!')
            id_counter += 1


thread_entrada = threading.Thread(
    target=receber_chamados_localmente,
    daemon=True
)

thread_entrada.start()

try:
    while not encerrar.is_set():
        prontos, _, _ = select.select([servidor_socket], [], [], 0.1)

        if not prontos:
            continue

        dados, endereco_cliente = servidor_socket.recvfrom(1024)
        comando = dados.decode('utf-8').strip()
        resposta = {}

        with fila_lock:
            if comando == 'ATENDER':
                chamado = operations.pop(fila_suporte)

                if chamado:
                    resposta = {
                        'status': 'OK',
                        'msg': f'Atendendo chamado #{chamado["id"]}: {chamado["desc"]}',
                    }
                else:
                    resposta = {
                        'status': 'ERRO',
                        'msg': 'A fila de suporte esta vazia!'
                    }

            elif comando == 'TAMANHO':
                resposta = {
                    'status': 'OK',
                    'msg': f'O tamanho atual da fila e: {fila_suporte["size"]}',
                }

            elif comando == 'ESPIAR':
                proximo = operations.peek(fila_suporte)

                if proximo:
                    resposta = {
                        'status': 'OK',
                        'msg': f'Proximo: #{proximo["id"]} - {proximo["desc"]}',
                    }
                else:
                    resposta = {
                        'status': 'ERRO',
                        'msg': 'Nenhum chamado pendente.'
                    }

            elif comando == 'IMPRIMIR':
                todos = operations.get_all(fila_suporte)

                if todos:
                    lista_str = ', '.join(
                        f'#{c["id"]} ({c["desc"]})'
                        for c in todos
                    )
                    resposta = {
                        'status': 'OK',
                        'msg': f'Fila atual: [{lista_str}]'
                    }
                else:
                    resposta = {
                        'status': 'OK',
                        'msg': 'Fila vazia.'
                    }

            else:
                resposta = {
                    'status': 'ERRO',
                    'msg': 'Comando desconhecido.'
                }

        servidor_socket.sendto(
            json.dumps(resposta).encode('utf-8'),
            endereco_cliente
        )

except KeyboardInterrupt:
    print('\nEncerrando...')

finally:
    encerrar.set()
    servidor_socket.close()
