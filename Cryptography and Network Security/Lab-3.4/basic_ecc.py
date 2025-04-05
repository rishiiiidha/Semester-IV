def mod_inverse(a, m):
    """Calculate modular multiplicative inverse of a modulo m"""
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    gcd, x, y = extended_gcd(a, m)
    if gcd != 1:
        raise Exception('Modular inverse does not exist')
    return x % m

class Point:
    def __init__(self, x, y, curve):
        self.x = x
        self.y = y
        self.curve = curve
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __add__(self, other):
        if self.x == 0 and self.y == 0:
            return other
        if other.x == 0 and other.y == 0:
            return self
        if self.x == other.x and self.y != other.y:
            return Point(0, 0, self.curve)
        
        if self.x == other.x:
            # Point doubling
            slope = (3 * self.x * self.x + self.curve.a) * mod_inverse(2 * self.y, self.curve.p)
        else:
            # Point addition
            slope = (other.y - self.y) * mod_inverse(other.x - self.x, self.curve.p)
        
        x3 = (slope * slope - self.x - other.x) % self.curve.p
        y3 = (slope * (self.x - x3) - self.y) % self.curve.p
        
        return Point(x3, y3, self.curve)
    
    def __mul__(self, k):
        result = Point(0, 0, self.curve)
        temp = Point(self.x, self.y, self.curve)
        
        while k:
            if k & 1:
                result = result + temp
            temp = temp + temp
            k >>= 1
        return result

class Curve:
    def __init__(self, p, a, b, gx, gy, n):
        self.p = p  # Prime modulus
        self.a = a  # Curve parameter a
        self.b = b  # Curve parameter b
        self.g = Point(gx, gy, self)  # Generator point
        self.n = n  # Order of generator point

def perform_key_exchange():
    # Define a simple curve: y² = x³ + 2x + 3 over F_17
    curve = Curve(
        p=17,  # Prime modulus
        a=2,   # Curve parameter a
        b=3,   # Curve parameter b
        gx=1,  # Generator point x
        gy=6,  # Generator point y
        n=19   # Order of generator point
    )
    
    # Generate private keys (small numbers for demonstration)
    alice_private_key = 5
    bob_private_key = 7
    
    # Generate public keys
    alice_public_key = curve.g * alice_private_key
    bob_public_key = curve.g * bob_private_key
    
    # Perform key exchange
    alice_shared_key = bob_public_key * alice_private_key
    bob_shared_key = alice_public_key * bob_private_key
    
    # Print results
    print("Curve: y² = x³ + 2x + 3 over F_17")
    print("\nAlice's Private Key:", alice_private_key)
    print("Bob's Private Key:", bob_private_key)
    print("\nAlice's Public Key Point:", (alice_public_key.x, alice_public_key.y))
    print("Bob's Public Key Point:", (bob_public_key.x, bob_public_key.y))
    print("\nAlice's Shared Key Point:", (alice_shared_key.x, alice_shared_key.y))
    print("Bob's Shared Key Point:", (bob_shared_key.x, bob_shared_key.y))
    
    # Verify keys match
    if alice_shared_key == bob_shared_key:
        print("\nKey exchange successful! Both parties have the same shared key point.")
    else:
        print("\nKey exchange failed! Keys do not match.")

if __name__ == "__main__":
    print("Performing Basic ECC Key Exchange...")
    perform_key_exchange() 