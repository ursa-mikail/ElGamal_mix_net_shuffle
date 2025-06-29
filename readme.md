# ElGamal Mix-Net 


### 🎴 Analogy: Card Shuffling
- A normal dealer can fake a shuffle—pretending to shuffle but actually keeping key cards in place.
- In secure systems, we want to prevent cheating, even if some "dealers" (mixing nodes) are dishonest.
- We do this using encryption and a group of nodes (mix-net). As long as one node is honest, the whole shuffle remains secure.


🧪 Proof of Shuffle (Mix-net)
We use a mix-net, where multiple servers perform:

1. Permutation (shuffle the order)

2. Re-encryption (hide the mapping)

Then, the final ciphertexts are jointly decrypted using threshold decryption, where secret key is shared among servers. Even if some servers are dishonest, as long as at least one is honest, the shuffle is trustworthy.

| **Step** | **Type**          | **What Happens**                           | **Purpose**                        |
| -------- | ----------------- | ------------------------------------------ | ---------------------------------- |
| 1        | Encryption        | Each message $M$ is encrypted as $(a, b)$  | Protects content                   |
| 2        | **Permutation**   | Ciphertexts are rearranged in random order | Break order linkage                |
| 3        | **Re-encryption** | Each ciphertext is re-randomized           | Break value linkage                |
| 4        | **Proof**         | Zero-knowledge proof published             | Verifies shuffle was done honestly |
| 5        | Decryption        | Jointly decrypt final ciphertexts          | Reveal $M$, with privacy preserved |


In the basic ElGamal mix-net shuffle setup:
- Each ciphertext is a pair (a,b). So no matter how many parties are involved, each ciphertext remains 2 values.
- The mix nodes (often called mix servers) each take the entire list of ciphertext pairs and do two things:
	1. Permute (shuffle) the order of the ciphertext pairs to break any link between input and output order.

	2. Re-encrypt each ciphertext with fresh randomness to hide any correlation between input ciphertext and output ciphertext values.

The ciphertext itself always consists of just two components a and b.

The nodes doing the shuffle and re-encryption operate on these pairs (a,b).

You can have multiple such nodes, each doing their own shuffle + re-encryption in sequence.

```Example with 2 nodes: 
Node 1: receives ciphertext list { ( 𝑎_𝑖 , 𝑏_𝑖 ) }, shuffles and re-encrypts → outputs { ( 𝑎_𝑖′ , 𝑏_𝑖′ ) } 
Node 2: receives { ( 𝑎_𝑖′ , 𝑏_𝑖′ ) } , shuffles and re-encrypts again → outputs { ( 𝑎_𝑖′′ , 𝑏_𝑖′′ ) }
Final output is decrypted jointly.

```

| Concept         | Description                              |
| --------------- | ---------------------------------------- |
| Ciphertext      | Always 2 parts: $a, b$                   |
| Shuffling node  | Receives list of $(a,b)$ pairs           |
| Number of nodes | Can be many, each shuffling sequentially |


## What do $$\ 𝑎_𝑖 \$$ and $$\ 𝑏_𝑖 \$$ ​ represent in ElGamal encryption?

Think of a secret message $$/ 𝑀_𝑖 /$$ — like:
- Your vote in an election
- Your bid in an auction
- A card in a deck (e.g., “Ace of Spades” represented by 0)
- Any piece of data to keep secret

### 🧠 What Problem Are We Solving?
To shuffle a list of encrypted values (like votes or cards) such that:

- No one knows which original value maps to which final one (privacy).
- Everyone can verify that the shuffle was honest (verifiability).

This process is called a verifiable shuffle, and it's used in electronic voting, privacy-preserving systems, and zero-knowledge proofs.


To protect that message $$/ 𝑀_𝑖 /$$​ , ElGamal encryption transforms it into 2 numbers, $$\ 𝑎_𝑖 \$$ and $$\ 𝑏_𝑖 \$$ , which together are the encrypted message — kind of like a sealed envelope.

- $$\ 𝑎_𝑖 \$$ = Part 1 of the encrypted message (think of it as the "lock" part) 
- $$\ b_𝑖 \$$  = Part 2 of the encrypted message (think of it as the "sealed contents" part) 

Together, ( $$\ 𝑎_𝑖 \$$, $$\ 𝑏_𝑖 \$$ )  look like random numbers to someone without the secret key — they can't figure out what $$/ 𝑀_𝑖 /$$​ is just by looking at them.


| Concept                 | Real-Life Equivalent                                                                                  |
| ----------------------- | ----------------------------------------------------------------------------------------------------- |
| $M_i$ (Message)         | The letter or card inside an envelope                                                                 |
| Encryption → $a_i,b_i$  | The sealed envelope with a special lock on it                                                         |
| Shuffle + Re-encryption | Mixing the envelopes and changing the locks so they look different but still contain the same letters |
| Decryption              | Using the key to open the envelope and read the letter                                                |


