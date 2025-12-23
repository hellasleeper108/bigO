import sys
import time
import random
import math
import itertools

# ==========================================
#  BIG O SANDBOX - EDUCATIONAL TOOL
# ==========================================
#
#  Welcome to the Big O Sandbox!
#  This program demonstrates how different algorithms grow in complexity.
#  
#  MODES:
#  1. Standard (Run without args): automated test of O(1) -> O(n^2).
#  2. Explain: Run with '--explain' to see definitions.
#  3. Custom: Run with '--custom' to test YOUR own function below.
#
# ==========================================

# --- CUSTOM USER SECTION ---
# Edit this function to test your own code's complexity!
# Try changing the logic and see if the analysis matches your guess.

USER_GUESS = "O(n)" # Guess your complexity: O(1), O(n), O(n^2), etc.

def custom_user_function(n):
    """
    A sandbox for you to experiment with.
    Currently: A simple loop (O(n)).
    """
    count = 0
    # Example: Single loop = O(n)
    for i in range(n):
        count += 1
    
    # Example: Nested loop = O(n^2)
    # for i in range(n):
    #     for j in range(n):
    #         count += 1
    return count

# ==========================================

EXPLANATIONS = {
    "O(1)": "Constant Time: The operation takes the same amount of time regardless of input size. Example: Accessing an array index.",
    "O(log n)": "Logarithmic Time: The time grows slowly as input increases. Doubling N adds only one unit of work. Example: Binary Search.",
    "O(n)": "Linear Time: The time grows directly proportional to input. Doubling N doubles the time. Example: Simple loop.",
    "O(n log n)": "Linearithmic Time: Common in efficient sorting algorithms. It's n operations, each taking log(n) time. Example: Merge Sort.",
    "O(n^2)": "Quadratic Time: Time grows with the square of the input. Doubling N quadruples the time. Example: Nested loops.",
    "O(2^n)": "Exponential Time: The runtime doubles with every single addition to N. Very scary. Example: Recursive Fibonacci.",
    "O(n!)": "Factorial Time: Grows insanely fast. Checks every possible permutation. The 'heat death of the universe' complexity."
}

def measure_time(func, n):
    """
    Runs func(n) and returns the execution time in seconds.
    We use perf_counter for high precision.
    """
    start = time.perf_counter()
    func(n)
    end = time.perf_counter()
    return end - start

# --- ALGORITHMS ---

def constant_time(n):
    """O(1): Always does 1 operation, ignored N."""
    return n + 1

def logarithmic_time(n):
    """O(log n): Cuts problem in half repeatedly."""
    count = 0
    while n > 1:
        n //= 2
        count += 1
    return count

def linear_time(n):
    """O(n): Iterates n times."""
    count = 0
    for i in range(n):
        count += 1
    return count

def linearithmic_time(n):
    """O(n log n): Runs log(n) work n times (simulated)."""
    count = 0
    # We simulate this by doing a loop of n, and an easy O(log n) op inside
    # (like resizing/copying, but math is cleaner here for pure CPU work)
    limit = n
    for i in range(n):
        temp = limit
        while temp > 1:
            temp //= 2
            count += 1
    return count

def quadratic_time(n):
    """O(n^2): Nested loops."""
    count = 0
    for i in range(n):
        for j in range(n):
            count += 1
    return count

def exponential_time_safe(n):
    """
    O(2^n) - Capped for safety in standard mode.
    Simulates recursion without the stack overflow risk for 'moderate' n.
    """
    # Actually running 2^n iterations
    count = 0
    target = 2**n
    # Check for sane limit before running
    if target > 50_000_000: # hard cap for auto-run
        return 0
    
    # We iterate target times
    for i in range(target):
        count += 1
    return count

# --- DANGER MODE ALGORITHMS ---

def danger_recursive_fib(n):
    """O(2^n): The classic recursive nightmare."""
    if n <= 1: return n
    return danger_recursive_fib(n-1) + danger_recursive_fib(n-2)

