from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend

def perform_key_exchange():
    # Generate private keys for both parties
    alice_private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
    bob_private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())

    # Get public keys
    alice_public_key = alice_private_key.public_key()
    bob_public_key = bob_private_key.public_key()

    # Perform key exchange
    alice_shared_key = alice_private_key.exchange(ec.ECDH(), bob_public_key)
    bob_shared_key = bob_private_key.exchange(ec.ECDH(), alice_public_key)

    # Print results
    print("Alice's Shared Key:", alice_shared_key.hex())
    print("Bob's Shared Key:", bob_shared_key.hex())

    # Verify keys match
    if alice_shared_key == bob_shared_key:
        print("\nKey exchange successful! Both parties have the same shared key.")
    else:
        print("\nKey exchange failed! Keys do not match.")

if __name__ == "__main__":
    print("Performing ECC Key Exchange...")
    perform_key_exchange() 