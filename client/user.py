import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from des.DES import DES
from des.utils import pad_string
import os
import threading
 
IP = "127.0.0.1"
PORT = 65432
DES_KEY = "12345678"  

def encrypt_des_key(public_key_path, des_key):
    """Encrypt DES key using RSA public key."""
    script_dir = os.path.dirname(__file__)
    public_key_path = os.path.join(script_dir, public_key_path)

    with open(public_key_path, "rb") as pub_file:
        public_key = RSA.import_key(pub_file.read())
        cipher_rsa = PKCS1_OAEP.new(public_key)
        encrypted_key = cipher_rsa.encrypt(des_key.encode())
    return encrypted_key

def receive_messages(sock):
    """Listen for messages from the server and print them."""
    while True:
        try:
            message = sock.recv(1024).decode()
            if message:
                print("\033[K", end="")  # \033[F: gerak ke baris sebelumnya, \033[K: hapus baris
                print("\r" + message)  # Cetak pesan baru
                print("You: ", end="", flush=True)
            else:
                break
        except:
            print("Connection closed by server.")
            break

def main():
    username = input("Enter your username: ")
    des_instance = DES(int(DES_KEY))

    encrypted_des_key = encrypt_des_key("public.pem", DES_KEY)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((IP, PORT))

        # Send username to the server
        s.sendall(username.encode())

        # Waiting for confirmation from server
        confirmation = s.recv(1024).decode()  
        if confirmation != "OK":
            print("Error: Server failed to acknowledge username.")
            return

        s.sendall(encrypted_des_key)

        print("Connected to the server.")
        # Start a thread to receive messages
        threading.Thread(target=receive_messages, args=(s,), daemon=True).start()

        while True:
            message = input("You: ")
            padded_message = pad_string(message)
            encrypted_chunks = [
                des_instance.encrypt(padded_message[i:i+64]) for i in range(0, len(padded_message), 64)
            ]
            encrypted_message = ''.join(encrypted_chunks)
            s.sendall(encrypted_message.encode())
            # print("Encrypted message sent:", encrypted_message)

if __name__ == "__main__":
    main()