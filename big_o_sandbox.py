import sys
import time
import random
import math
import itertools
import os

# Try to import curses
try:
    import curses
    CURSES_AVAILABLE = True
except ImportError:
    CURSES_AVAILABLE = False

# ==========================================
#  BIG O SANDBOX - EDUCATIONAL TOOL V2
# ==========================================
#
#  Features:
#  - Interactive Menu & Validation
#  - Comparison Mode (Side-by-Side)
#  - Step-Through Mode (Pause & Analyze)
#  - ASCII & Curses Visualization
#  - Safety Rails for Exponential/Factorial
#
# ==========================================

# --- CUSTOM USER SECTION ---
# Edit this function to test your own code's complexity!
USER_GUESS = "O(n)" 

def custom_user_function(n):
    """
    A sandbox for you to experiment with.
    Currently: A simple loop (O(n)).
    """
    count = 0
    for i in range(n):
        count += 1
    return count

# ==========================================

CONFIG = {
    "safety_enabled": True,
    "max_safe_n_2pow": 30, # Safe limit for O(2^n) if safety is on
    "max_safe_n_fact": 10, # Safe limit for O(n!) if safety is on
}

EXPLANATIONS = {
    "O(1)": "Constant Time: The operation takes the same amount of time regardless of input size. Gold standard.",
    "O(log n)": "Logarithmic Time: Grows slowly. Doubling N adds a tiny constant amount of work. Excellent.",
    "O(n)": "Linear Time: Growth is directly proportional to input. Fair and predictable.",
    "O(n log n)": "Linearithmic Time: Slightly steeper than linear. Standard for good sorting algorithms.",
    "O(n^2)": "Quadratic Time: Doubling N quadruples the time. Avoid for large datasets.",
    "O(2^n)": "Exponential Time: The runtime doubles with every single addition to N. Impractical for N > 40.",
    "O(n!)": "Factorial Time: Checks every permutation. Impractical for N > 12."
}

# --- ALGORITHMS ---

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
def exponential_time_safe(n): # Helper to simulate work without stack depth issues
    if CONFIG["safety_enabled"] and n > CONFIG["max_safe_n_2pow"]:
        raise ValueError(f"Safety limits prevent running O(2^n) with N={n}. Max safe N is {CONFIG['max_safe_n_2pow']}.")
    count = 0
    target = 2**n 
    # Hard cap to prevent freezing even if safety is somehow bypassed or high
    if target > 100_000_000: return 0 
    for i in range(target): count += 1
    return count
def factorial_time(n):
    if CONFIG["safety_enabled"] and n > CONFIG["max_safe_n_fact"]:
         raise ValueError(f"Safety limits prevent running O(n!) with N={n}. Max safe N is {CONFIG['max_safe_n_fact']}.")
    count = 0
    # Simulated work: permutations grow as n!
    # We use a smaller loop to simulate the 'cost' if n is huge, but for n<=12 actual perms is fine
    # For instructional honesty, we run actual perms if small, else error
    for p in itertools.permutations(range(n)):
        count += 1
    return count

ALGORITHMS = {
    "1": ("O(1)", constant_time),
    "2": ("O(log n)", logarithmic_time),
    "3": ("O(n)", linear_time),
    "4": ("O(n log n)", linearithmic_time),
    "5": ("O(n^2)", quadratic_time),
    "6": ("O(2^n)", exponential_time_safe),
    "7": ("O(n!)", factorial_time)
}

# --- HELPER FUNCTIONS ---

def measure_time(func, n):
    try:
        start = time.perf_counter()
        func(n)
        return time.perf_counter() - start
    except ValueError as e:
        print(f"\n[!] SKIPPED: {e}")
        return None
    except RecursionError:
        print("\n[!] CRASH: Recursion limit reached.")
        return None
    except KeyboardInterrupt:
        print("\n[!] ABORTED by user.")
        return None

