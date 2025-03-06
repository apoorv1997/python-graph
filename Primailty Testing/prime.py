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

def is_probable_prime(n, k=10):
    """
    Miller-Rabin primality test.
    Returns True if n is probably prime, otherwise False (composite).

    Steps:
      1. Check trivial cases (n < 2, even numbers, etc.).
      2. Write n-1 as 2^r * d with d odd.
      3. For k iterations, pick a random base a and test using modular exponentiation.
         - Compute x = a^d mod n.
         - If x is not 1 or n-1, square x repeatedly to see if it becomes n-1.
         - If not, n is composite.
      4. If all rounds pass, n is declared probably prime.
    """
    if n % 2 == 0:
        return False

    # Write n-1 as 2^r * d with d odd.
    r = 0
    d = n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Perform k rounds of testing.
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue

        composite_found = True
        for _ in range(r - 1):
            x = (x * x) % n
            if x == n - 1:
                composite_found = False
                break

        if composite_found:
            return False
    return True

def parse_binary_from_file(filename):
    """
    Opens the given file and searches for a binary number pattern after '0b'.
    It uses a regular expression to find the first occurrence of '0b' followed by binary digits.
    Returns the binary digits as a string, or None if no valid binary is found.
    """
    with open(filename, 'r') as f:
        content = f.read()
        # Search for a binary pattern like: 0b101010...
    match = re.search(r'0b([01]+)', content)
    if match:
        return match.group(1)
    else:
        print(f"No binary pattern found in file {filename}.")
        return None

def main():
    # Ask the user for three filenames, one at a time.
    filenames = []
    for i in range(1, 4):
        filename = input(f"Enter the filename for input {i}: ").strip()
        filenames.append(filename)

    # Parse binary numbers from each file.
    binary_numbers = []
    for filename in filenames:
        binary_str = parse_binary_from_file(filename)
        if binary_str is None:
            return
        binary_numbers.append(binary_str)

    # Convert the binary strings to integers.
    numbers = [int(b, 2) for b in binary_numbers]

    # Process each number and test for primality.
    results = []
    for index, num in enumerate(numbers, start=1):
        print(f"\nProcessing number {index}...")
        result = "Prime" if is_probable_prime(num) else "Composite"
        results.append(result)

    # Print final results.
    print("\nFinal Results:")
    for i, res in enumerate(results, start=1):
        print(f"Input {i}: {res}")

if __name__ == "__main__":
    main()
