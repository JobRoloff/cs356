from experiment_manager import ExperimentManager

def max_message_bytes_for_prime_bits(prime_bits: int) -> int:
    # n is ~2*prime_bits; bytes = bits/8
    # subtract a little headroom
    return max(1, (2 * prime_bits // 8) - 2)



def main():
    experiment_manager: ExperimentManager = ExperimentManager()
    
    prime_bits_list = [128, 256, 512, 1024]
    message_bytes_list = [8, 32,64,96]
    for prime_bits in prime_bits_list:
        # prime1 = generate_prime(prime_bits)
        # prime2 = generate_prime(prime_bits)
        # primes = (prime1, prime2)
        cap = max_message_bytes_for_prime_bits(prime_bits)
        for message_bytes in message_bytes_list:
            actual_length = min(message_bytes, cap)
            message = "A" * actual_length
            experiment_results = experiment_manager.run_experiment_by_bits(prime_bits ,message)
            print(
                f"Prime Bits : {prime_bits}, Message Bytes(requested) {message_bytes}"
                f"Message Bytes (used)={actual_length} -> {experiment_results}")
    

if __name__ == "__main__":
    main()