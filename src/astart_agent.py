from base_agent import BaseNPuzzleSolver
from state import State
from copy import deepcopy

class AStartAgent(BaseNPuzzleSolver):
	def __init__(self, filepath) -> None:
		super().__init__(filepath)
		self.hashtable = {self.state.id: self.state}
		self.open = [self.state.id]
		self.closed = []
		
	def solve(self):
		while(True):
			current_id = ""
			min_fscore = 10000
			for i in self.open:
				if self.hashtable[i].f_score < min_fscore:
					min_fscore = self.hashtable[i].f_score
					current_id = i

			self.closed.append(current_id)
			self.open.remove(current_id)

			current_object = self.hashtable[current_id]
			if current_object.f_score == 0:
				self.state = deepcopy(current_object)
				return
			
			for neighbor in current_object.get_neighbors():
				if any([neighbor.id == i for i in self.closed]):
					continue
				
				exists = False
				for i in self.open:
					i_object = self.hashtable[i]
					if neighbor == i_object and i_object.f_score > neighbor.f_score:
						i_object.f_score = neighbor.f_score
						i_object.parent = neighbor.id
						exists = True
						break

				if not exists:
					self.hashtable[neighbor.id] = neighbor
					self.open.append(neighbor.id)
