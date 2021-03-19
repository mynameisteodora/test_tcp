import socket
import logging

for i in range(10):
    print("Try", (i+1))
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    # server_address = ("35.246.27.70", 5002)
    server_address = ("127.0.0.1", 5002)
    print(f'connecting to {server_address[0]} port {server_address[1]}')
    sock.connect(server_address)

    user_message = ""


    try:
        sock.send("Something".encode())
        data = sock.recv(1000)
        print("Received data = ", data)


    except Exception as e:
        print('closing socket because of error')
        logging.error("Error: ", exc_info=e)
        sock.close()

    finally:
        sock.close()

print("Conversation ended.")
