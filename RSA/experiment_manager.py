"""
Questions to answer:
Influence of longer (prime numbers && messages) on RSA Process?
Most time consuming part of RSA?
Is encryption or decryption faster? Why so?


the manager class handles timing of the rsa processes given different prime number sizes (our experiment)
"""
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
    
    def run_trial(self, primes: tuple[int, int], message: str) -> TrialResult:
        keygen_s, key = self._time_call(
            lambda: self.rsa.genKey(prime_number_1=primes[0], prime_number_2=primes[1])
        )
        encryption_exponent, decryption_exponent, product_of_primes = key
        
        encoded_message : int = self._encode_message_to_int(message) % product_of_primes
        
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
        
        if plaintext != message:
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
        
    def _encode_message_to_int(self, message: str) -> int:
        data = message.encode("utf-8")
        return int.from_bytes(data, byteorder="big", signed=False)
    
    def _encode_message_to_int_mod_n(self, message:str, product_of_primes: int) -> int:
        encoded_message = int.from_bytes(message.encode("utf-8"), byteorder="big", signed=False)
        return encoded_message % product_of_primes
    
    def _decode_int_to_message(self, value: int):
        length = (value.bit_length() + 7) // 8
        data = value.to_bytes(length, byteorder="big", signed=False)
        return data.decode("utf-8")
        
    def run_experiment(
        self,
        small_primes: tuple[int, int],
        big_primes: tuple[int, int],
        small_message: str,
        big_message: str,
        runs: int = 3,
        warm_up_runs: int = 1
    ) -> tuple[ExperimentSummary, ExperimentSummary]:
        for _ in range(warm_up_runs):
            self.run_trial(small_primes, small_message)
            self.run_trial(big_primes, big_message)
        
        small_results: list[TrialResult] = []
        big_results: list[TrialResult] = []
        for _ in range(runs):
            small_results.append(self.run_trial(small_primes, small_message))
            big_results.append(self.run_trial(big_primes, big_message))
            
        return self._avg_summary(small_results), self._avg_summary(big_results)
    