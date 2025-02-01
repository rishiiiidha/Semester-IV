from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad

def des_encrypt(plain_text, key):
    if len(key) != 8:
        raise ValueError("Key must be 8 bytes long")
    plain_bytes = plain_text.encode('utf-8')
    padded_text = pad(plain_bytes, DES.block_size)
    cipher = DES.new(key.encode('utf-8'), DES.MODE_ECB)
    encrypted_bytes = cipher.encrypt(padded_text)
    return encrypted_bytes.hex()

def des_decrypt(encrypted_text, key):
    if len(key) != 8:
        raise ValueError("Key must be 8 bytes long")
    
    encrypted_bytes = bytes.fromhex(encrypted_text)
    
    cipher = DES.new(key.encode('utf-8'), DES.MODE_ECB)
    
    decrypted_padded = cipher.decrypt(encrypted_bytes)
    
    return unpad(decrypted_padded, DES.block_size).decode('utf-8')

def encrypt_file(input_file, output_file, key):
    with open(input_file, 'r') as f:
        plain_text = f.read()
    encrypted_text = des_encrypt(plain_text, key)
    with open(output_file, 'w') as f:
        f.write(encrypted_text)

def decrypt_file(input_file, output_file, key):
    with open(input_file, 'r') as f:
        encrypted_text = f.read()
    decrypted_text = des_decrypt(encrypted_text, key)
    with open(output_file, 'w') as f:
        f.write(decrypted_text)

plain_text = input("Enter plaintext (max 8 characters recommended): ")
key = input("Enter 8-character key: ")

if len(key) != 8:
    print("Error: Key must be exactly 8 characters long.")
else:
    encrypted_text = des_encrypt(plain_text, key)
    print("Encrypted:", encrypted_text)

    decrypted_text = des_decrypt(encrypted_text, key)
    print("Decrypted:", decrypted_text)

    # Encrypt and decrypt a file
    input_file = input("Enter the path of the file to encrypt: ")
    encrypted_file = input("Enter the path to save the encrypted file: ")
    decrypt_output_file = input("Enter the path to save the decrypted file: ")

    encrypt_file(input_file, encrypted_file, key)
    print(f"File encrypted and saved to {encrypted_file}")

    decrypt_file(encrypted_file, decrypt_output_file, key)
    print(f"File decrypted and saved to {decrypt_output_file}")