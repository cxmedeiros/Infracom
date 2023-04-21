import socket
import random
import time

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 6789
BUFFER_SIZE = 1024

# Creating the UDP socket
sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Setting the timeout to 1 second
sender_socket.settimeout(1)

# Probability of a packet being lost or corrupted
p_loss = 0.1
p_corrupt = 0.1

# Sequence number of the next packet to send
next_seq_num = 0

# Last acknowledgement received
last_ack_received = -1

# The maximum number of times we can retransmit before giving up
max_retransmits = 5

# The current number of times we have retransmitted the current packet
num_retransmits = 0

# The current packet being sent
current_packet = None

# The timer for the current packet
current_packet_timer = None


# Function to send the packet
def send_packet(packet):
    global current_packet, current_packet_timer

    # Add the checksum
    checksum = calculate_checksum(packet)
    packet_with_checksum = packet + checksum.to_bytes(2, byteorder="big")

    # Simulate packet loss
    if random.random() < p_loss:
        print("Packet lost: seq_num=" + str(get_seq_num(packet)))
        return

    # Simulate packet corruption
    if random.random() < p_corrupt:
        print("Packet corrupted: seq_num=" + str(get_seq_num(packet)))
        sender_socket.sendto(packet_with_checksum[:-1] + b"\x00", (UDP_IP_ADDRESS, UDP_PORT_NO))
    else:
        sender_socket.sendto(packet_with_checksum, (UDP_IP_ADDRESS, UDP_PORT_NO))

    # Start the timer
    current_packet = packet
    current_packet_timer = time.time()


# Function to calculate the checksum
def calculate_checksum(packet):
    checksum = 0

    for i in range(0, len(packet), 2):
        if i + 1 < len(packet):
            word = (packet[i] << 8) + packet[i + 1]
            checksum += word
        else:
            word = packet[i]
            checksum += word

    checksum = (checksum >> 16) + (checksum & 0xffff)
    checksum = checksum + (checksum >> 16)

    return ~checksum & 0xffff


# Function to get the sequence number of the packet
def get_seq_num(packet):
    return int.from_bytes(packet[:4], byteorder="big")


# Function to create a packet with the given sequence number and data
def make_packet(seq_num, data):
    packet = seq_num.to_bytes(4, byteorder="big") + data
    return packet


# Main function to send the data
def rdt_send(data):
    global next_seq_num, last_ack_received, num_retransmits

    while True:
        # If all packets have been acknowledged, we are done
        if last_ack_received == len(data) - 1:
            break

        # If we have not sent the maximum number of retransmits for the current packet,
        # and the timer for the current packet has not expired, do nothing
        if num_retransmits < max_retransmits and current_packet is not None \
                and time.time() - current_packet_timer < 0.5:
            continue

        # If we have sent the maximum number of retransmits for the current packet,
        # or the timer for the current packet has expired, resend the packet
        if num_re == MAX_RETRANSMITS or time.time() - start_time >= TIMEOUT:
            num_re = 0 # Reset the number of retransmits
        start_time = time.time() # Reset the start time for the timer
        print(f"Packet {seq_num} timed out. Resending...")