import socket
import subprocess
import argparse

parser = argparse.ArgumentParser(description='Script so useful.')
parser.add_argument("--file", type=str, default="~/Downloads/app_update.zip")
parser.add_argument("--port", type=str, default="/dev/ttys001")
parser.add_argument("--baud_rate", type=int, default=9600)

args = parser.parse_args()

zip_update = args.file
port = args.port
baud_rate = args.baud_rate

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('', 5003)
print(f'starting up on {server_address[0]} port {server_address[1]}')
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

print("local socket = ", sock)

class Slip:
    SLIP_BYTE_END             = 0o300
    SLIP_BYTE_ESC             = 0o333
    SLIP_BYTE_ESC_END         = 0o334
    SLIP_BYTE_ESC_ESC         = 0o335

    SLIP_STATE_DECODING                 = 1
    SLIP_STATE_ESC_RECEIVED             = 2
    SLIP_STATE_CLEARING_INVALID_PACKET  = 3

    @staticmethod
    def encode(data):
        newData = []
        for elem in data:
            if elem == Slip.SLIP_BYTE_END:
                newData.append(Slip.SLIP_BYTE_ESC)
                newData.append(Slip.SLIP_BYTE_ESC_END)
            elif elem == Slip.SLIP_BYTE_ESC:
                newData.append(Slip.SLIP_BYTE_ESC)
                newData.append(Slip.SLIP_BYTE_ESC_ESC)
            else:
                newData.append(elem)
        newData.append(Slip.SLIP_BYTE_END)
        return newData

    @staticmethod
    def decode_add_byte(c, decoded_data, current_state):
        finished = False
        if current_state == Slip.SLIP_STATE_DECODING:
            if c == Slip.SLIP_BYTE_END:
                finished = True
            elif c == Slip.SLIP_BYTE_ESC:
                current_state = Slip.SLIP_STATE_ESC_RECEIVED
            else:
                decoded_data.append(c)
        elif current_state == Slip.SLIP_STATE_ESC_RECEIVED:
            if c == Slip.SLIP_BYTE_ESC_END:
                decoded_data.append(Slip.SLIP_BYTE_END)
                current_state = Slip.SLIP_STATE_DECODING
            elif c == Slip.SLIP_BYTE_ESC_ESC:
                decoded_data.append(Slip.SLIP_BYTE_ESC)
                current_state = Slip.SLIP_STATE_DECODING
            else:
                current_state = Slip.SLIP_STATE_CLEARING_INVALID_PACKET
        elif current_state == Slip.SLIP_STATE_CLEARING_INVALID_PACKET:
            if c == Slip.SLIP_BYTE_END:
                current_state = Slip.SLIP_STATE_DECODING
                decoded_data = []

        return (finished, current_state, decoded_data)

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()

    try:
        print('connection from', client_address)
        print('connection = ', connection)
        print('type = ', type(connection))

        # Receive the data in small chunks and retransmit it
        while True:
            print('Waiting for message...')
            data = connection.recv(50000)
            print('received "%s"' % data) # this should be any data from airspeck and we need to receive it in one batch (messageLength = 117?)
            if data:
                print('Sending ping components back:')
                resp = [0x60, 0x09, 0x0B]
                encoded = Slip.encode(resp)
                print("sending encoded data: ", encoded)
                print("of type", type(encoded))
                connection.send(bytearray(Slip.encode(resp)))
            else:
                print('no more data from', client_address)
                break

    finally:
        # Clean up the connection
        connection.close()
