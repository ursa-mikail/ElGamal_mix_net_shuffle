
✅ Each of the N mix servers or clients (e.g. 5 nodes) would:
1. Generate its own ElGamal key pair (cₖ, Cₖ = cₖ·G)
2. Contribute to a joint public key:
- Use techniques like key aggregation, threshold encryption, or layered encryption.

3. Encrypt the message (e.g. 0–51) multiple times — each layer encrypted under a different node's public key (like onion encryption).

4. Each node in turn:
- Shuffles the ciphertexts.
- Re-randomizes the ciphertexts to prevent linkability.
- Produces a ZK proof that the shuffle is valid (i.e. permuted + re-randomized but same messages).
- Passes it to the next node.

5. The final node’s shuffle is decrypted in reverse order by each node revealing its private key or partial decryption.

### 🔐 Why Use N Key Pairs?

| Reason                | Why it matters                             |
| --------------------- | ------------------------------------------ |
| **Distributed trust** | No single party holds all decryption power |
| **Privacy**           | No party knows the full permutation        |
| **Accountability**    | Each mixer proves it did a valid shuffle   |
| **Security**          | Eliminates single-point-of-failure         |

### 🧩 ElGamal Mixnet with Multiple Keys (High-level sketch):

```
1. Node A: Encrypt under PK₁, shuffle₁, proof₁
2. Node B: Encrypt (or re-randomize) under PK₂, shuffle₂, proof₂
3. ...
n. Node N: Final shuffleN, proofN

Then:
Decryption₁ → Decryption₂ → ... → DecryptionN (full plaintext recovered)

```

