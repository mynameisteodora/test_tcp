import socket
import logging

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ("35.246.27.70", 5002)
print(f'connecting to {server_address[0]} port {server_address[1]}')
sock.connect(server_address)

user_message = ""

while True:
    try:
        # sock.send("Something".encode())
        data = sock.recv(50000)
        print("Received data = ", data)


    except Exception as e:
        print('closing socket because of error')
        logging.error("Error: ", exc_info=e)
        sock.close()

print("Conversation ended.")
