import socket
from rdtReceiver import *
from rdtSender import *

# Definir o endereço IP e a porta do servidor
IP_ADDRESS = "localhost"
PORT_NO = 6789
BUFFER_SIZE = 1024

def server():
    # Create a socket and bind it to a local address
    serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSock.bind((IP_ADDRESS, PORT_NO))
    print("Server started.\n")

    waiting = True
    seq_num = '0'
    expected_seq_num = '0'

    for i in range(2):
        print("Waiting for client's message...")
        msg, addr = serverSock.recvfrom(BUFFER_SIZE)
        seq_num, _ = msg.decode().split(',')

        print("msg: ", msg)
        print("seq_num: ", seq_num)

        print("Receiving message from rdtReceiver: ")
        rdtReceiving(serverSock, addr, seq_num, expected_seq_num)
        print("Received message | Sequence number: ", seq_num)

        if waiting:
            print("Sending new package in server...")
            # Enviando a mensagem por um canal confiável de transferência de dados.
            seq_num, waiting = rdtSending(serverSock, "Hello from server!", addr, seq_num, waiting)

    # Close the socket
    serverSock.close()

if __name__ == '__main__':
    server()
