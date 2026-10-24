# Cliente UDP - Aplicação 2
import json
import socket

HOST = '127.0.0.1'
PORTA = 5000

cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cliente_socket.settimeout(5.0)


def enviar_comando(comando):
    try:
        cliente_socket.sendto(
            comando.encode('utf-8'),
            (HOST, PORTA)
        )

        dados, _ = cliente_socket.recvfrom(1024)
        resposta = json.loads(dados.decode('utf-8'))

        return resposta.get(
            'msg',
            'Resposta inválida do servidor.'
        )

    except TimeoutError:
        return 'Erro: Servidor UDP nao respondeu.'

    except (OSError, json.JSONDecodeError):
        return 'Erro ao comunicar com o servidor.'


def menu():
    while True:
        print('\n' + '=' * 35)
        print('    PAINEL DO TÉCNICO (APLICAÇÃO 2)')
        print('=' * 35)
        print('1 - Atender proximo chamado (pop)')
        print('2 - Exibir tamanho da fila (size)')
        print('3 - Espiar proximo chamado (peek)')
        print('4 - Imprimir fila inteira')
        print('0 - Sair')

        opcao = input('>> ').strip()

        if opcao in ['1', '2', '3', '4']:
            cmds = {'1': 'ATENDER', '2': 'TAMANHO',
                    '3': 'ESPIAR', '4': 'IMPRIMIR'}
            print(f'\n{enviar_comando(cmds[opcao])}')
        elif opcao == '0':
            break


if __name__ == '__main__':
    try:
        menu()
    finally:
        cliente_socket.close()
