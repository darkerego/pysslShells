import socket
import ssl
import sys
from sys import exit

def socket_create():
    try:
        global host
        global port
        global ssls
        host = '127.0.0.1'
        port = 5600
        s = socket.socket()
        ssls = wrappedSocket = ssl.wrap_socket(s, ssl_version=ssl.PROTOCOL_TLSv1)
    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Connect to a remote socket
def socket_connect():
    try:
        global host
        global port
        ssls.connect((host, port))
    except socket.error as msg:
        print("Socket connection error: " + str(msg))


def send_commands(conn):
    while True:
        try:
            cmd = input()
            if cmd == 'quit':
                conn.send(str.encode('quit'))
                conn.close()
                ssls.close()
                sys.exit()
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(4096).decode())
                print(client_response, end="")
        except KeyboardInterrupt:
            conn.send(str.encode('quit'))
            conn.close()

def main():
    socket_create()
    socket_connect()
    send_commands(ssls)


main()
