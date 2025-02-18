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


int main()
{
    long long e, d, n;

    generateKeys(e, d, n);

    cout << "Public Key (e, n): (" << e << ", " << n << ")" << endl;
    cout << "Private Key (d, n): (" << d << ", " << n << ")" << endl;


    return 0;
}
