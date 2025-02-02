import socket
from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
import base64

def pad(text):
    # Use PKCS7 padding
    padding_length = 8 - (len(text) % 8)
    return text + chr(padding_length) * padding_length

def unpad(text):
    # Remove PKCS7 padding
    padding_length = ord(text[-1])
    return text[:-padding_length]

class TripleDESClient:
    def __init__(self, host='localhost', port=8000):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        # Generate a random 24-byte key for Triple DES
        self.key = DES3.adjust_key_parity(get_random_bytes(24))
        # Send the key securely
        self.socket.sendall(self.key)
        print("Connected to server and key exchanged")

    def encrypt_message(self, message):
        cipher = DES3.new(self.key, DES3.MODE_ECB)
        padded_text = pad(message)
        encrypted_text = cipher.encrypt(padded_text.encode('utf-8'))
        encoded_encrypted_text = base64.b64encode(encrypted_text).decode('utf-8')
        print(f"Encrypted Message (Base64): {encoded_encrypted_text}")  # Debug print
        return encoded_encrypted_text

    def decrypt_message(self, encrypted_message):
        cipher = DES3.new(self.key, DES3.MODE_ECB)
        decrypted_text = cipher.decrypt(base64.b64decode(encrypted_message))
        return unpad(decrypted_text.decode('utf-8'))

    def send_message(self):
        try:
            while True:
                message = input("Enter message: ")
                if message.lower() == 'quit':
                    break

                # Encrypt and send
                encrypted_message = self.encrypt_message(message)
                self.socket.sendall(encrypted_message.encode('utf-8'))

                # Receive and decrypt response
                response = self.socket.recv(1024).decode('utf-8')
                print(f"Received Encrypted Response (Base64): {response}")  # Debug print
                decrypted_response = self.decrypt_message(response)
                print(f"Server response (decrypted): {decrypted_response}")

        finally:
            self.socket.close()

if __name__ == "__main__":
    client = TripleDESClient()
    client.send_message()