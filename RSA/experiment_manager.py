from dataclasses import dataclass
from typing import Callable, TypeVar
from rsa import RSA
import time

@dataclass
class TrialResult:
    keygen_s: float
    encrypt_s: float
    decrypt_s: float


T = TypeVar("T")

@dataclass
class ExperimentSummary:
    average_keygen_s: float
    average_encrypt_s: float
    average_decrypt_s: float
    runs: int

class ExperimentManager:
    def __init__(self) -> None:
        self.rsa = RSA()

    
    def _time_call(self, function_to_run: Callable[[], T]) -> tuple[float, T]:
        start_time = time.perf_counter()
        function_return_value: T = function_to_run()
        finish_time = time.perf_counter()
        duration = finish_time - start_time
        return (duration, function_return_value)
    
    
    def run_trial_by_bits(self, prime_bits: int, message: str) -> TrialResult:
        keygen_s, key = self._time_call(lambda: self.rsa.genKeyFromBits(prime_bits))
        encryption_exponent, decryption_exponent, product_of_primes = key

        encoded_message, message_length = self._encode_message_to_int(message)

        if encoded_message >= product_of_primes:
            raise ValueError(
                f"Message is too big for modulus n. "
                f"Message bytes={message_length}, n_bits={product_of_primes.bit_length()}"
            )

        encrypt_s, ciphertext = self._time_call(
            lambda: self.rsa.encrypt(encryption_exponent, product_of_primes, encoded_message)
        )

        decrypt_s, plaintext = self._time_call(
            lambda: self.rsa.decrypt(decryption_exponent, product_of_primes, ciphertext)
        )

        if plaintext != encoded_message:
            raise ValueError("RSA failed: decrypted int != original encoded int")

        decoded_plaintext = self._decode_int_to_message(plaintext, message_length)
        if decoded_plaintext != message:
            raise ValueError("RSA failed: decrypted text != original message")

        return TrialResult(keygen_s=keygen_s, encrypt_s=encrypt_s, decrypt_s=decrypt_s)
    
    def run_trial(self, primes: tuple[int, int], message: str) -> TrialResult:
        keygen_s, key = self._time_call(
            lambda: self.rsa.genKey(prime_number_1=primes[0], prime_number_2=primes[1])
        )
        encryption_exponent, decryption_exponent, product_of_primes = key
        
        encoded_message, message_length = self._encode_message_to_int(message)
        
        # check message is too big
        if encoded_message >= product_of_primes:
            raise ValueError (f"Message is too big given the size of the provided primes"
                              f"Message int: {encoded_message}, Modulus n: {product_of_primes}")
        
        encrypt_s, ciphertext = self._time_call(
            lambda: self.rsa.encrypt(
                encryption_exponent=encryption_exponent, 
                product_of_primes=product_of_primes, 
                message_to_encrypt=encoded_message
            )
        )
        
        decrypt_s, plaintext = self._time_call(
            lambda: self.rsa.decrypt(
                decryption_exponent=decryption_exponent, 
                product_of_primes=product_of_primes, 
                ciphertext=ciphertext)
            )
        
        if plaintext != encoded_message:
            raise ValueError(
                "RSA failed: decrypted int != origincal encoded int."
                "primes might not be prime."
                f"\norigional={encoded_message}\ndecrypted={plaintext}"
            )
        
        decoded_plaintext = self._decode_int_to_message(plaintext, message_length)
        if decoded_plaintext != message:
            raise ValueError("RSA failed: decrypted text != og message")
        
        return TrialResult(keygen_s=keygen_s, encrypt_s=encrypt_s, decrypt_s=decrypt_s)
         
    def _avg_summary(self, results: list[TrialResult]) -> ExperimentSummary:
        
        runs: int = len(results)
        
        average_keygen_s: float = sum(result.keygen_s for result in results) / runs
        average_encrypt_s: float = sum(result.encrypt_s for result in results) / runs
        average_decrypt_s: float = sum(result.decrypt_s for result in results) / runs
        
        return ExperimentSummary(
            average_keygen_s= average_keygen_s,
            average_encrypt_s=average_encrypt_s,
            average_decrypt_s=average_decrypt_s,
            runs = runs
        )
        
    def summarize_by_prime_bits():
        return
    
    def _encode_message_to_int(self, message: str) -> tuple[int, int]:
        data = message.encode("utf-8")
        return int.from_bytes(data, byteorder="big", signed=False), len(data)
    
    
    def _decode_int_to_message(self, value: int, length: int) -> str:
        # length = (value.bit_length() + 7) // 8 or 1
        data = value.to_bytes(length, byteorder="big", signed=False)
        return data.decode("utf-8")
    def run_experiment_by_bits(
    self,
    prime_bits: int,
    message: str,
    runs: int = 3,
    warm_up_runs: int = 1
) -> ExperimentSummary:
        for _ in range(warm_up_runs):
            self.run_trial_by_bits(prime_bits, message)

        results: list[TrialResult] = []
        for _ in range(runs):
            results.append(self.run_trial_by_bits(prime_bits, message))

        return self._avg_summary(results)
   
    def run_experiment(
        self,
        primes: tuple[int, int],
        message: str,
        runs: int = 3,
        warm_up_runs: int = 1
    ) -> ExperimentSummary:
        for _ in range(warm_up_runs):
            self.run_trial(primes, message)
        
        results: list[TrialResult] = []
        for _ in range(runs):
            results.append(self.run_trial(primes, message))
            
        return self._avg_summary(results)
    