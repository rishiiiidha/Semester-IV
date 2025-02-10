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

def encrypt_and_send(filename, client_socket):
    with open(filename, "rb") as f:
        plaintext = f.read()
    encrypted_data = rc4_crypt(plaintext, KEY)
    print(f"Encrypted {filename}")
    client_socket.sendall(len(encrypted_data).to_bytes(4, "big"))
    client_socket.sendall(encrypted_data)
    print("File sent successfully!")

def main():
    client_socket = socket.socket()
    client_socket.connect(("localhost", 4000))  
    print("Connected to server successfully!")
    
    filename = "input.txt"  
    encrypt_and_send(filename, client_socket)
    
    client_socket.close()

if __name__ == "__main__":
    main()
