import socket
import subprocess
import argparse

parser = argparse.ArgumentParser(description='Script so useful.')
parser.add_argument("--file", type=str, default="app_update.zip")
parser.add_argument("--port", type=str)
parser.add_argument("--baud_rate", type=int, default=9600)

args = parser.parse_args()

zip_update = args.file
port = args.port
baud_rate = args.baud_rate

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('', 5002)
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
            data = connection.recv(50000)
            print('received "%s"' % data) # this should be any data from airspeck and we need to receive it in one batch (messageLength = 117?)
            if data:
                reply = input('Send nrf components back:')
                subprocess.run((f"nrfutil dfu serial -pkg {zip_update} -p {port} -b {baud_rate} -fc 0").split())
                # connection.sendall(reply.encode('utf-8'))
            else:
                print('no more data from', client_address)
                break

    finally:
        # Clean up the connection
        connection.close()