def draw_bar(val, max_val, width=40, char="#"):
    if max_val == 0 or val is None: return ""
    ratio = val / max_val
    num_chars = int(ratio * width)
    if num_chars == 0 and val > 0: return "." 
    return char * num_chars

def get_valid_int(prompt, min_val=0, max_val=float('inf')):
    while True:
        try:
            val = input(prompt).strip()
            if not val: continue 
            val = int(val)
            if min_val <= val <= max_val:
                return val
            print(f"Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

def select_algorithms():
    print("\nAvailable Algorithms:")
    for k, v in ALGORITHMS.items():
        print(f"[{k}] {v[0]}")
    print("[A] All Safe (1-5)")
    
    choice = input("Select algorithms (comma separated, e.g., '1,3') or 'A': ").strip().lower()
    selected = []
    
    if choice == 'a':
        return [ALGORITHMS[k] for k in ["1","2","3","4","5"]]
    
    parts = choice.split(',')
    for p in parts:
        p = p.strip()
        if p in ALGORITHMS:
            selected.append(ALGORITHMS[p])
    
    if not selected:
        print("No valid selection. Defaulting to O(n).")
        return [ALGORITHMS["3"]]
    return selected

def configure_range():
    print("\n--- Configure Input Range ---")
    start = get_valid_int("Start N (e.g. 100): ", 1)
    end = get_valid_int(f"End N (must be > {start}): ", start + 1)
    step = get_valid_int("Step size: ", 1)
    return range(start, end + 1, step)

# --- VISUALIZATION & MODES ---

def run_batch_test(algorithms, n_range, step_through=False):
    print(f"\n{'='*60}")
    print(f"{'BATCH TEST':^60}")
    print(f"{'='*60}")
    
    # Store results: results[alg_name] = [(n, time), ...]
    results = {alg[0]: [] for alg in algorithms}
    
    # Pre-calculate max time for scaling if NOT stepping through (for consistent chart)
    # If stepping through, we might scale locally or just let it flow.
    # For simplicity, we'll scale per row or keep a running max.
    
    global_max_time = 0.000001
    
    header = f"{'N':<8} | {'Algorithm':<12} | {'Time (s)':<10} | {'Growth Visualization'}"
    print(header)
    print("-" * len(header))

    prev_times = {alg[0]: None for alg in algorithms}

    for n in n_range:
        current_batch_times = []
        
        for name, func in algorithms:
            t = measure_time(func, n)
            if t is not None:
                results[name].append((n, t))
                current_batch_times.append((name, t))
                if t > global_max_time: global_max_time = t
            else:
                current_batch_times.append((name, None))

        # Dynamic scaling for this batch? 
        # Or simple linear scaling based on current max makes tiny bars visible early on.
        batch_max = max((t for _, t in current_batch_times if t is not None), default=0)
        if batch_max == 0: batch_max = 0.000001
        
        for name, t in current_batch_times:
            if t is None:
                bar = "SKIPPED"
                t_str = "---"
            else:
                bar = draw_bar(t, batch_max, width=25)
                t_str = f"{t:.6f}"
            
            print(f"{n:<8} | {name:<12} | {t_str:<10} | {bar}")
            
            # Step-through analysis
            if step_through and t is not None:
                prev = prev_times[name]
                if prev is not None and prev > 0:
                    growth = t / prev
                    if growth > 1.2:
                        print(f"       > {name} grew {growth:.1f}x")
        
        print("-" * len(header))
        
        # Update prev times
        for name, t in current_batch_times:
             if t is not None: prev_times[name] = t
             
        if step_through:
            input("\n[Paused] Press Enter to continue to next N...")
            print("-" * len(header))

    return results

def run_comparison_mode():
    print("\n--- Comparison Mode ---")
    print("Select strictly 2 algorithms to fight.")
    algs = select_algorithms()
    if len(algs) < 2:
        print("Need at least 2 for comparison!")
        return

    n_range = configure_range()
    
    print(f"\n{'N':<8} | {algs[0][0]:<12} | {algs[1][0]:<12} | {'Ratio (A/B)':<12} | {'Trend'}")
    print("-" * 65)
    
    for n in n_range:
        t1 = measure_time(algs[0][1], n)
        t2 = measure_time(algs[1][1], n)
        
        if t1 is None or t2 is None:
            print(f"{n:<8} | {'xxx':<12} | {'xxx':<12} | FAILED")
            continue
            
        ratio = t1 / t2 if t2 > 0 else 0
        
        trend = "Same"
        if ratio > 5: trend = f"{algs[0][0]} slower"
        elif ratio < 0.2: trend = f"{algs[1][0]} slower"
        elif ratio > 1.5: trend = "A > B"
        elif ratio < 0.7: trend = "B > A"
        
        print(f"{n:<8} | {t1:<12.5f} | {t2:<12.5f} | {ratio:<12.2f} | {trend}")

    print("\nAnalysis:")
    name1, name2 = algs[0][0], algs[1][0]
    print(f"Comparing {name1} vs {name2}:")
    if "O(n^2)" in name1 and "O(n)" in name2:
        print(f"> {name1} loses badly as N grows because it does N times more work.")
    elif "O(log n)" in name1 or "O(log n)" in name2:
         print(f"> The Log algorithm is vastly superior for large N.")
    elif "!" in name1 or "!" in name2:
         print("> Factorial is just unreasonable.")
    else:
         print("> Check the ratio column. If it stays constant, they represent the same complexity class.")

def run_curses_mode():
    if not CURSES_AVAILABLE:
        print("\n[!] Error: 'curses' module not available (Common on Windows without 'windows-curses').")
        print("Falling back to standard mode.")
        return

    def curses_main(stdscr):
        curses.curs_set(0)
        stdscr.nodelay(0)
        stdscr.clear()
        
        # Setup colors
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        
        # Select algorithms (hardcoded for demo simplicity in curses)
        demo_algs = [ALGORITHMS["3"], ALGORITHMS["5"], ALGORITHMS["2"]] # n, n^2, log n
        
        n = 100
        max_y, max_x = stdscr.getmaxyx()
        
        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "Big O Curses Viz (Press 'n' for next step, 'q' to quit)", curses.A_BOLD)
            
            row = 2
            max_time_in_step = 0
            results = []
            
            for name, func in demo_algs:
                t = measure_time(func, n)
                if t is None: t = 0
                results.append((name, t))
                if t > max_time_in_step: max_time_in_step = t
            
            for name, t in results:
                bar_len = int((t / (max_time_in_step + 0.00001)) * (max_x - 30))
                color = curses.color_pair(1)
                if t > 0.05: color = curses.color_pair(2)
                if t > 0.5: color = curses.color_pair(3)
                
                stdscr.addstr(row, 0, f"{name:<10} | {t:.5f}s | ", curses.A_NORMAL)
                stdscr.addstr(row, 25, "#" * bar_len, color)
                row += 2
                
            stdscr.addstr(row+2, 0, f"Current N: {n}")
            stdscr.refresh()
            
            key = stdscr.getch()
            if key == ord('q'):
                break
            elif key == ord('n'):
                n += 100
                if n > 2000: n += 500 # Skip faster later
    
    curses.wrapper(curses_main)

