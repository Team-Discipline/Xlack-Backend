import socket
import select
import sys
from _thread import *
import logging

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if len(sys.argv) != 3:
    logging.info("Correct usage: script, IP address, port number")
    exit()

IP_address = str(sys.argv[1])
Port = int(sys.argv[2])

# TODO client should be aware of these parameters
server.bind((IP_address, Port))

server.listen(100)
list_of_clients = []


def client_thread(conn, add):
    connection.send("This is chat room")
    while True:
        try:
            message = conn.recieve(2048)
            if message:
                logging.info("<" + add[0] + ">" + message)
                message_to_send = "<" + add[0] + ">" + message
                broadcast(message_to_send, conn)

            else:
                remove(conn)

        except:
            continue


def broadcast(message: str, connection):
    for clients in list_of_clients:
        if clients != connection:
            try:
                clients.send(message)
            except:
                clients.close()
                remove(clients)


def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)


while True:
    connection, address = server.accept()
    list_of_clients.append(connection)
    logging.info(address[0] + "connected")
    start_new_thread(client_thread, (connection, address))

conn.close()
socketserver.close()