### Why do we have $$\ 𝑎_𝑖 \$$ and $$\ 𝑏_𝑖 \$$​ instead of just 1 number? 

- ElGamal encryption mathematically splits the ciphertext into 2 parts: 

$$\ 𝑎_𝑖 = g^{k_i} \mod p\$$ 

$$\ 𝑏_𝑖 = Y^{k_i} x M_i \mod p \$$

This structure lets you: 
- Re-encrypt ciphertexts by multiplying $$\ 𝑎_𝑖 \$$ and $$\ 𝑏_𝑖 \$$ with new randomness (lock changed) 
- Perform proofs and shuffles without revealing the message 

| Step                                | Purpose                                                                                  |
| ----------------------------------- | ---------------------------------------------------------------------------------------- |
| 1. Encrypt messages                 | Using ElGamal: $(a, b) = (g^k, Y^k \cdot M)$                                             |
| 2. Mix nodes permute and re-encrypt | Without decrypting, change order and randomness                                          |
| 3. Final decryption                 | Done by multiple nodes using threshold secret sharing                                    |
| 4. Verification                     | Everyone can check that shuffle is valid without knowing which input became which output |



| **Phase**                   | **Operation**                            | **Action**                                                                | **Goal**                | **Who Does It?**      |
| --------------------------- | ---------------------------------------- | ------------------------------------------------------------------------- | ----------------------- | --------------------- |
| **1. Input**                | Original encryption                      | Encrypt each message $M_i$ with random $k_i$                              | Data privacy            | Sender (e.g., voters) |
| **2. Shuffle**              | **Permutation**                          | Randomly shuffle the list of ciphertexts                                  | Hide input–output order | Mix server            |
| **3. Re-encryption**        | **Re-randomize each ciphertext**         | Multiply each $a_i, b_i$ by fresh encryption of 1 (new randomness $k'_i$) | Prevent linkability     | Mix server            |
| **4. Proof of Shuffle**     | Zero-knowledge proof (e.g. Neff’s proof) | Publish cryptographic proof that shuffle is correct                       | Public verifiability    | Mix server            |
| **5. Threshold Decryption** | Joint decryption by servers              | Use private shares of secret key to decrypt the final shuffled outputs    | Get plaintext           | Decryption servers    |



| Phase      | Action                                | Example                            |
| ---------- | ------------------------------------- | ---------------------------------- |
| Encrypt    | $M = 10 \rightarrow (a=118, b=406)$   | Each message is encrypted uniquely |
| Shuffle    | Shuffle list of ciphertexts           | Order is randomly changed          |
| Re-encrypt | New random $k'$ applied to hide links | $(a, b) \rightarrow (a', b')$      |
| Decrypt    | Recover $M$ using private key         | Confirms data integrity            |


## 🔄 Visual Flow for 52 Cards

| Step                      | What Happens                      | How Many |
| ------------------------- | --------------------------------- | -------- |
| 🔐 Encrypt each card      | $M_i \rightarrow (a_i, b_i)$      | 52       |
| 🔀 Shuffle and re-encrypt | Mix and re-randomize all 52 pairs | 52       |
| ✅ Prove shuffle is valid  | Zero-knowledge proof              | 1 proof  |
| 🔓 Decrypt                | Get back all $M_i$, in new order  | 52       |


### Summary: 
- $$\ 𝑎_𝑖 \$$ and $$\ 𝑏_𝑖 \$$​ together hide the message $$/ 𝑀_𝑖 /$$ ​ so no one can read it without the secret key. 

- The shuffle mixes the encrypted messages to break any link between the original order and final order. 

- Re-encryption changes $$\ 𝑎_𝑖 \$$, $$\ 𝑏_𝑖 \$$ ​ so ciphertexts look different, even though they encrypt the same $$/ 𝑀_𝑖 /$$​ .


In ElGamal encryption for each item (like a vote or card), the full data is:
```
M_i, a_i, b_i
```

🔁 After shuffle and re-encryption:
You have:
```
M_j (same M, new index), a'_j, b'_j
```

> 💥 You don’t see the M_j value directly in the encrypted form
> Because it's still encrypted — hidden inside (a', b')

| Symbol | Meaning                                                  |
| ------ | -------------------------------------------------------- |
| $M_i$  | the original **message**, e.g. 0 to 51 (the card number) |
| $a_i$  | $g^{k_i} \mod p$, part of the ciphertext                 |
| $b_i$  | $Y^{k_i} \cdot M_i \mod p$, part of the ciphertext       |



| Stage            | What you see              | Message visible?                  |
| ---------------- | ------------------------- | --------------------------------- |
| Before shuffle   | `[(M_i, a_i, b_i)]`       | ✅ Yes, in testing (we print it)   |
| After shuffle    | `[(new_index, (a’, b’))]` | ❌ No — message is still encrypted |
| After decryption | `[(M_j, a’, b’)]`         | ✅ Yes, after decryption           |


| Confusion                                            | Clarification                                                                    |
| ---------------------------------------------------- | -------------------------------------------------------------------------------- |
| "Why do (a, b) values look unrelated after shuffle?" | Because they were **re-encrypted**, so the randomness changed                    |
| "How do I know the shuffle is valid?"                | You can't by looking — a **proof of shuffle** is used to confirm correctness     |
| "Are the messages preserved?"                        | Yes, the **underlying message $M$** is unchanged — you verify this by decryption |


| Use Case                  | What is $M$?                        | Why keep it secret?           |
| ------------------------- | ----------------------------------- | ----------------------------- |
| **Electronic voting**     | A person's vote (e.g. candidate ID) | Prevent vote-buying, coercion |
| **Private auctions**      | A bidder’s amount                   | Prevent unfair advantage      |
| **Anonymous credentials** | User identity hash                  | Protect user privacy          |


| Scenario                                  | Should $M$ be secret? | Notes                            |
| ----------------------------------------- | --------------------- | -------------------------------- |
| Voting, auctions, privacy-preserving tech | ✅ Yes                 | Message = confidential payload   |
| Educational/demo/test code                | ❌ Not necessary       | Message shown for learning       |
| Real-world protocols                      | ✅ Yes                 | Enforced via encryption + proofs |



### 🧠 Why does the second set (shuffled) not include M_j?
Because in a real protocol, you don't reveal the message until the end.

```
We kept track of M separately just to label which ciphertext came from which original message 

That’s why: 
(25, (428, 321)) 

Where: 25 is the original message number 
(428, 321) is the new ciphertext (a’, b’) after re-encryption 

In real usage: 
Only (a’, b’) is public 
The corresponding M is hidden 
The mapping from old to new ciphertexts is proven, not shown

✅ If you want to trace full data during testing:
Change the output format to:
[(original_M_i, original_(a,b), new_(a', b'))]

Therein:
[(25, (original_a, original_b), (new_a, new_b))]
```


## 🚫 ElGamal Mix-Net ≠ VRF
ElGamal mix-nets:
- Shuffle encrypted data to break linkage between input and output.
- Provide zero-knowledge proofs to verify the shuffle was honest.
- Don’t produce deterministic, verifiable random outputs from a known input.

They are not VRFs, but instead tools for:
- Privacy-preserving voting, e.g. tally votes without knowing who voted for whom.

✅ How ElGamal mix-nets help:
1. Each voter's choice (e.g. "Alice votes for Candidate A") is encrypted as:

$$\ 
(a_i​,b_i​) = ElGamal_encrypt(M_i​)
\$$

where $$\ M_i​)\$$ is the vote (e.g. 0 for Alice, 1 for Bob...)

