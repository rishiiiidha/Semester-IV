import socket

KEY = b"rishidhakey" 

def rc4_init(key):
    S = list(range(256))
    j = 0
    key_length = len(key)
    
    for i in range(256):
        j = (j + S[i] + key[i % key_length]) % 256
        S[i], S[j] = S[j], S[i]  
    
    return S

def rc4_crypt(data, key):
    S = rc4_init(key)
    i = j = 0
    output = bytearray()
    
    for byte in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i] 
        
        keystream_byte = S[(S[i] + S[j]) % 256]
        output.append(byte ^ keystream_byte)
    
    return bytes(output)

def receive_and_decrypt(conn):
    data_length = int.from_bytes(conn.recv(4), "big")

    encrypted_data = conn.recv(data_length)

    with open("encrypted.rc4", "wb") as f:
        f.write(encrypted_data)

    print("Received and saved encrypted file as 'encrypted.rc4'")

    decrypted_data = rc4_crypt(encrypted_data, KEY)

    with open("decrypted.txt", "wb") as f:
        f.write(decrypted_data)

    print("File decrypted and saved as 'decrypted.txt'")

def main():
    server_socket = socket.socket()
    server_socket.bind(("localhost", 4000))
    server_socket.listen(1)
    print("Server is listening on port 4000...")

    conn, addr = server_socket.accept()
    print(f"Connection established with {addr}")

    receive_and_decrypt(conn)
    
    conn.close()

if __name__ == "__main__":
    main()
