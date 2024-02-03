from copy import deepcopy

class State(object):
	"""
	This class represents a single state in our search path.
	It consists of a matrix, an ID, h_cost, g_cost, f_cost, and a parent.
	"""
	def __init__(self, matrix) -> None:
		self.matrix = matrix
		self.id = self.get_id()
		self.h_cost = self.linear_conflicts()
		self.g_cost = 0
		self.parent = None

	def set_f_cost(self):
		"""
		Set h_cost and g_cost. h_cost is equal to the number of inversions.
		g_cost is equal to the number of inversions to get to the original permutation.
		"""
		self.h_cost = self.linear_conflicts()
		self.g_cost += 1
		
	def get_f_cost(self):
		"""
		Dynamically returns the f cost.
		"""
		return self.h_cost + self.g_cost

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

	def manhattan(self, candidate, solved):
		"""
		Takes as input two flattened matrices,
		returns the Manhattan distance between them.
		Adapted from:
		https://github.com/asarandi/n-puzzle/blob/2853d6bb9e78dede1e4be4d432eb494c09efc3f5/npuzzle/heuristics.py#L46
		"""
		n = len(self.matrix)
		res = 0
		for i in range(n * n):
			if candidate[i] != 0 and candidate[i] != solved[i]:
				ci = solved.index(candidate[i])
				y = (i // n) - (ci // n)
				x = (i % n) - (ci % n)
				res += abs(y) + abs(x)
		return res

	def linear_conflicts(self):
		"""
		Calculates Manhattan distance + linear conflicts.
		Adapted from:
		https://github.com/asarandi/n-puzzle/blob/2853d6bb9e78dede1e4be4d432eb494c09efc3f5/npuzzle/heuristics.py#L46
		"""
		n = len(self.matrix)
		candidate = [element for sublist in self.matrix for element in sublist]
		solved = list(range(1, n*n))
		solved.append(0)

		def count_conflicts(candidate_row, solved_row, n, ans=0):
			counts = [0 for x in range(n)]
			for i, tile_1 in enumerate(candidate_row):
				if tile_1 in solved_row and tile_1 != 0:
					solved_i = solved_row.index(tile_1)
					for j, tile_2 in enumerate(candidate_row):
						if tile_2 in solved_row and tile_2 != 0 and i != j:
							solved_j = solved_row.index(tile_2)
							if solved_i > solved_j and i < j:
								counts[i] += 1
							if solved_i < solved_j and i > j:
								counts[i] += 1
			if max(counts) == 0:
				return ans * 2
			else:
				i = counts.index(max(counts))
				candidate_row[i] = -1
				ans += 1
				return count_conflicts(candidate_row, solved_row, n, ans)

		res = self.manhattan(candidate, solved)
		candidate_rows = [[] for y in range(n)]
		candidate_columns = [[] for x in range(n)]
		solved_rows = [[] for y in range(n)]
		solved_columns = [[] for x in range(n)]
		for y in range(n):
			for x in range(n):
				idx = (y * n) + x
				candidate_rows[y].append(candidate[idx])
				candidate_columns[x].append(candidate[idx])
				solved_rows[y].append(solved[idx])
				solved_columns[x].append(solved[idx])
		for i in range(n):
			res += count_conflicts(candidate_rows[i], solved_rows[i], n)
		for i in range(n):
			res += count_conflicts(candidate_columns[i], solved_columns[i], n)
		return res
