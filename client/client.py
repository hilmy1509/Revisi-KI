import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from des.DES import DES
from des.utils import pad_string

IP = "127.0.0.1"
PORT = 65432
DES_KEY = "12345678"  

def encrypt_des_key(public_key_path, des_key):
    """Encrypt DES key using RSA public key."""
    with open(public_key_path, "rb") as pub_file:
        public_key = RSA.import_key(pub_file.read())
        cipher_rsa = PKCS1_OAEP.new(public_key)
        encrypted_key = cipher_rsa.encrypt(des_key.encode())
    return encrypted_key

def main():
    des_instance = DES(int(DES_KEY))

    encrypted_des_key = encrypt_des_key("public.pem", DES_KEY)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((IP, PORT))
        print("Connected to the server.")

        s.sendall(encrypted_des_key)
        print("Encrypted DES key sent.")

        while True:
            message = input("Enter message to send: ")
            padded_message = pad_string(message)
            encrypted_chunks = [
                des_instance.encrypt(padded_message[i:i+64]) for i in range(0, len(padded_message), 64)
            ]
            encrypted_message = ''.join(encrypted_chunks)
            s.sendall(encrypted_message.encode())
            print("Encrypted message sent:", encrypted_message)

if __name__ == "__main__":
    main()