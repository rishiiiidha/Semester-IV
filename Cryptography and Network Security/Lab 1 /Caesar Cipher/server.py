import socket

def decrypt(msg, shift=1):
    decrypted_data = ""
    for char in msg.lower():
        if char.isalpha():
            shifted = (ord(char) - ord('a') - shift) % 26
            decrypted_data += chr(shifted + ord('a'))
        else:
            decrypted_data += char
    return decrypted_data

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