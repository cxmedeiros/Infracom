import socket

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 6789
BUFFER_SIZE = 1024

# Create socket and bind to port
serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))

def receive_file():
    # Receive file name from client
    file_name, addr = serverSock.recvfrom(BUFFER_SIZE)
    file_name = file_name.decode()

    # Servidor recebe dados do cliente e escreve no arquivo

    with open("./server/RECEIVED_" + file_name, "wb") as file:
        while True:
            data, addr = serverSock.recvfrom(BUFFER_SIZE)

            print(file_name)
            if data == file_name.encode():
                break

            print("Writing file...")
            file.write(data)
            # send ACK to client
            serverSock.sendto("ACK".encode(), addr)

    print("File saved to disk.")

    return file_name

def send_file(file_name, addr):
    # Send file name to client
    serverSock.sendto(file_name.encode(), addr)

    # Read file to be sent
    with open("./server/RECEIVED_" + file_name, "rb") as file:
        file_data = file.read()

    # Send file data to client (in chunks)
    for i in range(0, len(file_data), BUFFER_SIZE):
        serverSock.sendto(file_data[i:i+BUFFER_SIZE], addr)
        print("waiting for ACK")
        while True:
            data, addr = serverSock.recvfrom(BUFFER_SIZE)
            if data == "ACK".encode():
                print("ACK RECEIVED")
                break

    # Send command to client for stop receiving data
    serverSock.sendto(file_name.encode(), addr)

def resend_file(file_name, addr):
    while True:
        message, addr = serverSock.recvfrom(BUFFER_SIZE)
        message = message.decode()

        if message == "CONNECTING":
            print("Client connected.")
            # Send connected message to client
            serverSock.sendto("CONNECTED".encode(), addr)
            print("Connected message sent.")

            print("Sending file...")
            send_file(file_name, addr)
            print("File sent.")
            break


def server():
    print("Server started.")
    addr = (UDP_IP_ADDRESS, UDP_PORT_NO)

    # getting file amount to receive
    while True:
        file_amount, addr = serverSock.recvfrom(BUFFER_SIZE) 
        if file_amount.decode().isnumeric():
            break

    for i in range(int(file_amount.decode())):
        print("Receiving file...")
        file_name = receive_file()
        print("File received.")

        print("Resending file...")
        resend_file(file_name, addr)

    # Close socket
    serverSock.close()

if __name__ == "__main__":
    server()