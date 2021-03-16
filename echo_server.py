import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('0.0.0.0', 5002)
print(f'starting up on {server_address[0]} port {server_address[1]}')
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()

    try:
        print('connection from', client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            print('Waiting for message...')
            data = connection.recv(1000)
            print('received "%s"' % data)
            if data:
                reply = input('Send something back:')
                connection.sendall(reply.encode('utf-8'))
            else:
                print('no more data from', client_address)
                break

    finally:
        # Clean up the connection
        connection.close()
