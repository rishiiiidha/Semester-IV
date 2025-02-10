import socket
from Crypto.Cipher import ARC4 # type: ignore

KEY = b"rishidhakey" 

def rc4_encrypt(data, key):
    cipher = ARC4.new(key)
    return cipher.encrypt(data)

def encryption(filename, client_socket):
    with open(filename, "rb") as f:
        plaintext = f.read()
    encrypted_data = rc4_encrypt(plaintext, KEY)
    print(f"Encrypted {filename}")
    client_socket.sendall(encrypted_data)  

def main():
    client_socket = socket.socket()
    client_socket.connect(("localhost", 4000))
    print("Connected to server successfully!")
    filename = "input.txt"  
    encryption(filename, client_socket)
    print("File sent successfully!")
    client_socket.close()

if __name__ == "__main__":
    main()
