import argparse
import random

parser = argparse.ArgumentParser()
parser.add_argument("--size", help="Size of the N-puzzle.")
parser.add_argument("--output", help="Where to store the output.")
args = parser.parse_args()

def generate_puzzle(n):
    numbers = list(range(1, n**2))
    random.shuffle(numbers)
    puzzle = [numbers[i:i+n] for i in range(0, len(numbers), n)]
    puzzle[-1].append(0)  # Adding 0 as the empty space
    return puzzle

def print_puzzle(puzzle):
    for row in puzzle:
        print(" ".join(map(lambda x: f"{x:2}" if x != 0 else "  ", row)))

if __name__ == "__main__":
    puzzle = generate_puzzle(int(args.size))
    save_string = ""
    for line in puzzle:
        save_string = save_string + "\t".join(map(str, line)) + "\n"
    with open(args.output, "w") as f:   
        f.write(save_string)
