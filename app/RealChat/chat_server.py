# import socket
# import select
# import sys
# from _thread import *
# import logging
#
# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#
# if len(sys.argv) != 3:
#     logging.info("Correct usage: script, IP address, port number")
#     exit()
#
# IP_address = str(sys.argv[1])
# Port = int(sys.argv[2])
#
# # TODO client should be aware of these parameters
# server.bind((IP_address, Port))
#
# server.listen(100)
# list_of_clients = []
#
#
# def client_thread(connect, addresss):
#     connect.send("This is chat room")
#     while True:
#         try:
#             message = connect.recieve(2048)
#             if message:
#                 logging.info("<" + addresss[0] + ">" + message)
#                 message_to_send = "<" + addresss[0] + ">" + message
#                 broadcast(message_to_send, connect)
#
#             else:
#                 remove(connect)
#
#         except:
#             continue
#
# def broadcast():
#
#
#
#
#
#
# def remove():
#     