import time

def measure_time(func, n):
    """
    Executes func(n) and returns duration in seconds.
    """
    try:
        start = time.perf_counter()
        func(n)
        return time.perf_counter() - start
    except ValueError:
        return None # Caught safety error
    except RecursionError:
        return None
    except KeyboardInterrupt:
        return None
