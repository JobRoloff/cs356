import math as Math
from typing import Callable

class RSA:
    def modInverse(self, encryption_exponent: int, euler_totient: int):
        """
        calculate the modular multiplicative inverse, python 3.8+ provides a built in use of the pow function to accomplish this d = pow(e, -1, n)
        
        :param encryption_exponent: 
        :param euler_totient: calculates the number of numbers up to n that are relatively prime or coprime to n; meaning that they share no common factors with n other than 1
        """
        return pow(encryption_exponent, -1, euler_totient)

    # GenKeyFunction = Callable[[int, int], tuple(int, int, int)]
    def genKey(self,prime_number_1: int, prime_number_2: int) -> tuple[int, int, int]:
        product_of_primes: int = prime_number_1 * prime_number_2
        euler_totient: int = (prime_number_1-1)*(prime_number_2-1)
        
        encryption_exponent: int = 0
        for value in range(2, euler_totient):
            if Math.gcd(value, euler_totient) == 1:
                encryption_exponent = value
                break
        
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

