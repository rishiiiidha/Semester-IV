import socket
from Crypto.Cipher import ARC4 # type: ignore

KEY = b"rishidhakey" 
def rc4_decrypt(data, key):
    cipher = ARC4.new(key)
    return cipher.decrypt(data)

def encryptionAndDecryption(conn):
    encrypted_data = conn.recv(4096)  
    with open("encrypt.rc4", "wb") as f:
        f.write(encrypted_data)
    print("Received and saved encrypted file!")

    decrypted_data = rc4_decrypt(encrypted_data, KEY)
    with open("decrypt.txt", "wb") as f:
        f.write(decrypted_data)
    print("File decrypted and saved as 'decrypt.txt'")

def main():
    server_socket = socket.socket()
    server_socket.bind(("localhost", 4000))
    server_socket.listen(1)
    print("Server is listening on port 4000...")
    conn, addr = server_socket.accept()
    print(f"Connection established with {addr}")
    encryptionAndDecryption(conn)
    conn.close()

if __name__ == "__main__":
    main()