def danger_permutations(n):
    """O(n!): Generates all permutations of a range."""
    # itertools.permutations is highly optimized C, but it still has to generate n! items
    # We consume it to ensure work is done
    items = range(n)
    count = 0
    for p in itertools.permutations(items):
        count += 1
    return count

# --- VISUALIZATION ---

def draw_bar(val, max_val, width=30):
    """Returns a string of '#' proportional to val/max_val."""
    if max_val == 0: return ""
    
    ratio = val / max_val
    num_chars = int(ratio * width)
    
    # Ensure at least one char if value is non-zero but very small (unless logic dictates otherwise)
    if num_chars == 0 and val > 0:
        return "." # Tiny value indicator
    return "#" * num_chars

# --- CUSTOM ANALYSIS ---

def analyze_custom(func, guess_str):
    print(f"\n--- ANALYZING CUSTOM FUNCTION: {guess_str} ---")
    print("Disclaimer: This is empirical testing. OS noise, caching, and small N can skew results.")
    
    test_ns = [1000, 2000, 4000, 8000] # Adjust if function is very slow/fast
    
    # Pre-check speed with a small n to adjust range if needed
    t_start = time.perf_counter()
    func(500)
    if time.perf_counter() - t_start > 0.5:
        print("Function seems slow, reducing test range...")
        test_ns = [10, 20, 40, 80]
    
    print(f"{'N':<10} | {'Time (s)':<12} | {'Ratio (T(2n)/T(n))':<20}")
    print("-" * 50)
    
    prev_time = None
    ratios = []
    
    for n in test_ns:
        t = measure_time(func, n)
        
        ratio_str = "-"
        if prev_time is not None and prev_time > 0:
            ratio = t / prev_time
            ratios.append(ratio)
            ratio_str = f"{ratio:.2f}x"
        
        print(f"{n:<10} | {t:<12.6f} | {ratio_str}")
        prev_time = t
        
    print("-" * 50)
    
    if not ratios:
        return

    avg_ratio = sum(ratios) / len(ratios)
    print(f"Average Growth Ratio: ~{avg_ratio:.2f}x")
    
    # Theoretical mapping (doubling N)
    # O(1) -> 1x
    # O(log n) -> 1x (approx, log 2n = log n + 1)
    # O(n) -> 2x
    # O(n^2) -> 4x
    # O(2^n) -> Squaring the time (crazy high)
    
    if avg_ratio < 1.1:
        found = "O(1) or O(log n)"
    elif 1.5 <= avg_ratio <= 2.5:
        found = "O(n)"
    elif 3.5 <= avg_ratio <= 4.5:
        found = "O(n^2)"
    elif avg_ratio > 5:
        found = "O(2^n) or worse"
    else:
        found = "Unclear/Linearithmic"
        
    print(f"Based on this run, it behaves like: {found}")
    if guess_str in found or (guess_str == "O(n^2)" and "4.0" in str(avg_ratio)):
         print("Verdict: Your guess seems PLAUSIBLE.")
    else:
         print("Verdict: Data does not strongly support your guess (or N is too small).")

# --- MAIN ---

