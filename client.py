import socket
import sys
import os
import pty
import serial

# set up the virtual serial port
master, slave = pty.openpty()
s_name = os.ttyname(slave)
ser = serial.Serial(s_name)
print(s_name)


while True:

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('192.168.8.102', 10000)
    print(f'connecting to {server_address[0]} port {server_address[1]}')
    sock.connect(server_address)

    user_message = input("Enter a message to send\n")

    ser.write(user_message.encode('utf-8'))

    try:

        # Send data
        message = os.read(master, 1000)
        print(f'sending "{message}"')
        sock.sendall(message)

        # Look for the response
        amount_received = 0
        amount_expected = len(message)

        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received += len(data)
            print(f'received "{data}"')

    finally:
        print('closing socket')
        sock.close()
