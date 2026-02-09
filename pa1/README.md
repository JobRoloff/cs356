- [Getting Started](#getting-started)
- [Manual Testing](#manual-testing)
  - [Block Encryption / Decryption](#block-encryption--decryption)
  - [Stream Encryption / Decryption](#stream-encryption--decryption)


## Getting Started

```bash
make
make run TYPE=B IN=input.txt OUT=out.txt KEY=key.txt MODE=E
```

## Manual Testing

Given you've  ran the following,

```bash
make cipher
```

Additional Notes:
1. the ciphertext from encrypting a file will be copied and pasted into the input file for decryption. If the decryption of the ciphertext results in the original plaintext, we know the encryption/decryption code didn't result in a failure.


### Block Encryption / Decryption

test: one line containing text
```bash
./cipher B b-e-input.txt b-e-output.txt b-e-key.txt E
cp b-e-output.txt b-d-input.txt
./cipher B b-d-input.txt b-d-output.txt b-e-key.txt D
```


test: empty file
```bash
./cipher B b-e-input-2.txt b-e-output-2.txt b-e-key.txt E
# emptty file so you don't need to copy anyttihng over
./cipher B b-d-input-2.txt b-d-output-2.txt b-e-key.txt D
```

test: trailing newline
```bash
./cipher B b-e-input-3.txt b-e-output-3.txt b-e-key.txt E
cp b-e-output-3.txt b-d-input-3.txt
./cipher B b-d-input-3.txt b-d-output-3.txt b-e-key.txt D
```
### Stream Encryption / Decryption

test: simple single line happy path
```bash
./cipher S s-e-input.txt s-e-output.txt s-e-key.txt E
cp s-e-output.txt s-d-input.txt
./cipher S s-d-input.txt s-d-output.txt s-e-key.txt D
```

test: trailing whitespace is preserved
```bash
./cipher S s-e-input-2.txt s-e-output-2.txt s-e-key.txt E
cp s-e-output-2.txt s-d-input-2.txt
./cipher S s-d-input-2.txt s-d-output-2.txt s-e-key.txt D
```
