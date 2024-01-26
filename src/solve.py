import argparse
from datetime import datetime

from utils import pprint
from astart_agent import AStartAgent

parser = argparse.ArgumentParser()
parser.add_argument("--input", help="Filepath of the input matrix.")
parser.add_argument("--output", help="Where to store the output.")
args = parser.parse_args()


start = datetime.now()
for i in range(5):
	s = AStartAgent(args.input)
	s.solve()
	pprint(s.state.matrix)

end = datetime.now()

delta = end - start
print(delta.total_seconds())
