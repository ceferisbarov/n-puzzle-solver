from base_agent import BaseNPuzzleSolver
from copy import deepcopy
from utils import pprint

class AStartAgent(BaseNPuzzleSolver):
	"""
	This is an implementation of A* based N-puzzle agent.
	"""
	def __init__(self, filepath) -> None:
		super().__init__(filepath)
		self.hashtable = {self.state.id: self.state}
		self.open = [self.state.id]
		self.closed = []
		self.final_state_id = self.get_final_state_id()
	
	def get_final_state_id(self):
		"""
		Create the desired final state id.
		"""
		n = len(self.state.matrix)

		matrix = [i+1 for i in range(n*n)]
		matrix[-1] = 0

		return "".join(map(str, matrix))
	
	def solve(self):
		"""
		Traverses the path with A* star algorithm.
		If succesfull, updates the state. Otherwise, does nothing.
		"""
		# IMPORTANT
		# FINISH WHEN GOAL IS DEQUEUED
		# NOT WHEN IT IS ENQUEUED

		# UPDATE THE F SCORE
		# https://algorithmsinsight.wordpress.com/graph-theory-2/a-star-in-general/implementing-a-star-to-solve-n-puzzle/
		
		while(True):
			current_id = self.open[0]
			min_f_cost = self.hashtable[current_id].get_f_cost()
			for i in self.open:
				if self.hashtable[i].get_f_cost() <= min_f_cost:
					min_f_cost = self.hashtable[i].get_f_cost()
					current_id = i

			self.closed.append(current_id)
			self.open.remove(current_id)
			current_object = self.hashtable[current_id]
			if current_object.h_cost == 0:
				pprint(current_object.matrix)
				self.state = deepcopy(current_object)
				return
			
			for neighbor in current_object.get_neighbors():
				if any([neighbor.id == i for i in self.closed]):
					continue
				
				exists = False
				for i in self.open:
					i_object = self.hashtable[i]
					if neighbor == i_object and i_object.h_cost > neighbor.h_cost:
						i_object.set_f_cost(self.state.matrix)
						i_object.parent = current_id
						exists = True
						break

				if not exists:
					neighbor.set_f_cost(self.state.matrix)
					neighbor.parent = current_id
					self.hashtable[neighbor.id] = neighbor
					self.open.append(neighbor.id)

	def get_path(self):
		"""
		Returns the path from original to the final state.
		"""
		current_state = self.hashtable[self.final_state_id]
		while(current_state.parent):
			pprint(current_state.matrix)
			current_state  = self.hashtable[current_state.parent]
