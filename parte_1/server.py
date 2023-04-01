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
            print("Data received -> " + data.decode())
            print(file_name)
            if data.decode() == file_name:
                break
            print("Writing file...")
            file.write(data)
    print("File saved to disk.")

    return file_name

def send_file(file_name, addr):
    # Send file name to client
    serverSock.sendto(("SERVER_SENT" + file_name).encode(), addr)

    # Read file to be sent
    with open("./server/RECEIVED_" + file_name, "rb") as file:
        file_data = file.read()

    # Send file data to client (in chunks)
    for i in range(0, len(file_data), BUFFER_SIZE):
        serverSock.sendto(file_data[i:i+BUFFER_SIZE], addr)

    # Send command to client for stop receiving data
    serverSock.sendto(("SERVER_" + file_name).encode(), addr)

def server():
    print("Server started.")
    addr = (UDP_IP_ADDRESS, UDP_PORT_NO)

    print("Receiving file...")
    file_name = receive_file()
    print("File received.")

    while True:
        message, addr = serverSock.recvfrom(BUFFER_SIZE)
        message = message.decode()

        if message == "CONNECTING":
            print("Sending file...")
            send_file(file_name, addr)
            print("File sent.")
            break

    # Close socket
    serverSock.close()

if __name__ == "__main__":
    server()
