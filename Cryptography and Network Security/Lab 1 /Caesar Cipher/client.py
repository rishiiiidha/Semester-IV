import socket
from threading import *

class client(Thread):
    def __init__(self, socket, address):
        Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.start()

    def encryption(self, data, shift=1):
        encrypted_data = ""
        for char in data.lower():
            if char.isalpha():
                shifted = (ord(char) - ord('a') + shift) % 26
                encrypted_data += chr(shifted + ord('a'))
            else:
                encrypted_data += char
        return encrypted_data

    def run(self):
        while True:
            try:
                r = input("Send data: ")
                t = self.encryption(r)
                self.sock.send(t.encode())
                response = self.sock.recv(1024).decode()
                print(response)
            except Exception as e:
                print(f"Error: {e}")
                break

def main():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(("localhost", 3000))
    serversocket.listen(5)
    print('Sender ready and is listening')
    
    while True:
        clientsocket, address = serversocket.accept()
        print("Receiver " + str(address) + " connected")
        client(clientsocket, address)

if __name__ == "__main__":
    main()