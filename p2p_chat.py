# p2p_chat.py
import threading

from peer import Peer
from rsa_utils import generate_keys, encrypt_message, save_key_to_file, load_key_from_file


def chat_interface(peer, connection, private_key, public_key_peer):
    while True:
        message = input("\nYou: ")
        encrypted_message = encrypt_message(message, public_key_peer)
        peer.send_message(connection, encrypted_message)

def main():
    # Generate or load RSA keys
    private_key, public_key = generate_keys()
    save_key_to_file(private_key, "private_key.pem", is_private=True)
    save_key_to_file(public_key, "public_key.pem", is_private=False)

    # Peer Setup
    host = input("Enter your host IP (e.g., 127.0.0.1): ")
    port = int(input("Enter your port (e.g., 5000): "))
    peer = Peer(host, port)

    # Choose to be a server or client
    choice = input("Do you want to (1) start a server or (2) connect to a peer? (1/2): ")
    if choice == '1':
        connection = peer.start_server()
    elif choice == '2':
        peer_host = input("Enter the peer's IP address: ")
        peer_port = int(input("Enter the peer's port: "))
        connection = peer.connect_to_peer(peer_host, peer_port)
    else:
        print("Invalid choice")
        return

    # Exchange public keys with the peer
    public_key_peer_pem = connection.recv(4096)
    public_key_peer = load_key_from_file(public_key_peer_pem, is_private=False)
    connection.sendall(open("public_key.pem", "rb").read())

    # Start chatting
    threading.Thread(target=chat_interface, args=(peer, connection, private_key, public_key_peer)).start()

    # Handle incoming encrypted messages
    peer.receive_messages(connection)

if __name__ == "__main__":
    main()