def print_final_summary(results):
    if not results: return
    print("\n\n" + "="*50)
    print(f"{'FINAL RANKING SUMMARY':^50}")
    print("="*50)
    print("Ranking algorithms based on their behavior at max N:\n")
    
    # Flatten results to find end-state
    # results format: {'O(n)': [(10, 0.01), (20, 0.02)], ...}
    
    final_stats = []
    for name, data in results.items():
        if not data: continue
        last_n, last_t = data[-1]
        final_stats.append((name, last_t, last_n))
        
    # Sort by time asc
    final_stats.sort(key=lambda x: x[1])
    
    for rank, (name, t, n) in enumerate(final_stats, 1):
        status = "Unknown"
        if t < 0.001: status = "Instant (Perfect)"
        elif t < 0.1: status = "Fast (Good)"
        elif t < 1.0: status = "Slugish (Careful)"
        else: status = "Impractical (Bad)"
        
        # Judgment
        judgment = ""
        if "O(n!)" in name: judgment = "- It's a miracle this finished."
        elif "O(2^n)" in name: judgment = "- Don't use this in production."
        elif "O(n^2)" in name and t > 0.5: judgment = "- Does not scale well."
        
        print(f"{rank}. {name:<12}: {t:.5f}s (at N={n}) [{status}] {judgment}")
        
    print("\nTakeaway:")
    slowest = final_stats[-1][0]
    print(f" Avoid {slowest} if you value your free time.")

