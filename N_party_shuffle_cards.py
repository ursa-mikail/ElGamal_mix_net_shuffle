import random

# Toy ElGamal setup (not secure, just demo)
p = 467      # Small prime number
g = 2        # Generator
x = 127      # Private key
Y = pow(g, x, p)  # Public key

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

# Simulate a mix node: shuffle and re-encrypt a list of ciphertexts
def mix_node(ciphertexts):
    random.shuffle(ciphertexts)
    re_encrypted = []
    for M, a, b in ciphertexts:
        a2, b2 = re_encrypt(a, b, g, Y, p)
        re_encrypted.append((M, a2, b2))
    return re_encrypted

# Prepare deck and encrypt
deck = list(range(52))
ciphertexts = [(M, *encrypt(M, g, Y, p)) for M in deck]

print("Original ciphertexts (first 5):")
for i in range(5):
    M, a, b = ciphertexts[i]
    print(f"M={M} a={a} b={b}")

N = 10
# Run through N mix nodes sequentially
current_ciphertexts = ciphertexts
for i in range(1, (N+1)):
    current_ciphertexts = mix_node(current_ciphertexts)
    print(f"\nAfter mix node {i} (first 5):")
    for j in range(5):
        M, a, b = current_ciphertexts[j]
        print(f"M={M} a={a} b={b}")

# Decrypt final ciphertexts to verify messages
print("\nDecrypted messages after 3 mix nodes (first 5):")
for i in range(5):
    M, a, b = current_ciphertexts[i]
    dec = decrypt(a, b, x, p)
    print(f"Original M={M} Decrypted M={dec}")

"""
With N mix nodes (say 3), each node will sequentially:
- Take the ciphertext list it receives,
- Shuffle the order,
- Re-encrypt each ciphertext with fresh randomness,
- Pass the new ciphertext list to the next node.

The ciphertext format (a,b) remains the same throughout.

Starts with 52 encrypted cards.
Runs the ciphertext list through N = 3 mix nodes.
Each node shuffles and re-encrypts the entire list.
Prints the first 5 ciphertexts after each node.
Finally decrypts the first 5 ciphertexts to confirm correctness.

Original ciphertexts (first 5):
M=0 a=339 b=0
M=1 a=59 b=165
M=2 a=360 b=132
M=3 a=149 b=145
M=4 a=57 b=399

After mix node 1 (first 5):
M=9 a=13 b=225
M=20 a=334 b=440
M=4 a=386 b=240
M=7 a=455 b=2
M=39 a=35 b=310

After mix node 2 (first 5):
M=19 a=432 b=304
M=25 a=386 b=99
M=18 a=254 b=411
M=42 a=417 b=35
M=6 a=373 b=18

After mix node 3 (first 5):
M=25 a=417 b=410
M=0 a=118 b=0
M=38 a=243 b=39
M=7 a=164 b=360
M=36 a=313 b=455

Decrypted messages after 3 mix nodes (first 5):
Original M=25 Decrypted M=25
Original M=0 Decrypted M=0
Original M=38 Decrypted M=38
Original M=7 Decrypted M=7
Original M=36 Decrypted M=36

"""