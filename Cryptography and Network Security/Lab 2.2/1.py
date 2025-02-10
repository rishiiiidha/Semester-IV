from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

KEY_LENGTH = 32  
BLOCK_SIZE = AES.block_size  

def encrypt_data(data, key):
    cipher = AES.new(key, AES.MODE_CBC)  
    iv = cipher.iv  
    encrypted_bytes = cipher.encrypt(pad(data.encode(), BLOCK_SIZE))
    return iv + encrypted_bytes  

def decrypt_data(encrypted_data, key):
    iv = encrypted_data[:BLOCK_SIZE]  
    encrypted_bytes = encrypted_data[BLOCK_SIZE:]  
    cipher = AES.new(key, AES.MODE_CBC, iv)  
    decrypted_bytes = unpad(cipher.decrypt(encrypted_bytes), BLOCK_SIZE)
    return decrypted_bytes.decode()  

key = get_random_bytes(KEY_LENGTH)  
text = "Confidential Message!"

encrypted_message = encrypt_data(text, key)
decrypted_message = decrypt_data(encrypted_message, key)

print("Original:", text)
print("Encrypted:", encrypted_message)
print("Decrypted:", decrypted_message)