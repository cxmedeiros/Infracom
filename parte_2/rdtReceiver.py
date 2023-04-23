import socket

IP_ADDRESS = "127.0.0.1"
PORT_NO = 6789
BUFFER_SIZE = 1024

def __check_pkt(seq_num, expected_seq_num):
    return seq_num == expected_seq_num

def __nott(seq_num):
    return '0' if seq_num  == '1' else '1'

def rdtReceiving(socket, addr, seq_num, expected_seq_num):
    print("Entered rdtReceiving function\n")
    print("Expected seq_num: ", expected_seq_num, "\n")

    while True:        
        if not __check_pkt(seq_num, expected_seq_num):
            ack = __nott(seq_num).encode()
            print(f"Duplicate detected, resending ack {ack.decode()}!\n\n")
            socket.sendto(ack, addr)

            msg, _ = socket.recvfrom(BUFFER_SIZE)
            seq_num, _ = msg.decode().split(',')

        else:
            ack = seq_num.encode()
            print(f"Package is correct, sending ack {ack.decode()}!\n\n")
            socket.sendto(ack, addr)
            
            expected_seq_num = __nott(expected_seq_num)
            return expected_seq_num