2. All encrypted votes are submitted into a ballot box (a public list).

3. Mix nodes (run by election trustees) do:
- Shuffle the encrypted votes
- Re-encrypt each one
- Publish a zero-knowledge proof that:
	- The output list is a correct shuffle + re-encryption of the input list
	- No vote was changed or lost

4. Finally, the mix nodes jointly decrypt the shuffled ciphertexts.

🔍 Because of the shuffle:
- Voters are anonymized
- The order is broken
- Yet, the tally remains verifiably correct

- Anonymous credential systems

🧠 Problem:
To prove something about yourself without revealing who you are.

Example:
- You're over 18
- You're a certified user
- You own a valid credential

🔒 Goal:
- Authenticate attributes, not identity
- Avoid linkability (you can’t be tracked across uses)

✅ How ElGamal + mix-nets help:
1. A trusted authority issues encrypted credentials:
	ElGamal_encrypt(user’s attribute)

2. When you want to use your credential, a mix-net:	
- Shuffles and re-encrypts all issued credentials
- Publishes a ZK proof of valid shuffling

3. You can now reveal only the attribute, not your identity.

- Oblivious message routing (e.g. Tor, Sphinx)

🧠 Problem:
You want to send a message anonymously through a network.

But:
- You don’t want any server to know both who sent it and who it's for.
- You don’t want attackers to correlate message paths by observing network traffic.

🔒 Goal:
- Sender and receiver are unlinkable
- Path is untraceable
- Each node only knows its next hop

✅ How mix-nets and ElGamal help:
1. The sender encrypts their message in layers (like an onion):
- Layer 1: Encrypted for Node C
- Layer 2: Encrypted for Node B
- Layer 3: Encrypted for Node A

