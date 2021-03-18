# this server listens for a connection from a client
import socket
import subprocess
import pickle
import nordicsemi
from nordicsemi.dfu.dfu_transport_tcp import DfuTransportTCP
from nordicsemi.dfu.dfu_transport_serial import DfuTransportSerial
from nordicsemi.lister.device_lister import DeviceLister
from pc_ble_driver_py.exceptions import NordicSemiException
from nordicsemi.dfu.dfu import Dfu
from nordicsemi.dfu.dfu_transport import DfuEvent, TRANSPORT_LOGGING_LEVEL
import click

import logging

global_bar = None


def update_progress(progress=0):
    if global_bar:
        global_bar.update(progress)


def do_tcp(package, port, tcp_conn, connect_delay=None, flow_control=None, packet_receipt_notification=None, baud_rate=None,
           serial_number=None, ping=None, timeout=None):

    # if type(package) == str:
    #     package = click.Path(package)

    if flow_control is None:
        flow_control = DfuTransportSerial.DEFAULT_FLOW_CONTROL
    if packet_receipt_notification is None:
        packet_receipt_notification = DfuTransportSerial.DEFAULT_PRN
    if baud_rate is None:
        baud_rate = DfuTransportSerial.DEFAULT_BAUD_RATE
    if ping is None:
        ping = False
    if port is None:
        device_lister = DeviceLister()
        device = device_lister.get_device(serial_number=serial_number)
        if device is None:
            raise NordicSemiException("A device with serial number %s is not connected." % serial_number)
        port = device.get_first_available_com_port()
        logger.info("Resolved serial number {} to port {}".format(serial_number, port))

    if timeout is None:
        timeout = DfuTransportSerial.DEFAULT_TIMEOUT

    logger.info("Using board at serial port: {}".format(port))
    serial_backend = DfuTransportTCP(tcp_conn=tcp_conn, com_port=str(port), baud_rate=baud_rate,
                                     flow_control=flow_control, prn=packet_receipt_notification, do_ping=ping,
                                     timeout=timeout)

    serial_backend.register_events_callback(DfuEvent.PROGRESS_EVENT, update_progress)
    dfu = Dfu(zip_file_path=package, dfu_transport=serial_backend, connect_delay=connect_delay)

    if logger.getEffectiveLevel() > logging.INFO:
        with click.progressbar(length=dfu.dfu_get_total_size()) as bar:
            global global_bar
            global_bar = bar
            dfu.dfu_send_images()
    else:
        dfu.dfu_send_images()

    print("Device programmed.")


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
        print('connection = ', connection)
        print('type = ', type(connection))

        # this is starting the nrfutil code
        logger = logging.getLogger(__name__)
        log_level = TRANSPORT_LOGGING_LEVEL
        logging.basicConfig(format='%(asctime)s %(message)s', level=log_level)
        print("calling tcp")
        do_tcp(package="app_dfu_package.zip", port='/dev/tts001', tcp_conn=connection)
        # import pc_nrfutil.nordicsemi.__main__

        # # Once the connection is made to the client, try to invoke code
        # # from the other script
        # while True:
        #     print('Sending message from server_doer')
        #     subprocess.run((f"python server_doer.py --ta {client_address[0]} --tp {client_address[1]}").split())

    finally:
        # Clean up the connection
        connection.close()
