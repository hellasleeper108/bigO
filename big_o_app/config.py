# Configuration Constants

# Limits
MAX_SAFE_N_2POW = 30
MAX_SAFE_N_FACT = 10

# Mutable Runtime State
class AppState:
    safety_enabled = True
    mode = "TEACHING" # TEACHING | CHAOS
    delay = 0.1       # Seconds to sleep between steps in Teaching mode

EXPLANATIONS = {
    "O(1)": "Constant Time: The operation takes the same amount of time regardless of input size. Gold standard.",
    "O(log n)": "Logarithmic Time: Grows slowly. Doubling N adds a tiny constant amount of work. Excellent.",
    "O(n)": "Linear Time: Growth is directly proportional to input. Fair and predictable.",
    "O(n log n)": "Linearithmic Time: Slightly steeper than linear. Standard for good sorting algorithms.",
    "O(n^2)": "Quadratic Time: Doubling N quadruples the time. Avoid for large datasets.",
    "O(2^n)": "Exponential Time: The runtime doubles with every single addition to N. Impractical for N > 40.",
    "O(n!)": "Factorial Time: Checks every permutation. Impractical for N > 12."
}
