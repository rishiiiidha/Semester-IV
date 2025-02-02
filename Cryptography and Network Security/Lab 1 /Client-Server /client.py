import socket
from threading import *

class client(Thread):
    def __init__(self, socket, address):
        Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.start()
    def run(self):
        while True:
            try:
                r = input("Send data: ")
                self.sock.send(r.encode())
                response = self.sock.recv(1024).decode()
                print(response)
            except Exception as e:
                print(f"Error: {e}")
                break

def main():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(("localhost", 4000))
    serversocket.listen(5)
    print('Sender ready and is listening')
    
    while True:
        clientsocket, address = serversocket.accept()
        print("Receiver " + str(address) + " connected")
        client(clientsocket, address)

if __name__ == "__main__":
    main()