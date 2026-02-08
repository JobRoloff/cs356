import math as Math
import random
import secrets
import typing
from typing import Callable


class RSA:
    def is_probable_prime(self, prime1: int, prime2: int = 20) -> bool:
        if prime1 < 2:
            return False
        small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
        for prime_number in small_primes:
            if prime1 == prime_number:
                return True
            if prime1 % prime_number == 0:
                return False
        # write n-1 = d * 2^s
        d = prime1 - 1
        s = 0
        while d % 2 == 0:
            s += 1
            d //= 2

        # witness loop
        for _ in range(prime2):
            a = random.randrange(2, prime1 - 1)
            x = pow(a, d, prime1)
            if x == 1 or x == prime1 - 1:
                continue
            for __ in range(s - 1):
                x = pow(x, 2, prime1)
                if x == prime1 - 1:
                    break
            else:
                return False
        return True
    
    def generate_prime(self, bits: int) -> int:
        while True:
            # odd candidate with top bit set
            candidate = secrets.randbits(bits) | (1 << (bits - 1)) | 1
            if self.is_probable_prime(candidate, prime2=40):
                return candidate
            
    def modInverse(self, encryption_exponent: int, euler_totient: int):
        """
        calculate the modular multiplicative inverse, python 3.8+ provides a built in use of the pow function to accomplish this d = pow(e, -1, n)
        
        :param encryption_exponent: 
        :param euler_totient: calculates the number of numbers up to n that are relatively prime or coprime to n; meaning that they share no common factors with n other than 1
        """
        return pow(encryption_exponent, -1, euler_totient)

    def genKeyFromBits(self, prime_bits: int) -> tuple[int, int, int]:
        prime1 = self.generate_prime(prime_bits)
        prime2 = self.generate_prime(prime_bits)
        return self.genKey(prime1, prime2)
        

    # GenKeyFunction = Callable[[int, int], tuple(int, int, int)]
    def genKey(self,prime_number_1: int, prime_number_2: int) -> tuple[int, int, int]:
        product_of_primes: int = prime_number_1 * prime_number_2
        euler_totient: int = (prime_number_1-1)*(prime_number_2-1)
        
        # encryption_exponent: int = 0
        encryption_exponent = 65537
        # for value in range(3, euler_totient, 2):
        #     if Math.gcd(value, euler_totient) == 1:
        #         encryption_exponent = value
        #         break
        if Math.gcd(encryption_exponent, euler_totient) != 1:
            encryption_exponent = 3
            while Math.gcd(encryption_exponent, euler_totient) != 1:
                encryption_exponent += 2
        
        decryption_exponent = self.modInverse(encryption_exponent, euler_totient)
        
        return (encryption_exponent, decryption_exponent, product_of_primes)
    
    def encrypt(self, encryption_exponent: int, product_of_primes: int, message_to_encrypt: int) -> int:
        """
        Encryption takes the message raises it to the power of e (the encryption exponent) then takes the modulo of that product by n
        """
        return pow(message_to_encrypt, encryption_exponent, product_of_primes)
    
    def decrypt(self, decryption_exponent: int, product_of_primes: int, ciphertext: int) -> int:
        """
        Docstring for decrypt
        #Decryption takes the cipher text, raises it to the power of d (the decryption exponent) and then takes the modulo of that product by n
        """
        return pow(ciphertext, decryption_exponent, product_of_primes)

