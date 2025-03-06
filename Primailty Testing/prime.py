import random
import re
import threading

class GlobalState:
    def __init__(self):
        self.composite_count = 0
        self.lock = threading.Lock()

def miller_rabin_iteration(n, d, r):
    a = random.randrange(2, n - 1)
    x = pow(a, d, n)
    if x == 1 or x == n - 1:
        return True
    for _ in range(r - 1):
        x = (x * x) % n
        if x == n - 1:
            return True
    return False

def test_primality_iterative(index, n, results, global_state, max_iterations=10000):
    # Precompute factors: write n - 1 as 2^r * d with d odd.
    r = 0
    d = n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for iteration in range(max_iterations):
        # Check if two composites are already found.
        with global_state.lock:
            if global_state.composite_count >= 2:
                results[index] = "Prime"
                print(f"Thread for input {index + 1} stopping early (assumed Prime).")
                return

        # Perform one Miller-Rabin iteration.
        if not miller_rabin_iteration(n, d, r):
            results[index] = "Composite"
            with global_state.lock:
                global_state.composite_count += 1
            print(f"Thread for input {index + 1} determined Composite in iteration {iteration + 1}.")
            return

    # If all iterations pass, declare the number probably prime.
    results[index] = "Prime"
    print(f"Thread for input {index + 1} completed {max_iterations} iterations (assumed Prime).")

def parse_binary_from_file(filename):
    with open(filename, 'r') as f:
        content = f.read()
    match = re.search(r'0b([01]+)', content)
    if match:
        return match.group(1)
    else:
        print(f"No binary pattern found in file {filename}.")
        return None

def main():
    # Ask the user for three filenames.
    filenames = []
    for i in range(1, 4):
        filename = input(f"Enter the filename for input {i}: ").strip()
        filenames.append(filename)

    # Parse binary numbers from the files.
    binary_numbers = []
    for filename in filenames:
        binary_str = parse_binary_from_file(filename)
        if binary_str is None:
            return  # Exit if any file fails to provide a binary number.
        binary_numbers.append(binary_str)

    # Convert binary strings to integers.
    numbers = [int(b, 2) for b in binary_numbers]

    # Create a shared results list.
    results = [None] * 3

    # Create a global state to track how many composites have been found.
    global_state = GlobalState()

    # Create threads for each number's primality test.
    test_threads = []
    for index, num in enumerate(numbers):
        t = threading.Thread(target=test_primality_iterative, args=(index, num, results, global_state, 100))
        test_threads.append(t)
        t.start()

    # Wait for all primality test threads to complete.
    for t in test_threads:
        t.join()

    # Print final results and write them to results.txt.
    final_output = "\nFinal Results:\n"
    for i, res in enumerate(results, start=1):
        final_output += f"Input {i}: {res}\n"
    print(final_output)

    with open("results.txt", "w") as out_file:
        out_file.write(final_output)

if __name__ == "__main__":
    main()
