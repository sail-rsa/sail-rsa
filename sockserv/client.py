from client_server_base import ClientServerBase
import socket, threading, pickle, random
from packet import Packet
from packet import PacketType
from user_data import UserData
import subprocess

import sys
sys.path.append('../python')
import rsa_soln

class Client(ClientServerBase):
    def __init__(self, socket, e, d, n, host_addr, username, using_java):
        super().__init__(socket)
        self.messages = ['test']
        self.user_list = {}
        self.e = e
        self.d = d
        self.n = n
        self.host_addr = host_addr
        self.username = username
        self.using_java = using_java

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
            cyphertext = ''
            if self.using_java:
                result = subprocess.Popen(['java', '-cp', '.', 'sail/Encrypt', '_____' + message, str(e), str(n)], stdout = subprocess.PIPE, cwd = '../java/src/')
                for line in result.stdout:
                    line = line.decode('utf-8')
                    cyphertext = line
            else:
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
            decrypted_message = ''
            if self.using_java:
                print(packet.data)
                result = subprocess.Popen(['java', '-cp', '.', 'sail/Decrypt', packet.data.strip(), str(self.d), str(self.n)], stdout = subprocess.PIPE, cwd = '../java/src/')
                for line in result.stdout:
                    line = line.decode('utf-8')
                    decrypted_message = line
            else:
                decrypted_message = rsa_soln.decrypt(packet.data, self.d, self.n)
            self.messages.append(decrypted_message)
        elif packet.type == PacketType.SERVER_BROADCAST_USER_LIST:
            self.user_list = {}
            for user_data in packet.data:
                print('{} {}'.format(user_data.username, user_data.pub_key))
                self.user_list[user_data.username] = user_data.pub_key
