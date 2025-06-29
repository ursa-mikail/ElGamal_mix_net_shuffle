package main

import (
	"fmt"

	"go.dedis.ch/kyber/v3"
	"go.dedis.ch/kyber/v3/group/edwards25519"
	"go.dedis.ch/kyber/v3/proof"
	"go.dedis.ch/kyber/v3/shuffle"
)

// Ciphertext is ElGamal encrypted data
type Ciphertext struct {
	X kyber.Point
	Y kyber.Point
}

// Node represents a mix server with keypair and ZK proof
type Node struct {
	priv  kyber.Scalar
	pub   kyber.Point
	proof []byte
}

func main() {
	n := 52       // Number of messages
	numNodes := 5 // Number of mixers

	suite := edwards25519.NewBlakeSHA256Ed25519()
	rand := suite.RandomStream()

	// 1. Initialize nodes with individual keys
	nodes := make([]*Node, numNodes)
	jointPub := suite.Point().Null()
	for i := 0; i < numNodes; i++ {
		priv := suite.Scalar().Pick(rand)
		pub := suite.Point().Mul(priv, nil)
		nodes[i] = &Node{priv: priv, pub: pub}
		jointPub.Add(jointPub, pub) // Aggregate public key
	}

	// 2. Encode 0–51 as messages (points)
	msgs := make([]kyber.Point, n)
	for i := 0; i < n; i++ {
		sc := suite.Scalar().SetInt64(int64(i))
		msgs[i] = suite.Point().Mul(sc, nil)
	}

	// 3. Encrypt each message under joint public key
	ciphertexts := make([]Ciphertext, n)
	for i := 0; i < n; i++ {
		r := suite.Scalar().Pick(rand)
		X := suite.Point().Mul(r, nil)
		Y := suite.Point().Mul(r, jointPub)
		Y.Add(Y, msgs[i])
		ciphertexts[i] = Ciphertext{X, Y}
	}

	// 4. Each node shuffles and proves
	for i, node := range nodes {
		Xs := make([]kyber.Point, n)
		Ys := make([]kyber.Point, n)
		for j := range ciphertexts {
			Xs[j] = ciphertexts[j].X
			Ys[j] = ciphertexts[j].Y
		}

		Xbar, Ybar, prover := shuffle.Shuffle(suite, nil, jointPub, Xs, Ys, rand)
		proofBytes, err := proof.HashProve(suite, "PairShuffle", prover)
		if err != nil {
			panic(fmt.Sprintf("Proof failed at node %d: %v", i, err))
		}
		verifier := shuffle.Verifier(suite, nil, jointPub, Xs, Ys, Xbar, Ybar)
		if err := proof.HashVerify(suite, "PairShuffle", verifier, proofBytes); err != nil {
			panic(fmt.Sprintf("Verification failed at node %d: %v", i, err))
		}

		node.proof = proofBytes

		// Update ciphertexts with shuffled result
		for j := range ciphertexts {
			ciphertexts[j] = Ciphertext{Xbar[j], Ybar[j]}
		}
		fmt.Printf("✅ Node %d: shuffle + proof OK\n", i)
	}

	// 5. Output: first few shuffled ciphertexts
	fmt.Println("\nShuffled values (first N ciphertexts):")
	for i := 0; i < n; i++ {
		fmt.Printf("X[%d]: %s\n", i, ciphertexts[i].X.String())
		fmt.Printf("Y[%d]: %s\n", i, ciphertexts[i].Y.String())
	}
}

/*
% go mod tidy
% go run main.go
✅ Node 0: shuffle + proof OK
✅ Node 1: shuffle + proof OK
✅ Node 2: shuffle + proof OK
✅ Node 3: shuffle + proof OK
✅ Node 4: shuffle + proof OK

Shuffled values (first N ciphertexts):
X[0]: 09f26e5cafd588f8c5705d0f3ea8bb1a12cd80b6030bab21eaefbda3cdc86f48
Y[0]: 98ddc946d743da2af153a0313cb0e3fccf05adbace4912b980a8ea81702af897
X[1]: b77d85ca3674f884c882721ed1b6db1e378acdcd096934d27841acf08e2401ce
Y[1]: 12bcce598d2136f539219287b88038aba9e9c68904a828d2b2eed09c32aa3a79
:
X[50]: b2bf757c2b071015ea9e575a8fad42c3e7e5b71c6d216057e3e64a9e8e40d9ce
Y[50]: 22286aa23314c97184495a11efff7302861b3170a2cf3f19b9c9634184594bc3
X[51]: 7e6c2491c533ad659518e7145e2be1ea656c951e70f329b23a06b8a8274b4556
Y[51]: bbb0e1e2952df21f26f09f322d8054e06be2000193eb86ee9cec81ecb7a761a0

- Generate N key pairs (1 per node - Each node has its own keypair.)
- Encrypt each value in layers
	- Structs for organizing:
		- Node – holds keypair and proofs.
		- Ciphertext – (X, Y) pair.

		- Encrypts 52 values (0–51) once under a joint public key (sum of all public keys).
		- Each node shuffles, re-randomizes, and proves the shuffle.
		- Final output can be decrypted in reverse (not included here unless you request it).

- Allow each node to shuffle + prove
- Eventually decrypt step-by-step

*/
