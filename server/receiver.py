#receiver.py
import socket
import os
import sys
sys.path.append(os.path.abspath('../'))
from des.DES import DES
from des.utils import bin_to_text

IP = "127.0.0.1"
PORT = 65432
DES_KEY = 12345678 

def main():
    des_instance = DES(DES_KEY)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((IP, PORT))
        s.listen()
        print("Waiting for connection...")

        conn, addr = s.accept()
        with conn:
            print("Connected by", addr)
            encrypted_message = conn.recv(4096).decode()
            print("Received encrypted message:", encrypted_message)

            decrypted_chunks = [des_instance.decrypt(encrypted_message[i:i+64]) for i in range(0, len(encrypted_message), 64)]
            decrypted_binary = ''.join(decrypted_chunks)
            decrypted_message = bin_to_text(decrypted_binary)  
            print("Decrypted message:", decrypted_message)

if __name__ == "__main__":
    main()