import os
from Crypto.PublicKey import RSA

def generate_key_pair():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

def save_keys(private_key, public_key):
    # Tentukan folder untuk penyimpanan
    server_folder = "server"
    client_folder = "client"

    # Buat folder jika belum ada
    os.makedirs(server_folder, exist_ok=True)
    os.makedirs(client_folder, exist_ok=True)

    # Simpan private key di folder server
    private_key_path = os.path.join(server_folder, "private.pem")
    with open(private_key_path, "wb") as priv_file:
        priv_file.write(private_key)

    # Simpan public key di folder server dan client
    public_key_server_path = os.path.join(server_folder, "public.pem")
    public_key_client_path = os.path.join(client_folder, "public.pem")
    with open(public_key_server_path, "wb") as pub_file:
        pub_file.write(public_key)
    with open(public_key_client_path, "wb") as pub_file:
        pub_file.write(public_key)

    print(f"Private key saved to {private_key_path}")
    print(f"Public key saved to {public_key_server_path} and {public_key_client_path}")

if __name__ == "__main__":
    priv_key, pub_key = generate_key_pair()
    save_keys(priv_key, pub_key)
    print("Public and private keys generated and saved.")
