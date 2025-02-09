from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

KEY_SIZE = 32  
BLOCK_SIZE = AES.block_size  

def encrypt_text(plain_text, key):
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv 
    ciphertext = cipher.encrypt(pad(plain_text.encode(), BLOCK_SIZE))
    return iv + ciphertext  

def decrypt_text(cipher_text, key):
    iv = cipher_text[:BLOCK_SIZE] 
    ciphertext = cipher_text[BLOCK_SIZE:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plain_text = unpad(cipher.decrypt(ciphertext), BLOCK_SIZE)
    return plain_text.decode()
key = get_random_bytes(KEY_SIZE)  
plain_text = "Hello, my name is Rishidha!"

encrypted_text = encrypt_text(plain_text, key)
decrypted_text = decrypt_text(encrypted_text, key)

print("Original Text:", plain_text)
print("Encrypted Text:", encrypted_text)
print("Decrypted Text:", decrypted_text)
