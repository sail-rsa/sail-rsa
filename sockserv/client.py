from client_server_base import ClientServerBase
import socket, threading, pickle, random
from packet import Packet
from packet import PacketType
from user_data import UserData

import sys
sys.path.append('../python')
import rsa_soln

class Client(ClientServerBase):
    def __init__(self, socket, e, d, n, host_addr, username):
        super().__init__(socket)
        self.messages = ['test']
        self.user_list = {}
        self.e = e
        self.d = d
        self.n = n
        self.host_addr = host_addr
        self.username = username

    def send_initial_connect_message(self, _):
        self.send_packet(
            (self.host_addr, 8000),
            Packet(
                PacketType.CLIENT_JOIN,
                UserData(self.username, (self.e, self.n)),
                self.p2p_addr
            )
        )

    def send_message(self, message, username):
        if username in self.user_list:
            e = self.user_list[username][0]
            n = self.user_list[username][1]
            print('first')
            cyphertext = rsa_soln.encrypt('_____' + message, e, n)
            print('sending message!')
            self.send_packet(
                (self.host_addr, 8000),
                Packet(
                    PacketType.CLIENT_SEND_MESSAGE,
                    cyphertext,
                    self.p2p_addr
                )
            )

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
            self.messages = packet.data
            for i in range(len(self.messages)):
                message = self.messages[i]
                self.messages[i] = str(rsa_soln.decrypt(message, self.d, self.n))
        elif packet.type == PacketType.SERVER_BROADCAST_USER_LIST:
            self.user_list = {}
            for user_data in packet.data:
                print('{} {}'.format(user_data.username, user_data.pub_key))
                self.user_list[user_data.username] = user_data.pub_key
