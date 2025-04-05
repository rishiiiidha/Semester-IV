import socket
import hashlib
import random
import base64
from Crypto.Cipher import AES  # type: ignore
from Crypto.Util.Padding import pad, unpad  # type: ignore

def dh_keys():
    prime, base = 23, 5
    private = random.randint(1, prime - 1)
    public = pow(base, private, prime)
    return private, public, prime, base

def shared_key(private, public, prime):
    return hashlib.sha512(str(pow(public, private, prime)).encode()).digest()[:32]

def hash_text(text):
    return hashlib.sha512(text.encode()).digest()

def encrypt(text, key):
    cipher = AES.new(key, AES.MODE_CBC)
    data = text.encode() + b"***" + hash_text(text)
    encrypted = cipher.encrypt(pad(data, AES.block_size))
    return base64.b64encode(cipher.iv + encrypted).decode()

def decrypt(enc_text, key):
    raw_data = base64.b64decode(enc_text)
    iv, cipher_text = raw_data[:16], raw_data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(cipher_text), AES.block_size)
    text, received_hash = decrypted.split(b"***")
    return text.decode(), hash_text(text.decode()) == received_hash

def main():
    priv, pub, prime, base = dh_keys()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 4000))
    server.listen(1)
    print("Server listening on port 4000...")

    client, addr = server.accept()
    print(f"Client {addr} connected")

    client.send(f"{pub},{prime},{base}".encode())
    client_pub = int(client.recv(1024).decode())
    print(f"Client public key: {client_pub}")

    key = shared_key(priv, client_pub, prime)
    print("Shared key established")

    enc_text = client.recv(1024).decode()
    dec_text, integrity = decrypt(enc_text, key)

    print("\nReceived Message:")
    print(f"Content: {dec_text}")
    print(f"Integrity: {'Yes' if integrity else 'No'}")

    response = "Message received with integrity verification"
    client.send(encrypt(response, key).encode())

    client.close()
    server.close()

if __name__ == "__main__":
    main()