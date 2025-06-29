import random

# Toy ElGamal setup (not secure, just demo)
p = 467      # Small prime number
g = 2        # Generator
x = 127      # Private key
Y = pow(g, x, p)  # Public key: Y = g^x mod p

def encrypt(M, g, Y, p):
    k = random.randint(1, p - 2)
    a = pow(g, k, p)
    b = (pow(Y, k, p) * M) % p
    return a, b

def re_encrypt(a, b, g, Y, p):
    k2 = random.randint(1, p - 2)
    a2 = (pow(g, k2, p) * a) % p
    b2 = (pow(Y, k2, p) * b) % p
    return a2, b2

def decrypt(a, b, x, p):
    ax = pow(a, x, p)
    ax_inv = pow(ax, -1, p)
    return (b * ax_inv) % p

deck = list(range(52))

# Encrypt all cards
ciphertexts = [(M, *encrypt(M, g, Y, p)) for M in deck]

# Shuffle ciphertexts (shuffle only ciphertexts but keep track of original M)
shuffled = ciphertexts.copy()
random.shuffle(shuffled)

# Re-encrypt shuffled ciphertexts
re_encrypted = []
for M, a, b in shuffled:
    a2, b2 = re_encrypt(a, b, g, Y, p)
    re_encrypted.append((M, a, b, a2, b2))

# Show original, shuffled+re-encrypted
print(f"{'M':>3} | {'orig a':>6} {'orig b':>6} | {'new a':>6} {'new b':>6}")
print("-" * 37)
for (M, a, b, a2, b2) in re_encrypted:
    print(f"{M:3} | {a:6} {b:6} | {a2:6} {b2:6}")

# Optional: verify correctness by decrypting new ciphertexts
print("\nDecrypted messages after shuffle:")
for (M, a, b, a2, b2) in re_encrypted:
    dec = decrypt(a2, b2, x, p)
    print(f"M={M} decrypted = {dec}")

"""
For each card: 
The original message 𝑀_𝑖 
The original ciphertext ( 𝑎_𝑖 , 𝑏_𝑖 ) 
The shuffled and re-encrypted ciphertext ( 𝑎_𝑖′ , 𝑏_𝑖′ ) 

This way you can trace each item fully through the shuffle and re-encryption.


  M | orig a orig b |  new a  new b
-------------------------------------
 18 |    384     83 |    258    448
 33 |    120     54 |    263    158
  0 |    232      0 |     34      0
 36 |    339    185 |    268    372
 :
 38 |     14    323 |     87    377
 46 |    307    342 |    281    160

Decrypted messages after shuffle:
M=18 decrypted = 18
M=33 decrypted = 33
M=0 decrypted = 0
M=36 decrypted = 36
:
M=38 decrypted = 38
M=46 decrypted = 46
"""