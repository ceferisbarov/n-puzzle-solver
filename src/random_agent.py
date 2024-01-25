import random
from base_agent import BaseNPuzzleSolver

class RandomNPuzzleSolver(BaseNPuzzleSolver):
	def __init__(self, filepath, max_moves) -> None:
		super().__init__(filepath)
		self.max_moves = max_moves

	def solve(self):
		num_moves = 0
		while(not self.solved and num_moves <= self.max_moves):
			try:
				r = random.choice([1,2,3,4])
				if r == 1:
					self.swap_north()
				elif r == 2:
					self.swap_east()
				elif r == 3:
					self.swap_west()
				else:
					self.swap_south()

				num_moves += 1
				self.solved = self.is_solved()

			except:
				continue
