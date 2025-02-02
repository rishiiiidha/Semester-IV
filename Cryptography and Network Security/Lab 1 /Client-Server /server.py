import socket

s = socket.socket()
s.connect(("localhost", 4000))
print("Connected successfully!")

while True:
    try:
        msg = s.recv(1024).decode()
        if not msg:
            break
       
        print("\nReceived message:", msg)
        ack = f"Message received successfully\n"
        s.send(ack.encode())
    except:
        break

s.close()