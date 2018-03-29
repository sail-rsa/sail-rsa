import socket, threading, pickle
from message import Message
from message import MessageType

class ClientServerBase:
    def __init__(self, socket):
        self.p2p_addr = ('', socket)
        self.peer_sockets = {}
        self.p2p_socket = None

    def process_message(self, message):
        pass

    def start_listening(self, _):
        self.p2p_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.p2p_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.p2p_socket.bind(self.p2p_addr)
        self.p2p_socket.listen(5)

        while True:
            conn_socket, addr = self.p2p_socket.accept()
            message = conn_socket.recv(4096)
            try:
                message = pickle.loads(message)
                self.process_message(message)
            except pickle.UnpicklingError:
                pass

        self.p2p_socket.close

    def send_message(self, peer_addr, data):
        """Sends a message with provided data to a given address, opening a new
        p2p socket if neccesary"""
        try:
            if not peer_addr in self.peer_sockets or True:
                peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                peer_socket.connect(peer_addr)
                self.peer_sockets[peer_addr] = peer_socket
            else:
                peer_socket = self.peer_sockets[peer_addr]
                peer_socket.connect(peer_addr)
            peer_socket.send(pickle.dumps(data))
        except ConnectionRefusedError:
            pass
