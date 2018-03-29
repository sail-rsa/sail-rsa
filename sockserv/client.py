from client_server_base import ClientServerBase
import socket, threading, pickle, random
from message import Message
from message import MessageType
from user_data import UserData

class Client(ClientServerBase):
    def process_message(self, message):
        if message.type == MessageType.SERVER_CHECK_ONLINE:
            threading.Thread(
                    target = self.send_message,
                    args = (message.reply_addr, Message(MessageType.CLIENT_RESP_ONLINE, '', self.p2p_addr))
            ).start()
        elif message.type == MessageType.SERVER_BROADCAST_MESSAGE:
            print(message.data)
        elif message.type == MessageType.SERVER_BROADCAST_USER_LIST:
            print(message.data)

client = Client(random.randint(5000, 8000))
threading.Thread(
        target = client.start_listening,
        args = (None,)
).start()
threading.Thread(
        target = client.send_message,
        args = (('localhost', 5000), Message(MessageType.CLIENT_JOIN, UserData('User{}'.format(random.randint(1, 100)), random.randint(1000, 5000)), client.p2p_addr))
).start()

while True:
    message = input('')
    threading.Thread(
            target = client.send_message,
            args = (('localhost', 5000), Message(MessageType.CLIENT_SEND_MESSAGE, message, client.p2p_addr))
    ).start()
