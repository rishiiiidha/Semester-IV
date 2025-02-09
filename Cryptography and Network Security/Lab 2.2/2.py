from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

KEY_SIZE = 32  
BLOCK_SIZE = AES.block_size 

def encrypt_file(input_file, output_file, key):
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv  
    
    with open(input_file, 'rb') as f:
        plaintext = f.read()
    
    ciphertext = cipher.encrypt(pad(plaintext, BLOCK_SIZE))
    
    with open(output_file, 'wb') as f:
        f.write(iv + ciphertext) 
    
    print("Encryption complete. Encrypted file saved as:", output_file)

def decrypt_file(input_file, output_file, key):
    with open(input_file, 'rb') as f:
        iv = f.read(BLOCK_SIZE)
        ciphertext = f.read()
    
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), BLOCK_SIZE)
    
    with open(output_file, 'wb') as f:
        f.write(plaintext)
    
    print("Decryption complete. Decrypted file saved as:", output_file)

key = get_random_bytes(KEY_SIZE)

plaintext_file = "input.txt"
encrypted_file = "encrypted.aes"
decrypted_file = "decrypted.txt"

encrypt_file(plaintext_file, encrypted_file, key)
decrypt_file(encrypted_file, decrypted_file, key)
