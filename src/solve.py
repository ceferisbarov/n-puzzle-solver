import argparse

from astart_agent import AStartAgent

parser = argparse.ArgumentParser()
parser.add_argument("--input", help="Filepath of the input matrix.")
parser.add_argument("--output", help="Where to store the output.")
args = parser.parse_args()


agent = AStartAgent(args.input)
agent.solve()
if args.output:
	agent.save_path(args.output)
