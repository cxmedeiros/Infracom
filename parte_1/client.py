import socket

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 6789
BUFFER_SIZE = 1024

# Create socket
clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Read file to be sent
with open("./client/file_to_send.txt", "rb") as file:
    file_data = file.read()

def send_file(file_name):
    # Send file name to server
    clientSock.sendto(file_name.encode(), (UDP_IP_ADDRESS, UDP_PORT_NO))

    # Read file to be sent
    with open("./client/" + file_name, "rb") as file:
        file_data = file.read()     

    # Send file data to server (in chunks)
    for i in range(0, len(file_data), BUFFER_SIZE):
        clientSock.sendto(file_data[i:i+BUFFER_SIZE], (UDP_IP_ADDRESS, UDP_PORT_NO))

    # Send command to server for stop receiving data
    clientSock.sendto(file_name.encode(), (UDP_IP_ADDRESS, UDP_PORT_NO))

def receive_file():
    print("ENTROU NO RECEIVE FILE")

    # Receive file name from server
    connectingMessage = "CONNECTING"
    clientSock.sendto(connectingMessage.encode(), (UDP_IP_ADDRESS, UDP_PORT_NO))

    # Receive file name from server
    file_name, addr = clientSock.recvfrom(BUFFER_SIZE)
    file_name = file_name.decode()

    print("File name received on CLIENT: " + file_name)

    # Cliente recebe dados do servidor e escreve no arquivo
    with open("./client/RECEIVED_" + file_name, "wb") as file:
        while True:
            print("Receiving data on CLIENT...")
            data, addr = clientSock.recvfrom(BUFFER_SIZE)
            print("Data received." + data.decode())
            if data.decode() == file_name:
                break
            file.write(data)
    print("File saved to disk on CLIENT.")


def client():
    print("Client started.")

    print("Sending file...")
    send_file("file_to_send.txt")
    print("File sent.")

    print("Receiving file...")
    receive_file()
    print("File received.")

    # Close socket
    clientSock.close()

if __name__ == "__main__":
    client()