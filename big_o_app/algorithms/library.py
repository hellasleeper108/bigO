import itertools
from ..config import AppState, MAX_SAFE_N_2POW, MAX_SAFE_N_FACT

def constant_time(n): return n + 1

def logarithmic_time(n):
    count = 0
    while n > 1:
        n //= 2
        count += 1
    return count

def linear_time(n):
    count = 0
    for i in range(n): count += 1
    return count

def linearithmic_time(n):
    count = 0
    limit = n
    for i in range(n):
        temp = limit
        while temp > 1:
            temp //= 2
            count += 1
    return count

def quadratic_time(n):
    count = 0
    for i in range(n):
        for j in range(n): count += 1
    return count

def exponential_time_safe(n):
    if AppState.safety_enabled and n > MAX_SAFE_N_2POW:
        raise ValueError(f"Safety limit (N={MAX_SAFE_N_2POW}) exceeded for O(2^n).")
    
    count = 0
    target = 2**n 
    if target > 100_000_000: return 0 
    for i in range(target): count += 1
    return count

def factorial_time(n):
    if AppState.safety_enabled and n > MAX_SAFE_N_FACT:
         raise ValueError(f"Safety limit (N={MAX_SAFE_N_FACT}) exceeded for O(n!).")
    
    count = 0
    for p in itertools.permutations(range(n)):
        count += 1
    return count
