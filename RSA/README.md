# RSA Timing Experiments (CS356)

A small Python project that benchmarks the RSA workflow across different **prime sizes** and **message lengths**, measuring the time spent in:

- **Key generation** (including prime generation)
- **Encryption**
- **Decryption**

The goal is to record observations that answer:

1) How do longer prime numbers and longer messages affect RSA speed?  
2) What part of RSA takes the most time (keygen, encryption, decryption) and why?  
3) Is encryption or decryption faster, and why?

---

## What this project does

For each combination of:

- Prime sizes (bits per prime): `128, 256, 512, 1024`
- Message lengths (bytes requested): `8, 32, 64, 96`

the program:

1. Generates two probable primes `p` and `q` of the given bit size.
2. Builds RSA key material:
   - `n = p*q`
   - `phi(n) = (p-1)(q-1)`
   - choose a small public exponent `e`, compute `d = e^{-1} mod phi(n)`
3. Encodes the message to an integer `m`.
4. Encrypts: `c = m^e mod n`
5. Decrypts: `m = c^d mod n`
6. Verifies the decrypted plaintext matches the original.
7. Records average timing results over multiple runs.

If a requested message is too large to fit in the modulus (`m >= n`), the message is automatically capped to the maximum safe length for that key size.

---

## Project structure

Typical layout:

- `main.py`  
  Runs the experiment grid and prints `ExperimentSummary` results.

- `experiment_manager.py`  
  Orchestrates trials, measures timing, computes averages, validates correctness.

- `rsa.py`  
  RSA implementation (key generation, encrypt, decrypt) plus prime generation and primality testing used for key generation timing.

---

## Requirements

- Python 3.8+ (recommended 3.10+)

No external dependencies are required (uses only the Python standard library).

---

## How to run

From the project directory:

```bash
python main.py
