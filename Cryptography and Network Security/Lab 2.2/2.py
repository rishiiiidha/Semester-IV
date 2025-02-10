from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

KEY_LENGTH = 32  
BLOCK_SIZE = AES.block_size  

def encrypt_file(source_file, encrypted_file, key):
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv  

    with open(source_file, 'rb') as file:
        file_data = file.read()
    
    encrypted_data = cipher.encrypt(pad(file_data, BLOCK_SIZE))
    
    with open(encrypted_file, 'wb') as file:
        file.write(iv + encrypted_data)  
    
    print(f"File encrypted successfully: {encrypted_file}")

def decrypt_file(encrypted_file, output_file, key):
    with open(encrypted_file, 'rb') as file:
        iv = file.read(BLOCK_SIZE)
        encrypted_data = file.read()
    
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), BLOCK_SIZE)
    
    with open(output_file, 'wb') as file:
        file.write(decrypted_data)
    
    print(f"File decrypted successfully: {output_file}")

key = get_random_bytes(KEY_LENGTH)

original_file = "input.txt"
encrypted_output = "secured_data.aes"
decrypted_output = "output.txt"

encrypt_file(original_file, encrypted_output, key)
decrypt_file(encrypted_output, decrypted_output, key)