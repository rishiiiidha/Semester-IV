import socket
from Crypto.Cipher import AES
import os

def pad(data):
    return data + b' ' * (16 - len(data) % 16)

def main():
    key = os.urandom(16)
    cipher = AES.new(key, AES.MODE_ECB)
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 4000))
    server_socket.listen(1)
    print('Server is listening...')
    
    client_socket, address = server_socket.accept()
    print(f"Client {address} connected")
    
    client_socket.send(key)
    
    encrypted_msg = client_socket.recv(1024)
    decrypted_msg = cipher.decrypt(encrypted_msg).strip().decode()
    print("Received:", decrypted_msg)
    
    ack = "Message received"
    client_socket.send(cipher.encrypt(pad(ack.encode())))
    
    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    main()
