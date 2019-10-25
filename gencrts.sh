#!/bin/sh
# Generate keys for ssl socket
test -d ssl|| mkdir ssl >/dev/null 2>&1

openssl genrsa -des3 -out ssl/server.orig.key 2048
openssl rsa -in ssl/server.orig.key -out ssl/server.key
openssl req -new -key ssl/server.key -out ssl/server.csr
openssl x509 -req -days 365 -in ssl/server.csr -signkey ssl/server.key -out ssl/server.crt

exit
