from copy import deepcopy
from utils import pprint, MIN_N, MAX_N
from state import State

class AStartAgent(object):
	"""
	This is an implementation of A* based N-puzzle agent.
	"""
	def __init__(self, filepath) -> None:
		self.state = self.read_input(filepath)
		assert self.state.is_solvable(), "This matrix has no solution!"

		self.hashtable = {self.state.id: self.state}
		self.open = [self.state.id]
		self.closed = []
		self.final_state_id = self.get_final_state_id()
	
	def read_input(self, filepath):
		"""
		Given a filepath:
		(1) parses contens of this file into a 2D list,
		(2) validates the content
		and returns it.
		"""
		with open(filepath, "r") as f:
			input_lines = f.readlines()

		n = len(input_lines)

		if n < MIN_N or n > MAX_N:
			raise ValueError("Invalid matrix size!")
		
		input_matrix = []

		for line in input_lines:
			values = list(map(int, line.split("\t")))
			input_matrix.append(values)

		return State(input_matrix)

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
				current_depth = self.get_depth(current_object)
				for i in self.open:
					i_object = self.hashtable[i]
					if neighbor.id == i_object.id and i_object.h_cost > neighbor.h_cost:
						i_object.set_f_cost()
						i_object.parent = current_id
						i_object.g_cost = current_depth + 1
						exists = True
						break

				if not exists:
					neighbor.set_f_cost()
					neighbor.parent = current_id
					self.hashtable[neighbor.id] = neighbor
					self.open.append(neighbor.id)

	def get_depth(self, state):
		depth = 0
		while(state.parent):
			depth += 1			
			state  = self.hashtable[state.parent]
		
		return depth

	def save_path(self, save_path):
		"""
		Returns the path from original to the final state.
		"""
		current_state = self.hashtable[self.final_state_id]
		i = 1
		with open(save_path, "w") as f:
			while(current_state.parent):
				save_string = f"state {i}\n"
				i += 1
				for line in current_state.matrix:
					save_string = save_string + "\t".join(map(str, line)) + "\n"
				
				save_string += "--------\n"
				f.write(save_string)
				
				current_state  = self.hashtable[current_state.parent]