# --- MAIN APP ---

def main_menu():
    while True:
        print("\n" + "="*40)
        print(" BIG O SANDBOX - MAIN MENU")
        print("="*40)
        print(f"Safety Limits: {'ON' if CONFIG['safety_enabled'] else 'OFF (Dangerous)'}")
        print("1. Quick Standard Test (Automated)")
        print("2. Custom Batch Test (Select Algs & Range)")
        print("3. Comparison Mode (A vs B)")
        print("4. Step-Through Mode (Pause & Learn)")
        print(f"5. Toggle Safety Limits")
        print("6. Curses Visualization Mode")
        print("7. Explain Big-O Definitions")
        print("8. Run Custom User Function")
        print("9. Exit")
        
        choice = input("\nSelect option: ").strip()
        
        if choice == '1':
            # Standard suite
            algs = [ALGORITHMS["1"], ALGORITHMS["2"], ALGORITHMS["3"], ALGORITHMS["5"]]
            results = run_batch_test(algs, [100, 500, 1000, 2000])
            print_final_summary(results)
            
        elif choice == '2':
            algs = select_algorithms()
            rng = configure_range()
            results = run_batch_test(algs, rng)
            print_final_summary(results)
            
        elif choice == '3':
            run_comparison_mode()
            
        elif choice == '4':
            algs = select_algorithms()
            rng = configure_range()
            run_batch_test(algs, rng, step_through=True)
            
        elif choice == '5':
            CONFIG["safety_enabled"] = not CONFIG["safety_enabled"]
            print(f"\n>> Safety is now {'ON' if CONFIG['safety_enabled'] else 'OFF'}.")
            
        elif choice == '6':
            run_curses_mode()
            
        elif choice == '7':
            print("\n=== DEFINITIONS ===")
            for k, v in EXPLANATIONS.items():
                print(f"{k:<10}: {v}")
                
        elif choice == '8':
            # Legacy custom function wrapper
            import inspect
            print("\nAnalyzing custom_user_function code...")
            print(inspect.getsource(custom_user_function))
            print("Running legacy analysis tool...")
            # Inline the old analysis logic roughly or simpler version
            n_vals = [1000, 2000, 4000]
            prev = None
            print(f"{'N':<10} | {'Time':<10} | {'Ratio'}")
            for n in n_vals:
                t = measure_time(custom_user_function, n)
                ratio_str = f"{(t/prev):.2f}x" if prev and prev > 0 else "-"
                print(f"{n:<10} | {t:.5f}s   | {ratio_str}")
                prev = t
                
        elif choice == '9':
            print("Exiting.")
            sys.exit(0)
            
        else:
            print("Invalid option.")

if __name__ == "__main__":
    # Check for CLI args from original legacy version to not break workflow if user used args
    if "--curses" in sys.argv:
        run_curses_mode()
        sys.exit(0)
    elif "--explain" in sys.argv:
        print("\n=== DEFINITIONS ===")
        for k, v in EXPLANATIONS.items():
             print(f"{k:<10}: {v}")
        sys.exit(0)
    
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nGood bye!")
