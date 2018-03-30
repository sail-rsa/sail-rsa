from client_server_base import ClientServerBase
import socket, threading, pickle, random
from packet import Packet
from packet import PacketType
from user_data import UserData

class Client(ClientServerBase):
    def __init__(self, socket):
        super().__init__(socket)
        self.messages = []
        self.user_list = []

    def process_packet(self, packet):
        """
        Handles a packet recieved by this client from the server.
        """
        if packet.type == PacketType.SERVER_CHECK_ONLINE:
            threading.Thread(
                    target = self.send_packet,
                    args = (packet.reply_addr, Packet(PacketType.CLIENT_RESP_ONLINE, '', self.p2p_addr))
            ).start()
        elif packet.type == PacketType.SERVER_BROADCAST_MESSAGE:
            self.messages.append(packet.data)
        elif packet.type == PacketType.SERVER_BROADCAST_USER_LIST:
            self.user_list = packet.data

client = Client(random.randint(5000, 8000))
threading.Thread(
        target = client.start_listening,
        args = (None,)
).start()
threading.Thread(
        target = client.send_packet,
        args = (('localhost', 5000), Packet(PacketType.CLIENT_JOIN, UserData('User{}'.format(random.randint(1, 100)), random.randint(1000, 5000)), client.p2p_addr))
).start()

while True:
    message = input('')
    if message == 'users':
        print([user.username for user in client.user_list])
    '''threading.Thread(
            target = client.send_packet,
            args = (('localhost', 5000), Packet(PacketType.CLIENT_SEND_MESSAGE, message, client.p2p_addr))
    ).start()'''
