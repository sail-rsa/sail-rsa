from enum import Enum

class MessageType(Enum):
    CLIENT_JOIN = 0
    SERVER_CHECK_ONLINE = 1
    CLIENT_RESP_ONLINE = 2
    CLIENT_SEND_MESSAGE = 3
    SERVER_BROADCAST_MESSAGE = 4
    SERVER_BROADCAST_USER_LIST = 5

class Message:
    def __init__(self, message_type, message_data, reply_addr):
        self.type = message_type
        self.data = message_data
        self.reply_addr = reply_addr
