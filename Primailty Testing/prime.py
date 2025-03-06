'''The task at hand is taking a massiviely large prime number along with 2 other numbers that
are not prime what i have to do is figure out which of those numbers are not prime while trying to
figure out if the other numbers are prime

Ok so lets start brain storming ideas, for of we need to make sure it odd so we can check the first bit
and see if it is zero if the bit is zero that the number is automaticlaly not prime as it means that the
number can be dividied by 2


Honestly first lets set up so that the prgoram takes files and pasres the files taking the binary after the
0b, then it takes the inputs. It will ask for 1 then 2 then 3. Then it will start the proccess, i will need
it to be efficent but will also add some sign that the program is working for right now it will
probaly be a thread of some sort that keep on prinint the time taken or just a print statment so i know
the program is running to some exent
'''

# Program to test primality of large binary numbers using the Miller-Rabin test.
# The program reads three binary numbers (each a string of '0's and '1's), converts them to decimal,
# and then checks if they are prime or composite.
#
# Author: [Your Name]
# Date: [Today's Date]

import random
import re
import threading

class GlobalState:
    def __init__(self):
        self.composite_count = 0
        self.lock = threading.Lock()

def miller_rabin_iteration(n, d, r):
    """
    Performs one iteration of the Miller-Rabin test for n.
    Precomputed: n - 1 = 2^r * d (with d odd).
    Returns True if the iteration passes (i.e. does NOT witness compositeness),
    or False if a witness for compositeness is found.
    """
    a = random.randrange(2, n - 1)
    x = pow(a, d, n)
    if x == 1 or x == n - 1:
        return True
    for _ in range(r - 1):
        x = (x * x) % n
        if x == n - 1:
            return True
    return False

def test_primality_iterative(index, n, results, global_state, max_iterations=100):
    """
    Tests number n for primality using up to max_iterations of the Miller-Rabin test.
    If at any point two composites are already found (global_state.composite_count >= 2),
    the thread stops early and declares its number prime.
    Once a witness to compositeness is found, the thread stops and sets its result to "Composite".
    """
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
    """
    Opens the file, reads its content, and extracts the binary number (digits after '0b').
    Returns the binary string or None if not found.
    """
    try:
        with open(filename, 'r') as f:
            content = f.read()
        match = re.search(r'0b([01]+)', content)
        if match:
            return match.group(1)
        else:
            print(f"No binary pattern found in file {filename}.")
            return None
    except Exception as e:
        print(f"Error reading file {filename}: {e}")
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
