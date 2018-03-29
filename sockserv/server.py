from client_server_base import ClientServerBase
import socket, threading, pickle
from packet import Packet
from packet import PacketType
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

    def process_packet(self, packet):
        """
        Handles a packet recieved by the server from a client.
        """
        if packet.type == PacketType.CLIENT_JOIN:
            client = packet.reply_addr
            client_data = packet.data
            self.username_to_client[client_data.username] = client
            self.clients.append(client)
            self.client_data.append(client_data)
            self.client_to_data[client] = client_data
            for client in self.clients:
                threading.Thread(
                        target = self.send_packet,
                        args = (client, Packet(PacketType.SERVER_BROADCAST_USER_LIST, self.client_data, self.p2p_addr))
                ).start()
        elif packet.type == PacketType.CLIENT_RESP_ONLINE:
            self.clients_to_check.remove(packet.reply_addr)
        elif packet.type == PacketType.CLIENT_SEND_MESSAGE:
            for client in self.clients:
                threading.Thread(
                        target = self.send_packet,
                        args = (client, Packet(PacketType.SERVER_BROADCAST_MESSAGE, packet.data, self.p2p_addr))
                ).start()

    def client_check_loop(self, _):
        """
        Queries each connected client periodically to check if they are still
        connected. Should be run on its own thread.
        """
        while True:
            # Delay between each check. Client gets this many seconds to respond.
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
                            target = self.send_packet,
                            args = (client, Packet(PacketType.SERVER_BROADCAST_USER_LIST, self.client_data, self.p2p_addr))
                    ).start()

            self.clients_to_check = []
            print('Connected:')
            for client in self.clients:
                print('{}: {}'.format(client, self.client_to_data[client]))
                self.clients_to_check.append(client)
                threading.Thread(
                        target = self.send_packet,
                        args = (client, Packet(PacketType.SERVER_CHECK_ONLINE, '', self.p2p_addr))
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
