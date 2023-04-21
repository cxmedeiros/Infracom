import socket
import struct

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 6789
BUFFER_SIZE = 1024

receiverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))

# RDT3.0 protocol implementation
def rdt_receive():
    expected_seq_num = 0
    received_data = b""
    while True:
        data, addr = receiverSock.recvfrom(BUFFER_SIZE)
        pkt_seq_num, pkt_checksum, pkt_data = unpack_packet(data)
        
        if pkt_checksum != calculate_checksum(pkt_data):
            print("Packet with incorrect checksum received. Discarding...")
            continue
        
        if pkt_seq_num != expected_seq_num:
            print("Packet with incorrect sequence number received. Discarding...")
            ack_pkt = make_ack_packet(not expected_seq_num)
        else:
            received_data += pkt_data
            ack_pkt = make_ack_packet(expected_seq_num)
            expected_seq_num = 1 - expected_seq_num
        
        receiverSock.sendto(ack_pkt, addr)
        
        if pkt_seq_num == 1:
            break
    
    return received_data

# Helper functions for packet creation and manipulation
def make_packet(seq_num, data):
    checksum = calculate_checksum(data)
    return struct.pack("!HH", seq_num, checksum) + data

def unpack_packet(packet):
    seq_num, checksum = struct.unpack("!HH", packet[:4])
    data = packet[4:]
    return seq_num, checksum, data

def make_ack_packet(seq_num):
    return struct.pack("!HH", seq_num, 0)

def calculate_checksum(data):
    checksum = 0
    for i in range(0, len(data), 2):
        if i + 1 < len(data):
            chunk = (data[i] << 8) + data[i+1]
            checksum += chunk
        else:
            chunk = data[i]
            checksum += chunk
    checksum = (checksum >> 16) + (checksum & 0xffff)
    checksum = ~checksum & 0xffff
    return checksum

def rdt_receiver():
    data = rdt_receive()
    # Do something with the received data
    print("Received data: " + data.decode())

if __name__ == "__main__":
    rdt_receiver()