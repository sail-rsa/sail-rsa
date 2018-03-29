from enum import Enum

class PacketType(Enum):
    CLIENT_JOIN = 0
    SERVER_CHECK_ONLINE = 1
    CLIENT_RESP_ONLINE = 2
    CLIENT_SEND_MESSAGE = 3
    SERVER_BROADCAST_MESSAGE = 4
    SERVER_BROADCAST_USER_LIST = 5

class Packet:
    def __init__(self, packet_type, packet_data, reply_addr):
        self.type = packet_type
        self.data = packet_data
        self.reply_addr = reply_addr
