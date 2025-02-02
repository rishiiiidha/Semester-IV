import socket
from Crypto.Cipher import DES3
import base64

def pad(text):
    # Use PKCS7 padding
    padding_length = 8 - (len(text) % 8)
    return text + chr(padding_length) * padding_length

def unpad(text):
    # Remove PKCS7 padding
    padding_length = ord(text[-1])
    return text[:-padding_length]

class TripleDESServer:
    def __init__(self, host='localhost', port=8000):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(1)
        print("Server is listening...")

    def handle_client(self, client_socket):
        # Receive the key from client
        key = client_socket.recv(24)

        def encrypt_message(message):
            cipher = DES3.new(key, DES3.MODE_ECB)
            padded_text = pad(message)
            encrypted_text = cipher.encrypt(padded_text.encode('utf-8'))
            encoded_encrypted_text = base64.b64encode(encrypted_text).decode('utf-8')
            print(f"Encrypted Response (Base64): {encoded_encrypted_text}")  # Debug print
            return encoded_encrypted_text

        def decrypt_message(encrypted_message):
            cipher = DES3.new(key, DES3.MODE_ECB)
            decrypted_text = cipher.decrypt(base64.b64decode(encrypted_message))
            return unpad(decrypted_text.decode('utf-8'))

        try:
            while True:
                # Receive and decrypt message
                encrypted_message = client_socket.recv(1024).decode('utf-8')
                if not encrypted_message:
                    break

                print(f"Received Encrypted Message (Base64): {encrypted_message}")  # Debug print
                decrypted_message = decrypt_message(encrypted_message)
                print(f"Received (decrypted): {decrypted_message}")

                # Send encrypted response
                response = f"Server received: {decrypted_message}"
                encrypted_response = encrypt_message(response)
                client_socket.sendall(encrypted_response.encode('utf-8'))

        finally:
            client_socket.close()

    def start(self):
        try:
            while True:
                client_socket, addr = self.server_socket.accept()
                print(f"Client connected from {addr}")
                self.handle_client(client_socket)
        finally:
            self.server_socket.close()

if __name__ == "__main__":
    server = TripleDESServer()
    server.start()