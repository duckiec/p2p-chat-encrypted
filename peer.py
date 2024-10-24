# peer.py
import socket
import threading

class Peer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start_server(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)
        print(f"Listening on {self.host}:{self.port}")
        conn, addr = self.sock.accept()
        print(f"Connected by {addr}")
        threading.Thread(target=self.receive_messages, args=(conn,)).start()
        return conn

    def connect_to_peer(self, peer_host, peer_port):
        self.sock.connect((peer_host, peer_port))
        threading.Thread(target=self.receive_messages, args=(self.sock,)).start()
        return self.sock

    def send_message(self, conn, message):
        conn.sendall(message)

    def receive_messages(self, conn):
        while True:
            try:
                data = conn.recv(4096)
                if data:
                    print("\nReceived:", data.decode())
                else:
                    break
            except ConnectionResetError:
                break

    def close_connection(self):
        self.sock.close()
