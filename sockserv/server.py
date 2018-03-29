from client_server_base import ClientServerBase
import socket, threading, pickle
from message import Message
from message import MessageType
from user_data import UserData
import time

class Server(ClientServerBase):
    def __init__(self, socket):
        self.clients_to_check = []
        self.clients = []
        self.client_to_data = {}
        self.client_data = []
        self.username_to_client = {}
        super().__init__(socket)

    def process_message(self, message):
        if message.type == MessageType.CLIENT_JOIN:
            client = message.reply_addr
            client_data = message.data
            self.username_to_client[client_data.username] = client
            self.clients.append(client)
            self.client_data.append(client_data)
            self.client_to_data[client] = client_data
            for client in self.clients:
                threading.Thread(
                        target = self.send_message,
                        args = (client, Message(MessageType.SERVER_BROADCAST_USER_LIST, self.client_data, self.p2p_addr))
                ).start()
        elif message.type == MessageType.CLIENT_RESP_ONLINE:
            self.clients_to_check.remove(message.reply_addr)
        elif message.type == MessageType.CLIENT_SEND_MESSAGE:
            for client in self.clients:
                threading.Thread(
                        target = self.send_message,
                        args = (client, Message(MessageType.SERVER_BROADCAST_MESSAGE, message.data, self.p2p_addr))
                ).start()

    def client_check_loop(self, _):
        while True:
            time.sleep(5)
            update = False
            for client in self.clients_to_check:
                if client in self.peer_sockets:
                    del self.peer_sockets[client]
                self.clients.remove(client)
                self.client_data.remove(self.client_to_data[client])
                del self.client_to_data[client]
                update = True

            if update:
                for client in self.clients:
                    threading.Thread(
                            target = self.send_message,
                            args = (client, Message(MessageType.SERVER_BROADCAST_USER_LIST, self.client_data, self.p2p_addr))
                    ).start()

            self.clients_to_check = []
            print('Connected:')
            for client in self.clients:
                print('{}: {}'.format(client, self.client_to_data[client]))
                self.clients_to_check.append(client)
                threading.Thread(
                        target = self.send_message,
                        args = (client, Message(MessageType.SERVER_CHECK_ONLINE, '', self.p2p_addr))
                ).start()
            print()

server = Server(5000)
threading.Thread(
        target = server.start_listening,
        args = (None,)
).start()
threading.Thread(
        target = server.client_check_loop,
        args = (None,)
).start()
