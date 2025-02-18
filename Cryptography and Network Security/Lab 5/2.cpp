#include <iostream>
#include <cmath>

using namespace std;

long long gcd(long long a, long long b)
{
    if (a == 0)
        return b;
    return gcd(b % a, a);
}

long long modInverse(long long e, long long phi)
{
    for (long long d = 2; d < phi; d++)
    {
        if ((e * d) % phi == 1)
            return d;
    }
    return -1; 
}

void generateKeys(long long &e, long long &d, long long &n)
{
    long long p = 61; 
    long long q = 53; 
    n = p * q;
    long long phi = (p - 1) * (q - 1);

    for (e = 2; e < phi; e++)
    {
        if (gcd(e, phi) == 1)
            break;
    }

    d = modInverse(e, phi);
}

long long power(long long base, long long expo, long long mod)
{
    long long res = 1;
    base = base % mod;
    while (expo > 0)
    {
        if (expo & 1)
            res = (res * base) % mod;
        base = (base * base) % mod;
        expo >>= 1;
    }
    return res;
}

long long encrypt(long long m, long long e, long long n)
{
    return power(m, e, n);
}

long long decrypt(long long c, long long d, long long n)
{
    return power(c, d, n);
}

int main()
{
    long long e, d, n;

    
    generateKeys(e, d, n);

    
    cout << "Public Key (e, n): (" << e << ", " << n << ")" << endl;
    cout << "Private Key (d, n): (" << d << ", " << n << ")" << endl;

   
    long long number = 42; 
    long long encNum = encrypt(number, e, n);
    long long decNum = decrypt(encNum, d, n);

    cout << "\nOriginal Number: " << number << endl;
    cout << "Encrypted Number: " << encNum << endl;
    cout << "Decrypted Number: " << decNum << endl;

 
    char letter = 'G';                                      
    long long letterASCII = static_cast<long long>(letter); 
    long long encLetter = encrypt(letterASCII, e, n);
    long long decLetterASCII = decrypt(encLetter, d, n);
    char decLetter = static_cast<char>(decLetterASCII); 

    cout << "\nOriginal Letter: " << letter << endl;
    cout << "Encrypted Letter: " << encLetter << endl;
    cout << "Decrypted Letter: " << decLetter << endl;

    return 0;
}
