from .library import (
    constant_time,
    logarithmic_time,
    linear_time,
    linearithmic_time,
    quadratic_time,
    exponential_time_safe,
    factorial_time
)

ALGORITHMS = {
    "1": ("O(1)", constant_time),
    "2": ("O(log n)", logarithmic_time),
    "3": ("O(n)", linear_time),
    "4": ("O(n log n)", linearithmic_time),
    "5": ("O(n^2)", quadratic_time),
    "6": ("O(2^n)", exponential_time_safe),
    "7": ("O(n!)", factorial_time)
}
