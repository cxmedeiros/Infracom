# from socket import settimeout
import socket

IP_ADDRESS = "127.0.0.1"
PORT_NO = 6789
BUFFER_SIZE = 1024

def ack_confirm(ack, seq_num):
    return ack == seq_num

def seq_num_change(seq_num):
    if seq_num == '0':
        return '1'
    else:
        return '0'
    
def is_waiting_ack(waiting):
    return waiting

def rdtSending(socket, chunk, addr, seq_num, waiting):
    print("Sending package...")
    waiting = False

    # Criando o pacote com número de sequência e dado.
    pkt = seq_num + "," + chunk
    print(pkt)

    # Enquanto está no estado de espera pelo ack correto, continua retransmitindo o último pacote enviado após timeout.
    while not waiting:
        print(f"Sending package with: ({seq_num}, \"{chunk}\")")
        socket.sendto(pkt.encode(), addr)

        # Ligando o temporizador
        socket.settimeout(5)

        try:
            ack, addr = socket.recvfrom(BUFFER_SIZE)
        except socket.timeout:
            # Detectando timeout.
            print("Timeout!\n\n")
            continue

        # Verificando se o ack recebido é correto.
        if ack_confirm(ack.decode(), seq_num):
            print("The ack is correct!\n\n")

            # Desligando o temporizador
            socket.settimeout(None)
            # Atualizando o número de sequência.
            seq_num = seq_num_change(seq_num)

            # Voltando para o estado de espera pela transmissão de uma nova mensagem.
            waiting = True

    return seq_num, waiting


