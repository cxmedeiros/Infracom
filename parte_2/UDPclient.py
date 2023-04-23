import socket
from rdtSender import *
from rdtReceiver import *
import struct

IP_ADDRESS = "localhost"
PORT_NO = 6789
BUFFER_SIZE = 1024

def client():
    # Criando o socket
    clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Client started.")

    waiting_ack = True
    seq_num = '0'

    for i in range(2):
        data = "Hello from client!"

        if waiting_ack:
            print("Sending new package in client...")
            seq_num, waiting_ack = rdtSending(clientSock, data, (IP_ADDRESS, PORT_NO), seq_num, waiting_ack)

        print("Waiting for server's message...")
        msg, addr = clientSock.recvfrom(BUFFER_SIZE)
        seq_num, _ = msg.decode().split(',')

        print("Receiving message from rdtReceiver: ")
        print("Sequence number: ", seq_num)
        rdtReceiving(seq_num, addr)

    # Close the socket
    clientSock.close()

if __name__ == "__main__":
    client()
