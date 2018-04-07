from client_server_base import ClientServerBase
import socket, threading, pickle, random
from packet import Packet
from packet import PacketType
from user_data import UserData

import subprocess
import math

import sys
sys.path.append('../python')
import rsa_soln

class Client(ClientServerBase):
    def __init__(self, socket, e, d, n, host_addr, username, using_java):
        super().__init__(socket)
        self.messages = []
        self.user_list = {}
        self.e = e
        self.d = d
        self.n = n
        self.host_addr = host_addr
        self.username = username
        self.using_java = using_java
        self.last_msg_rec = -1

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
        message = message[:300]
        if username in self.user_list:
            e = self.user_list[username][0]
            n = self.user_list[username][1]

            max_msg_size = math.floor(math.log2(n) / 8)

            message_left = '_____' + message
            ciphertexts = []
            while len(message_left) > max_msg_size:
                if self.using_java:
                    result = subprocess.Popen(['java', '-cp', '.', 'sail/Encrypt', message_left[:max_msg_size], str(e), str(n)], stdout = subprocess.PIPE, cwd = '../java/src/')
                    result.wait()
                    for line in result.stdout:
                        line = line.decode('utf-8')
                        ciphertext = line
                else:
                    ciphertext = rsa_soln.encrypt(message_left[:max_msg_size], e, n)
                ciphertexts.append(ciphertext)
                message_left = message_left[max_msg_size:]

            if self.using_java:
                result = subprocess.Popen(['java', '-cp', '.', 'sail/Encrypt', message_left, str(e), str(n)], stdout = subprocess.PIPE, cwd = '../java/src/')
                result.wait()
                for line in result.stdout:
                    line = line.decode('utf-8')
                    ciphertext = line
            else:
                ciphertext = rsa_soln.encrypt(message_left, e, n)
            ciphertexts.append(ciphertext)

            self.send_packet(
                (self.host_addr, 8000),
                Packet(
                    PacketType.CLIENT_SEND_MESSAGE,
                    ciphertexts,
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

            for i in range(len(packet.data)):
                message_data = packet.data[i]
                if message_data[1] <= self.last_msg_rec:
                    continue;
                self.last_msg_rec = message_data[1]
                ciphertexts = message_data[2]
                message = ''
                for portion in ciphertexts:
                    if self.using_java:
                        result = subprocess.Popen(['java', '-cp', '.', 'sail/Decrypt', portion.strip(), str(self.d), str(self.n)], stdout = subprocess.PIPE, cwd = '../java/src/')
                        result.wait()
                        for line in result.stdout:
                            line = line.decode('utf-8')
                            solved = line
                    else:
                        solved = rsa_soln.decrypt(portion, self.d, self.n)
                    message += solved
                self.messages.append((message_data[0], str(message)))
        elif packet.type == PacketType.SERVER_BROADCAST_USER_LIST:
            self.user_list = {}
            for user_data in packet.data:
                self.user_list[user_data.username] = user_data.pub_key
