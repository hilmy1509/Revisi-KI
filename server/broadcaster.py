import socket
import threading
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from des.DES import DES
from des.utils import bin_to_text
import os

IP = "127.0.0.1"
PORT = 65432

clients = []
DES_KEY = None 

def broadcast(message, sender_conn):
    """Send a message to all connected clients except the sender."""
    for client in clients:
        if client != sender_conn:
            try:
                client.sendall(message.encode())
            except Exception as e:
                print(f"Error broadcasting to a client: {e}")
                clients.remove(client)

def handle_client(conn, addr):
    global DES_KEY
    print(f"Client {addr} connected.")

    # Receive username
    username = conn.recv(1024).decode()
    if conn not in clients:
        clients.append(conn)
    print(f"Received username: {username} {len(clients)}")

    conn.sendall("OK".encode())
    print("Username acknowledged, waiting for DES key.")

    encrypted_key = conn.recv(256)  

    script_dir = os.path.dirname(__file__)
    public_key_path = os.path.join(script_dir, "private.pem")

    with open(public_key_path, "rb") as priv_file:
        private_key = RSA.import_key(priv_file.read())
        cipher_rsa = PKCS1_OAEP.new(private_key)
        DES_KEY = cipher_rsa.decrypt(encrypted_key)
    print(f"Received DES key {username}: {DES_KEY.decode()}")

    des_instance = DES(int(DES_KEY.decode()))
    while True:
        try:
            encrypted_message = conn.recv(1024).decode()
            if not encrypted_message:
                break
            print(f"Encrypted message from {username}: {encrypted_message}")

            # Decrypt message
            decrypted_chunks = [
                des_instance.decrypt(encrypted_message[i:i+64]) for i in range(0, len(encrypted_message), 64)
            ]
            decrypted_binary = ''.join(decrypted_chunks)
            decrypted_message = bin_to_text(decrypted_binary)
            print(f"Message from {addr}: {decrypted_message}")

            # Broadcast decrypted message to all clients
            broadcast(f"{username}: {decrypted_message}", conn)
        except ConnectionResetError:
            break

    print(f"Client {username} disconnected.")
    clients.remove(conn)
    conn.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((IP, PORT))
        s.listen()
        print("Server listening for connections...")

        while True:
            conn, addr = s.accept()
            clients.append(conn)
            threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    main()