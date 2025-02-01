import socket

def decrypt(msg):
    key = "monarchy"
    matrix = []
    used = set()
    
    for c in key.lower():
        if c not in used and c != 'j':
            matrix.append(c)
            used.add(c)
    
    for c in "abcdefghiklmnopqrstuvwxyz":
        if c not in used:
            matrix.append(c)
            used.add(c)
    
    matrix = [matrix[i:i + 5] for i in range(0, 25, 5)]

    def find_pos(char):
        for i in range(5):
            for j in range(5):
                if matrix[i][j] == char:
                    return i, j
        return None

    def decrypt_pair(pair):
        r1, c1 = find_pos(pair[0])
        r2, c2 = find_pos(pair[1])
        if r1 == r2:
            return matrix[r1][(c1 - 1) % 5] + matrix[r2][(c2 - 1) % 5]
        elif c1 == c2:
            return matrix[(r1 - 1) % 5][c1] + matrix[(r2 - 1) % 5][c2]
        else:
            return matrix[r1][c2] + matrix[r2][c1]

    result = ""
    for i in range(0, len(msg), 2):
        result += decrypt_pair(msg[i:i+2])
    
    if result.endswith('x'):
        result = result[:-1]
        
    return result

s = socket.socket()
s.connect(("localhost", 3000))
print("Connected successfully!")

while True:
    try:
        enc_msg = s.recv(1024).decode()
        if not enc_msg:
            break
            
        dec_msg = decrypt(enc_msg)
        print("\nReceived encrypted message:", enc_msg)
        print("Decrypted message:", dec_msg)
        ack = f"Message received and decrypted successfully\n"
        s.send(ack.encode())
    except:
        break

s.close()