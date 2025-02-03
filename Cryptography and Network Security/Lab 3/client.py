import socket
from Crypto.Cipher import AES

def pad(data):
    return data + b' ' * (16 - len(data) % 16)

def main():
    client_socket = socket.socket()
    client_socket.connect(("localhost", 4000))
    print("Connected to server successfully!")
    
    key = client_socket.recv(16)
    cipher = AES.new(key, AES.MODE_ECB)
    print("Encryption established")
    
    message = input("Enter message to send: ")
    encrypted_message = cipher.encrypt(pad(message.encode()))
    print("Encrypted Message :", encrypted_message)
    client_socket.send(encrypted_message)
    
    encrypted_response = client_socket.recv(1024)
    decrypted_response = cipher.decrypt(encrypted_response).strip().decode()
    print("Server response:", decrypted_response)
    
    client_socket.close()

if __name__ == "__main__":
    main()
