from client_server_base import ClientServerBase
import socket, threading, pickle
from packet import Packet
from packet import PacketType
from user_data import UserData
import time

MAX_SERVER_CONNECTIONS = 25

class Server(ClientServerBase):
    def __init__(self, socket):
        super().__init__(socket)
        self.clients_to_check = []
        self.clients = {}
        self.username_to_client_data = {}
        self.max_num_connections = MAX_SERVER_CONNECTIONS

    def broadcast_user_list(self):
        """
        Broadcasts a list of active users to all clients
        """
        user_list = [self.clients[addr] for addr in self.clients]
        for client in self.clients:
            threading.Thread(
                    target = self.send_packet,
                    args = (client, Packet(PacketType.SERVER_BROADCAST_USER_LIST, user_list, self.p2p_addr))
            ).start()

    def broadcast_message(self, message):
        """
        Broadcasts a chat message to all clients
        """
        for client in self.clients:
            threading.Thread(
                    target = self.send_packet,
                    args = (client, Packet(PacketType.SERVER_BROADCAST_MESSAGE, message, self.p2p_addr))
            ).start()

    def process_packet(self, packet):
        """
        Handles a packet recieved by the server from a client.
        """
        # Client first connects with server
        if packet.type == PacketType.CLIENT_JOIN:
            client_addr = packet.reply_addr
            client_data = packet.data
            self.username_to_client_data[client_data.username] = client_data
            self.clients[client_addr] = client_data
            self.broadcast_user_list();

        # Client confirms that they are still connected
        elif packet.type == PacketType.CLIENT_RESP_ONLINE:
            if packet.reply_addr in self.clients_to_check:
                self.clients_to_check.remove(packet.reply_addr)

        # Client sends a chat message
        elif packet.type == PacketType.CLIENT_SEND_MESSAGE:
            print(packet.data)
            self.broadcast_message(packet.data)

    def purge_clients(self):
        ret = len(self.clients_to_check) > 0
        for client_addr in self.clients_to_check:
            if client_addr in self.peer_sockets:
                del self.peer_sockets[client_addr]
            del self.username_to_client_data[self.clients[client_addr].username]
            del self.clients[client_addr]
        return ret

    def client_check_loop(self, _):
        """
        Queries each connected client periodically to check if they are still
        connected. Should be run on its own thread.
        """
        while True:
            # Delay between each check. Client gets this many seconds to respond.
            time.sleep(5)
            if self.purge_clients():
                self.broadcast_user_list();

            self.clients_to_check = []
            print('Connected:')
            for client_addr in self.clients:
                print('{}: {}'.format(client_addr, self.clients[client_addr].username))
                self.clients_to_check.append(client_addr)
                threading.Thread(
                        target = self.send_packet,
                        args = (client_addr, Packet(PacketType.SERVER_CHECK_ONLINE, '', self.p2p_addr))
                ).start()
            print()

server = Server(8000)
threading.Thread(
        target = server.start_listening,
        args = (None,)
).start()
threading.Thread(
        target = server.client_check_loop,
        args = (None,)
).start()