2. The message enters the network:
- Node A decrypts outer layer and forwards to Node B
- Node B does the same
- Eventually it reaches the destination

3. In systems like Sphinx or Loopix, a batch of such messages is:
- Shuffled and re-encrypted by each node
- Making traffic patterns oblivious (hard to trace)

4. Mix-nets anonymize messages while proving:
- The routing is correct
- No message was dropped or altered

| Use Case                | What’s Shuffled?    | Why?                                     |
| ----------------------- | ------------------- | ---------------------------------------- |
| Voting                  | Encrypted votes     | Break link between voter and vote        |
| Anonymous credentials   | Encrypted ID/tokens | Prevent cross-site or cross-use tracking |
| Onion/mix routing (Tor) | Encrypted messages  | Obfuscate paths and sources              |


✅ ElGamal Mix-Net helps with verifiable shuffles

🔄 To build a VRF-style tool from ElGamal, you'd need to:
- Use ElGamal encryption for input masking
- Prove properties (e.g., mix was random and unbiased) via zero-knowledge
- Possibly add a hash-to-group or hash-to-curve layer to anchor to a seed

So in advanced protocols (like MixCoin, or modern zero-knowledge random beacons), you might combine ElGamal shuffles with VRFs or commitments to achieve verifiable randomness in privacy-preserving ways.


| Use Case                                           | Tool                                   |
| -------------------------------------------------- | -------------------------------------- |
| I want a verifiable shuffle                        | Use **ElGamal + ZKP proof of shuffle** |
| I want deterministic random output + verifiability | Use a **VRF**                          |


| Concept        | VRF                         | ElGamal Shuffle                       |
| -------------- | --------------------------- | ------------------------------------- |
| Deterministic? | Yes (for a given key/input) | No (depends on random permutations)   |
| Verifiable?    | Yes (output + proof)        | Yes (ZK proof of shuffle correctness) |
| Output?        | Random-looking number       | Shuffled ciphertexts                  |
| Use Case       | Random selection            | Anonymous data reordering             |


---

## 🔐 What is ElGamal Encryption?

### Key Generation:
1. Choose a large prime `p`, and a generator `g`.
2. Choose a secret key `x`, then compute the public key:

$$\
Y = g^x mod p
\$$

3. Public key: `(Y, g, p)`
4. Secret key: `x`

---

### Encrypting a Message `M`:
1. Pick a random number `k`
2. Compute:

$$\
a = g^k mod p
b = Y^k * M mod p
\$$

3. Ciphertext is the pair: `(a, b)`

---

### Decrypting:
To recover `M`, compute:

$$\
M = b / a^x mod p
\$$

**Why this works:**

- Given:  

$$\
b = Y^k * M = g^(xk) * M
a^x = g^(kx)
\$$

- Then:
$$\
b / a^x = (g^(xk) * M) / g^(kx) = M
\$$

---

## 🔄 Re-Encryption and Mixing

We can shuffle and re-encrypt encrypted values **without decrypting them**.

### Example:

Original ciphertext:

$$\
(a1, b1) = (g^k1, Y^k1 * M)
\$$

To re-encrypt, pick a new random `k2`, and compute:

$$\
a2 = g^k2 * a1 mod p
b2 = Y^k2 * b1 mod p
\$$

This results in:

$$\
a2 = g^(k1 + k2)
b2 = Y^(k1 + k2) * M
\$$

So it's **as if we encrypted the message again**, but without ever decrypting it!

- but were a single end decryption process can decrypt the answer.

$$\
M = \frac{b}{a^x}

b = Y^{k_1 + k_2} * M

a = (g^{k_1 + k_2})^x

Y = g^x \mod p

\$$

---

## 🔁 Permutation = Shuffling

**What**: Change the order of the list.

**Why**: Break the link between input and output.

**Example**: You randomly rearrange the encrypted items:

```plaintext
Original order:
[(a₁, b₁), (a₂, b₂), (a₃, b₃), (a₄, b₄)]

After permutation:
[(a₃, b₃), (a₁, b₁), (a₄, b₄), (a₂, b₂)]

🔐 Re-encryption = Hide Mapping
What: Re-randomize the encryption by multiplying with a new encryption of 1.

Why: So even if someone knows the encryption of M, they won’t recognize it after the shuffle.

Mathematically:
If the original ciphertext is:
(a, b) = (g^k, Y^k ⋅ M)

You choose a new random k′, and compute:
a′ = g^k′ ⋅ a mod p
b′ = Y^k′ ⋅ b mod p

After substitution:
a′ = g^(k + k′)
b′ = Y^(k + k′) ⋅ M

So the result is a fresh encryption of the same message M, with new randomness.
```
