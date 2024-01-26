from copy import deepcopy

class State(object):
	def __init__(self, matrix) -> None:
		self.matrix = matrix
		self.id = self.get_id()
		self.f_score = self.count_inversions()
		self.g_score = None
		self.parent = None

	def get_id(self):
		flat = [
			x
			for row in self.matrix
			for x in row
		]

		return "".join(map(str, flat))
	
	def count_inversions(self, matrix=None):
		"""
		Returns the number of inversions in a given matrix.
		https://www.geeksforgeeks.org/check-instance-15-puzzle-solvable/
		"""
		arr = deepcopy(matrix) if matrix else deepcopy(self.matrix)
		n = len(arr)
		arr1=[]
		for y in arr:
			for x in y:
				arr1.append(x)
		arr=arr1
		inv_count = 0
		for i in range(n * n - 1):
			for j in range(i + 1,n * n):
				if (arr[j] and arr[i] and arr[i] > arr[j]):
					inv_count+=1
		
		return inv_count
	
	def get_empty_slot(self):
		n = len(self.matrix)
		for i in range(n):
			if 0 in self.matrix[i]:
				return i, self.matrix[i].index(0)

	def get_neighbors(self):
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
	
	def __eq__(self, other):
		return self.id == other.id
	
	def is_solvable(self):
		"""
		Checks if the given matrix is a solvable n-puzzle.
		"""
		num_inversions = self.count_inversions()
		initial_inverse_row = len(self.matrix) - self.get_empty_slot()[0]

		if len(self.matrix) % 2 == 1:
			return num_inversions % 2 == 0

		if initial_inverse_row % 2 == 1:
			return num_inversions % 2 == 0 
		
		if initial_inverse_row % 2 == 0:
			return num_inversions % 2 == 1
		
		return False

