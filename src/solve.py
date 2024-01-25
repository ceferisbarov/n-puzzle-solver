import argparse
from datetime import datetime

from random_agent import RandomNPuzzleSolver

parser = argparse.ArgumentParser()
parser.add_argument("--input", help="Filepath of the input matrix.")
parser.add_argument("--output", help="Where to store the output.")
args = parser.parse_args()


start = datetime.now()
for i in range(100):
	print(i)
	s = RandomNPuzzleSolver(args.input, max_moves=10000000)
	s.solve()

end = datetime.now()

delta = end - start
print(delta.total_seconds())
