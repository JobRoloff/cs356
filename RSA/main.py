from experiment_manager import ExperimentManager

def main():
    experiment_manager: ExperimentManager = ExperimentManager()
    
    small_primes = (101, 103)
    big_primes = (7793, 3659)
    
    small_message = "Hi"
    big_message = "Job prays to someday become a software engineer"


    
    experiemnt_results = experiment_manager.run_experiment(small_primes, big_primes, small_message, big_message)
    
    print(experiemnt_results)
    

if __name__ == "__main__":
    main()