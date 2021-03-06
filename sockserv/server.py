from client_server_base import ClientServerBase
import socket, threading, pickle
from packet import Packet
from packet import PacketType
from user_data import UserData
import time

MAX_SERVER_CONNECTIONS = 35

class Server(ClientServerBase):
    def __init__(self, socket):
        super().__init__(socket)
        self.time_since_response = {}
        self.clients = {}
        self.message_history = []
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

    def broadcast_messages(self):
        """
        Broadcasts a chat message to all clients
        """
        for client in self.clients:
            threading.Thread(
                    target = self.send_packet,
                    args = (client, Packet(PacketType.SERVER_BROADCAST_MESSAGE, self.message_history[-5:], self.p2p_addr))
            ).start()

    def process_packet(self, packet):
        """
        Handles a packet recieved by the server from a client.
        """
        # Client first connects with server
        if packet.type == PacketType.CLIENT_JOIN:
            client_addr = packet.reply_addr
            client_data = packet.data
            self.clients[client_addr] = client_data
            self.time_since_response[client_addr] = 0
            self.broadcast_user_list();

        # Client confirms that they are still connected
        elif packet.type == PacketType.CLIENT_RESP_ONLINE:
            if packet.reply_addr in self.time_since_response:
                if self.time_since_response[packet.reply_addr] > 1:
                    threading.Thread(
                            target = self.send_packet,
                            args = (packet.reply_addr, Packet(PacketType.SERVER_BROADCAST_MESSAGE, self.message_history[-5:], self.p2p_addr))
                    ).start()
                self.time_since_response[packet.reply_addr] = 0

        # Client sends a chat message
        elif packet.type == PacketType.CLIENT_SEND_MESSAGE:
            self.message_history.append((self.clients[packet.reply_addr].username, len(self.message_history), packet.data))
            self.broadcast_messages()

    def purge_clients(self):
        to_delete = []
        for client_addr in self.time_since_response:
            if self.time_since_response[client_addr] > 5:
                if client_addr in self.peer_sockets:
                    del self.peer_sockets[client_addr]
                del self.clients[client_addr]
                to_delete.append(client_addr)
                removed_one = True
        for client_addr in to_delete:
            del self.time_since_response[client_addr]
        return len(to_delete) > 0

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


            print('Connected:')
            for client_addr in self.clients:
                self.time_since_response[client_addr] += 1
                print('{}: {}'.format(client_addr, self.clients[client_addr].username))
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
