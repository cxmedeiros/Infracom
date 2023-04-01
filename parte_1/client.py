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
        print("waiting for ACK")
        while True:
            data, addr = clientSock.recvfrom(BUFFER_SIZE)
            if data == "ACK".encode():
                print("ACK RECEIVED")
                break

    # Send command to server for stop receiving data
    print("Sending file name to server for stop receiving data...")
    clientSock.sendto(file_name.encode(), (UDP_IP_ADDRESS, UDP_PORT_NO))

def receive_file():
    print("ENTROU NO RECEIVE FILE")

    # Receive file name from server
    print("Sending connect message to server...")
    connectingMessage = "CONNECTING"
    clientSock.sendto(connectingMessage.encode(), (UDP_IP_ADDRESS, UDP_PORT_NO))

    while True:
        data, addr = clientSock.recvfrom(BUFFER_SIZE)

        print("Waiting for server to connect...")
        if data == "CONNECTED".encode():
            break
    print("Server connected. receiving file name...")

    # Receive file name from server
    file_name, addr = clientSock.recvfrom(BUFFER_SIZE)
    file_name = file_name.decode()

    print("File name received on CLIENT: " + file_name)

    # Cliente recebe dados do servidor e escreve no arquivo
    with open("./client/RECEIVED_" + file_name, "wb") as file:
        while True:
            print("Receiving data on CLIENT...")
            data, addr = clientSock.recvfrom(BUFFER_SIZE)

            if data == file_name.encode():
                print("BREAK")
                break

            file.write(data)
            # send ACK to client
            clientSock.sendto("ACK".encode(), addr)
    print("File saved to disk on CLIENT.")


def client():
    print("Client started.")
    files = ["file_to_send.txt", "pdf_to_send.pdf", "img_to_send.png"]
    # files = ["file_to_send.txt"]
    clientSock.sendto(str(len(files)).encode(), (UDP_IP_ADDRESS, UDP_PORT_NO))


    for file in files:
        print("Sending file...")
        send_file(file)
        print("File sent.")

        print("Receiving file...")
        receive_file()
        print("File received.")

    # Close socket
    clientSock.close()

if __name__ == "__main__":
    client()