def run_standard_suite():
    suite = [
        ("O(1) Constant", constant_time, [100, 1000, 10000, 100000]),
        ("O(log n) Logarithmic", logarithmic_time, [100, 1000, 10000, 100000]),
        ("O(n) Linear", linear_time, [100, 1000, 10000, 100000]),
        ("O(n log n) Linearithmic", linearithmic_time, [100, 1000, 10000, 100000]),
        # Reduced N for quadratic to keep it snappy
        ("O(n^2) Quadratic", quadratic_time, [100, 500, 1000, 2000]),
        # Very small N for exponential simulation
        ("O(2^n) Exponential (Safe)", exponential_time_safe, [10, 15, 20, 22])
    ]

    print("\n=== RUNNING AUTOMATED BIG-O COMPLEXITY TEST ===")
    
    results_summary = []

    for name, func, n_values in suite:
        print(f"\n--- Testing {name} ---")
        print(f"{'N':<10} | {'Time (s)':<12} | {'Growth':<30}")
        print("-" * 55)
        
        times = []
        for n in n_values:
            t = measure_time(func, n)
            times.append(t)
        
        # Max time in this specific batch (for local scaling)
        max_t = max(times) if times else 0
        
        for n, t in zip(n_values, times):
            bar = draw_bar(t, max_t)
            print(f"{n:<10} | {t:<12.6f} | {bar}")
            
        # Quick educational blurb
        if "O(1)" in name:
            print("> Note: Time stays basically flat despite 1000x input size.")
        elif "O(n)" in name and "log" not in name:
            print("> Note: 10x input = ~10x time. Nice and predictable.")
        elif "O(n^2)" in name:
            print("> Note: Doubling input (1k to 2k) -> ~4x time. Validating squares!")
            
        results_summary.append((name, n_values[-1], times[-1]))

    # SUMMARY
    print("\n\n=== FINAL COMPARISON (At largest common reasonable N) ===")
    print("How long would they take if we gave them all the same heavy workload?")
    print("(Extrapolated/Estimated for slower ones based on behavior)")
    print(f"{'Algorithm':<25} | {'Behavior':<40}")
    print("-" * 65)
    for name, _, _ in results_summary:
        comment = EXPLANATIONS.get(name.split(" ")[0], "Complex complexity.")
        print(f"{name:<25} | {comment}")
    print("-" * 65)

def run_danger_mode():
    print("\n\n" + "!"*40)
    print("       WELCOME TO DANGER MODE")
    print("!"*40)
    print("Warning: These algorithms grow FAST. We are not protecting you here.")
    print("If it gets stuck, press Ctrl+C to bail out.\n")
    
    while True:
        print("Choose your poison:")
        print("1. Recursive Fibonacci O(2^n) - The elegant stack overflow-er")
        print("2. Permutation Generator O(n!) - The universe heater")
        print("3. Return to safety")
        
        choice = input("\nSelect (1-3): ").strip()
        
        if choice == '3':
            break
            
        func = None
        algo_name = ""
        
        if choice == '1':
            func = danger_recursive_fib
            algo_name = "O(2^n)"
            print("\nRecommended max N: 35 (Wait time: seconds to minutes)")
            print("N=40 might take a while. N=50? See you next year.")
        elif choice == '2':
            func = danger_permutations
            algo_name = "O(n!)"
            print("\nRecommended max N: 11 (Wait time: seconds)")
            print("N=12 is 12x slower. N=13 is 13x slower than that.")
            print("12! = 479,001,600 iterations.")
        else:
            continue
            
        try:
            n_val = int(input(f"Enter N for {algo_name}: "))
            print(f"Running {algo_name} with N={n_val}...")
            print("Calculating... (Ctrl+C to abort)")
            
            t = measure_time(func, n_val)
            print(f"\nSUCCESS! Finished in {t:.4f} seconds.")
            
            if t < 0.1:
                print("Too fast? Try a slightly larger N next time.")
            else:
                print("Phew. That was some heavy lifting.")
                
        except ValueError:
            print("That's not a number.")
        except KeyboardInterrupt:
            print("\n\nCowardly cancellation... good choice! That was taking too long.")
        except RecursionError:
            print("\n\nCRASH! Recursion depth exceeded. Python saved you from yourself.")
        
        print("-" * 30)

if __name__ == "__main__":
    if "--explain" in sys.argv:
        print("\n=== BIG O NOTATION EXPLAINED ===\n")
        for key, val in EXPLANATIONS.items():
            print(f"{key:<10} : {val}")
        sys.exit(0)
        
    if "--custom" in sys.argv:
        analyze_custom(custom_user_function, USER_GUESS)
        sys.exit(0)

    # Standard run
    run_standard_suite()
    
    # Optional danger mode prompt
    try:
        print("\n" + "="*50)
        user_input = input("Enter DANGER MODE to test O(n!)? (y/n): ").lower().strip()
        if user_input == 'y':
            run_danger_mode()
        else:
            print("\nExiting safely. Happy coding!")
    except KeyboardInterrupt:
        print("\nBye!")
