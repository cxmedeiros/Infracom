import socket

# Definir o endereço IP e a porta do servidor
IP_ADDRESS = "127.0.0.1"
PORT_NO = 6789
BUFFER_SIZE = 1024

def client():
    # Create a socket
    clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Client started.\n")

    # Connect to the server
    clientSock.connect((IP_ADDRESS, PORT_NO))
    print("Connected to server.\n")

    # Send a message to the server
    clientSock.send(b'9, Init message!')
    print("Sent to server: 9, Init message!\n")

    clientSock.send(b'0, Hello from client 0!')

    # Receive a message from the server
    print("Waiting for server's message...")
    msg = clientSock.recv(BUFFER_SIZE)
    print("Received from server:", msg)

    clientSock.send(b'2, Hello from client 2!')

    # Receive a message from the server
    print("Waiting for server's message...")
    msg = clientSock.recv(BUFFER_SIZE)
    print("Received from server:", msg)

    clientSock.send(b'3, Hello from client 3!')

    # Receive a message from the server
    print("Waiting for server's message...")
    msg = clientSock.recv(BUFFER_SIZE)
    print("Received from server:", msg)

    # Receive a message from the server
    print("Waiting for server's message...")
    msg = clientSock.recv(BUFFER_SIZE)
    print("Received from server:", msg)

    # Close the socket
    clientSock.close()

if __name__ == '__main__':
    client()