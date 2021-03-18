# this server listens for a connection from a client
# to access namespace of caller

import socket
import subprocess
import argparse
import logging
import pickle


# parser = argparse.ArgumentParser(description='Script so useful.')
# parser.add_argument("--ta", type=str, default="127.0.0.1")
# parser.add_argument("--tp", type=int, default=5002)
#
# args = parser.parse_args()
#
# tcp_address = args.ta
# tcp_port = args.tp
#
# # Create a TCP/IP socket
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("Unpickle connection")
filehandler = open("connection.p", "rb")
connection = pickle.load(filehandler)
filehandler.close()

# # Bind the socket to the port
# reply_address = (tcp_address, tcp_port)
# print(f'Trying to reply to {reply_address[0]} port {reply_address[1]}')
# print(f'From ', sock)
# sock.connect(reply_address)

# Try to send something
try:
    print("Sending something")
    connection.send("abc".encode())
except Exception as e:
    print('closing socket because of error')
    logging.error("Error: ", exc_info=e)
    connection.close()

print("Connection ended")
