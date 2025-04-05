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
    secret = pow(public, private, prime)
    return hashlib.sha512(str(secret).encode()).digest()[:32]

def hash_text(text):
    return hashlib.sha512(text.encode()).digest()

def encrypt(text, key):
    cipher = AES.new(key, AES.MODE_CBC)
    text_hash = hash_text(text)
    data = text.encode() + b"***" + text_hash
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
    client = socket.socket()
    client.connect(("localhost", 4000))
    print("Connected to server!")

    priv, pub, prime, base = dh_keys()
    print(f"Client public key: {pub}")

    server_pub, prime, base = map(int, client.recv(1024).decode().split(','))
    print(f"Server public key: {server_pub}")

    client.send(str(pub).encode())
    key = shared_key(priv, server_pub, prime)
    print("Shared key established")

    text = input("Enter message: ")
    enc_text = encrypt(text, key)
    print(f"Encrypted: {enc_text}")

    client.send(enc_text.encode())
    enc_response = client.recv(1024).decode()
    dec_response, integrity = decrypt(enc_response, key)

    print("\nResults:")
    print(f"Decrypted: {dec_response}")
    print(f"Integrity: {'Yes' if integrity else 'No'}")
    client.close()

if __name__ == "__main__":
    main()