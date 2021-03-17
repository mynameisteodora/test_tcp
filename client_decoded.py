import socket
import sys
import logging
import os
import pty

# set up the virtual serial port
# master, slave = pty.openpty()
# s_name = os.ttyname(slave)
# ser = serial.Serial(s_name)
# print(s_name)

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ("35.246.27.70", 5002)
print(f'connecting to {server_address[0]} port {server_address[1]}')
sock.connect(server_address)

user_message = ""

while True and user_message != "Bye":

    user_message = input("Enter a message to send\n")

    # ser.write(user_message.encode('utf-8'))

    try:

        # Send data
        # message = os.read(master, 1000)
        print(f'sending "{user_message}"')
        sock.sendall(user_message.encode('utf-8'))

        data = sock.recv(1000)
        print(f'received "{data}"')

        if data.decode('utf-8').strip() == 'Bye':
            print("Received bye from server, closing connection")
            sock.close()
            break

    except Exception as e:
        print('closing socket because of error')
        logging.error("Error: ", exc_info=e)
        sock.close()
        break

print("Conversation ended.")
