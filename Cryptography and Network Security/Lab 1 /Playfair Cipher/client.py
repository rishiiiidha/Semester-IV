import socket
from threading import *

class client(Thread):
    def __init__(self, socket, address):
        Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.start()

    def encryption(self, data):
        key = "monarchy"
        matrix = []
        used_chars = set()
        for c in key.lower():
            if c not in used_chars and c != 'j':
                matrix.append(c)
                used_chars.add(c)
        for c in "abcdefghiklmnopqrstuvwxyz":
            if c not in used_chars:
                matrix.append(c)
                used_chars.add(c)
        matrix = [matrix[i:i + 5] for i in range(0, 25, 5)]
        def find_position(char):
            for i in range(5):
                for j in range(5):
                    if matrix[i][j] == char:
                        return i, j
            return None
        def playfair_encrypt_pair(pair):
            r1, c1 = find_position(pair[0])
            r2, c2 = find_position(pair[1])
            if r1 == r2:  
                return matrix[r1][(c1 + 1) % 5] + matrix[r2][(c2 + 1) % 5]
            elif c1 == c2: 
                return matrix[(r1 + 1) % 5][c1] + matrix[(r2 + 1) % 5][c2]
            else: 
                return matrix[r1][c2] + matrix[r2][c1]
        data = data.lower().replace('j', 'i')
        if len(data) % 2 != 0:
            data += 'x'
        encrypted_data = ""
        for i in range(0, len(data), 2):
            encrypted_data += playfair_encrypt_pair(data[i:i+2])
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