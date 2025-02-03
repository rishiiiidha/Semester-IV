# client.py
import socket
from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
import base64

def pad(text):
    padding_length = 8 - (len(text) % 8)
    return text + chr(padding_length) * padding_length

def unpad(text):
    padding_length = ord(text[-1])
    return text[:-padding_length]

class DESClient:
    def __init__(self, host='localhost', port=8000):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        self.key = get_random_bytes(8)
        self.socket.sendall(self.key)  
        print("Connected to server and key exchanged")

    def encrypt_message(self, message):
        cipher = DES.new(self.key, DES.MODE_ECB)
        padded_text = pad(message)
        encrypted_text = cipher.encrypt(padded_text.encode('utf-8'))
        return base64.b64encode(encrypted_text).decode('utf-8')

    def decrypt_message(self, encrypted_message):
        cipher = DES.new(self.key, DES.MODE_ECB)
        decrypted_text = cipher.decrypt(base64.b64decode(encrypted_message))
        return unpad(decrypted_text.decode('utf-8'))

    def send_message(self):
        try:
            while True:
                message = input("Enter message: ")
                if message.lower() == 'quit':
                    break

                print(f"Original Message: {message}")
                encrypted_message = self.encrypt_message(message)
                print(f"Encrypted Message: {encrypted_message}")
                self.socket.sendall(encrypted_message.encode('utf-8'))

                response = self.socket.recv(1024).decode('utf-8')
                print(f"Received Encrypted Response: {response}")
                decrypted_response = self.decrypt_message(response)
                print(f"Decrypted Response: {decrypted_response}")

        finally:
            self.socket.close()

if __name__ == "__main__":
    client = DESClient()
    client.send_message()