import matplotlib.pyplot as plt

def plot_external(algorithms, n_range, results):
    """
    Opens a standard Matplotlib window with the given results.
    
    algorithms: List of (name, func)
    n_range: range object
    results: Dictionary { algorithm_name: [times...] }
    """
    try:
        plt.figure(figsize=(10, 6))
        x = list(n_range)
        
        for name, times in results.items():
            # Filter out incompatible lengths or None types just in case
            if len(times) != len(x):
                continue
            
            # Matplotlib handles None naturally (breaks line), but let's be safe
            safe_times = [t if t is not None else float('nan') for t in times]
            
            plt.plot(x, safe_times, marker='o', label=name)
        
        plt.title("Runtime Complexity Comparison")
        plt.xlabel("Input Size (N)")
        plt.ylabel("Time (seconds)")
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend()
        
        # Show blocking or non-blocking?
        # Ideally non-blocking so TUI doesn't freeze effectively
        # But 'block=False' requires event loop handling.
        # Simple 'show()' blocks the process.
        print("Opening external chart...")
        plt.show()
    except Exception as e:
        print(f"Error opening external plot: {e}")
