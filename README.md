# Big O Sandbox

A single-file Python interactive educational tool for exploring time complexities.

![Big O Growth](https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Comparison_computational_complexity.svg/600px-Comparison_computational_complexity.svg.png)
*(Image concept: Visualizing growth)*

## Features

- **Automated Complexity Test**: Run without arguments to see a comparative table of algorithms from O(1) to O(2ⁿ) with ASCII visualization.
- **Danger Mode**: Opt-in to test heavy O(n!) and O(2ⁿ) algorithms (with safeguards... somewhat).
- **Explanations**: Build-in dictionary of Big-O definitions.
- **Custom Analysis**: Write your own function in the file and let the tool guess its complexity.

## Usage

### 1. Standard Run
Tests O(1) through O(n²) automatically.
```bash
python big_o_sandbox.py
```

### 2. See Explanations
```bash
python big_o_sandbox.py --explain
```

### 3. Test Your Own Code
Edit `custom_user_function` inside `big_o_sandbox.py`, then run:
```bash
python big_o_sandbox.py --custom
```

## Requirements
- Python 3.x
- No external libraries required (uses `time`, `random`, `math`, `itertools`, `sys`).

## License
MIT
