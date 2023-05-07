import socket

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 6789
BUFFER_SIZE = 1024

# Criando o socket UDP
clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Função para calcular o checksum dos pacotes de dados
def calculate_checksum(packet):
    return sum(packet) % 256

# Função para enviar um pacote de dados para o servidor
def send_packet(data, seq_num, addr):
    checksum = calculate_checksum(seq_num.to_bytes(2, byteorder='big') + data)
    packet = seq_num.to_bytes(2, byteorder='big') + data + checksum.to_bytes(1, byteorder='big')
    clientSock.sendto(packet, addr)

# Função para receber um pacote de dados do servidor
def receive_packet(expected_seq_num):
    while True:
        packet, addr = clientSock.recvfrom(BUFFER_SIZE)
        seq_num = int.from_bytes(packet[:2], byteorder='big')
        data = packet[2:-1]
        checksum = int.from_bytes(packet[-1:], byteorder='big')
        if seq_num == expected_seq_num and checksum == calculate_checksum(packet):
            return data, addr

# Função para enviar um arquivo para o servidor
def send_file(file_name):
    # enviando
    clientSock.sendto(file_name.encode(), (UDP_IP_ADDRESS, UDP_PORT_NO))

    # Ler arquivo a ser enviado
    with open("./client/" + file_name, "rb") as file:
        file_data = file.read()

    # Divide os dados em pacotes menores para transmitir e reconstruir o arquivo original no receptor
    packets = [file_data[i:i+BUFFER_SIZE] for i in range(0, len(file_data), BUFFER_SIZE)]

    # Envia os pacotes para o servidor
    seq_num = 0
    for packet in packets:
        send_packet(packet, seq_num, (UDP_IP_ADDRESS, UDP_PORT_NO))
        print("Waiting for ACK")
        # Espera pelo acknowledgement do servidor
        while True:
            data, addr = receive_packet(seq_num)
            if data == b"ACK":
                print("ACK RECEIVED")
                seq_num = (seq_num + 1) % 2
                break

    # Comando p/ o server para parar de receber dados
    print("Sending file name to server for stop receiving data...")
    clientSock.sendto(file_name.encode(), (UDP_IP_ADDRESS, UDP_PORT_NO))
def receive_file():
    print("ENTROU NO RECEIVE FILE")

    # envia mensagem de conexao ao servidor
    print("Sending connect message to server...")
    connectingMessage = "CONNECTING"
    clientSock.sendto(connectingMessage.encode(), (UDP_IP_ADDRESS, UDP_PORT_NO))

    # espera a conexão
    while True:
        data, addr = clientSock.recvfrom(BUFFER_SIZE)
        print("Waiting for server to connect...")
        if data == "CONNECTED".encode():
            break
    print("Server connected. receiving file name...")

    # Recebe nome do arquivo do servidor
    file_name, addr = clientSock.recvfrom(BUFFER_SIZE)
    file_name = file_name.decode()

    print("File name received on CLIENT: " + file_name)

    # Lista para armazenar os pacotes recebidos
    received_packets = [None, None]
    expected_seq_num = 0

    # Recebe os pacotes de dados do servidor e escreve no arquivo
    with open("./client/RECEIVED_" + file_name, "wb") as file:
        while True:
            print("Receiving data on CLIENT...")
            data, addr = receive_packet(expected_seq_num)

            # Para de receber dados quando comando é recebido pelo servidor
            if data == file_name.encode():
                print("BREAK")
                break

            received_packets[expected_seq_num] = data
            # Mandando ACKs p/ o servidor
            clientSock.sendto(b"ACK", addr)

            # Verifica se o pacote esperado foi recebido
            while received_packets[expected_seq_num] is not None:
                file.write(received_packets[expected_seq_num])
                received_packets[expected_seq_num] = None
                expected_seq_num = (expected_seq_num + 1) % 2

    print("File saved to disk on CLIENT.")

# Função principal do cliente
def client():
    print("Client started.")
    files = ["file_to_send.txt", "pdf_to_send.pdf", "img_to_send.png"]
    clientSock.sendto(str(len(files)).encode(), (UDP_IP_ADDRESS, UDP_PORT_NO))

    # Envia e recebe todos arquivos
    for file in files:
        print("Sending file...")
        send_file(file)
        print("File sent.")

        print("Receiving file...")
        receive_file()
        print("File received.")

    # Fecha o socket do cliente
    clientSock.close()

if __name__ == "__main__":
    client()