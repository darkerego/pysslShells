#from __future__ import print_function
import socket
import sys
import ssl
cmd = ""
#from openssl import *
#from __future__ import print_function

#context = ssl.context(SSL.SSLv23_METHOD)
#context.use_privatekey_file('ssl.key')
#context.use_certificate_file('ssl.cert')
# Create socket (allows two computers to connect)
def socket_create():
    try:
        global host
        global port
        global s
        host = ''
        port = 9999
        s = socket.socket()
        s = ssl.wrap_socket(s, certfile='../ssl/server.crt', keyfile='../ssl/server.key', ssl_version=ssl.PROTOCOL_TLSv1)
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
        try:
            cmd = input()
            if cmd == 'quit':
                conn.send(str.encode('quit'))
                conn.close()
                s.close()
                sys.exit()
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(1024).decode())
                print(client_response, end="")
        except KeyboardInterrupt:
            conn.send(str.encode('quit'))
            conn.close()



def main():
    socket_create()
    socket_bind()
    socket_accept()


main()
