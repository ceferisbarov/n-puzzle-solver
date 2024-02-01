from copy import deepcopy

class State(object):
	"""
	This class represents a single state in our search path.
	It consists of a matrix, an ID, h_cost, g_cost, f_cost, and a parent.
	"""
	def __init__(self, matrix) -> None:
		self.matrix = matrix
		self.id = self.get_id()
		self.h_cost = self.count_inversions()
		self.g_cost = 0
		self.parent = None

	def set_f_cost(self, original_matrix):
		"""
		Set h_cost and g_cost. h_cost is equal to the number of inversions.
		g_cost is equal to the number of inversions to get to the original permutation.
		"""
		self.h_cost = self.count_inversions()

		original_flat = []
		for y in original_matrix:
			for x in y:
				original_flat.append(x)

		self_flat = []
		for y in self.matrix:
			for x in y:
				self_flat.append(x)

		i = 0
		g_cost = 0

		while(i < len(original_flat)):
			if original_flat[i] != self_flat[i]:
				wrong_id = self_flat.index(original_flat[i])
				if wrong_id < i:
					self_flat = self_flat[:wrong_id] + \
								[self_flat[i]] + \
								self_flat[wrong_id:i] + \
								self_flat[i+1:]
				else:
					self_flat = self_flat[:i] + \
								[self_flat[wrong_id]] + \
								self_flat[i:wrong_id] + \
								self_flat[wrong_id+1:]
					
				g_cost += (wrong_id - i)
				continue

			i += 1

		self.g_cost = g_cost
		
	def get_f_cost(self):
		"""
		Dynamically returns the f cost.
		"""
		return self.h_cost + self.g_cost
	
	def __eq__(self, other):
		"""
		Override equality operator.
		"""
		return self.id == other.id	

	def get_id(self):
		"""
		Returns a unique ID based on contents of the matrix.
		"""
		flat = [
			x
			for row in self.matrix
			for x in row
		]

		return "".join(map(str, flat))
	
	def count_inversions(self, ignore_zero=False):
		"""
		Returns the number of inversions in a given matrix.
		Adapted from:
		https://www.geeksforgeeks.org/check-instance-15-puzzle-solvable/
		"""
		n = len(self.matrix)
		flat = []
		for y in self.matrix:
			for x in y:
				flat.append(x)

		inv_count = 0
		for i in range(n * n - 1):
			for j in range(i + 1, n * n):
				if (flat[j] and flat[i] and flat[i] > flat[j]):
					inv_count += 1
				elif flat[i] == 0 and not ignore_zero:
					inv_count += 1
		
		return inv_count
	
	def get_empty_slot(self):
		"""
		Returns index (i, j) of the empty slot.
		"""
		n = len(self.matrix)
		for i in range(n):
			if 0 in self.matrix[i]:
				return i, self.matrix[i].index(0)

	def get_neighbors(self):
		"""
		Returns all traversable neighbors.
		"""
		n = len(self.matrix)
		i, j = self.get_empty_slot()
		neighbors = []

		north = deepcopy(self.matrix)
		east = deepcopy(self.matrix)
		west = deepcopy(self.matrix)
		south = deepcopy(self.matrix)
	
		if i - 1 >= 0:
			north[i][j], north[i-1][j] = north[i-1][j], north[i][j]
			neighbors.append(State(north))

		if j + 1 < n:
			east[i][j], east[i][j+1] = east[i][j+1], east[i][j]
			neighbors.append(State(east))

		if j - 1 >= 0:
			west[i][j], west[i][j-1] = west[i][j-1], west[i][j]
			neighbors.append(State(west))

		if i + 1 < n:
			south[i][j], south[i+1][j] = south[i+1][j], south[i][j]
			neighbors.append(State(south))

		return neighbors
	
	def is_solvable(self):
		"""
		Checks if the given matrix is a solvable n-puzzle.
		https://www.geeksforgeeks.org/check-instance-15-puzzle-solvable/
		"""
		num_inversions = self.count_inversions(ignore_zero=True)
		initial_inverse_row = len(self.matrix) - self.get_empty_slot()[0]

		if len(self.matrix) % 2 == 1:
			return num_inversions % 2 == 0

		if initial_inverse_row % 2 == 1:
			return num_inversions % 2 == 0 
		
		if initial_inverse_row % 2 == 0:
			return num_inversions % 2 == 1
		
		return False
