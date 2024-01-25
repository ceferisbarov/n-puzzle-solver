import random
from config import MIN_N, MAX_N

class BaseNPuzzleSolver(object):
	def __init__(self, filepath) -> None:
		self.matrix = self.read_input(filepath)
		self.solvable = self.is_solvable()
		self.solved = self.is_solved()

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

		return input_matrix
	
	def count_inversions(self):
		"""
		Returns the number of inversions in a given matrix.
		https://www.geeksforgeeks.org/check-instance-15-puzzle-solvable/
		"""
		arr = self.matrix.copy()
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

	def is_solved(self):
		flat = [
			x
			for row in self.matrix
			for x in row
		]

		return flat == sorted(flat)
	
	def get_empty_slot(self):
		n = len(self.matrix)
		for i in range(n):
			if 0 in self.matrix[i]:
				return i, self.matrix[i].index(0)
			
	def swap_north(self):
		i, j = self.get_empty_slot()
		self.matrix[i][j], self.matrix[i-1][j] = self.matrix[i-1][j], self.matrix[i][j]

	def swap_south(self):
		i, j = self.get_empty_slot()
		self.matrix[i][j], self.matrix[i+1][j] = self.matrix[i+1][j], self.matrix[i][j]

	def swap_east(self):
		i, j = self.get_empty_slot()
		self.matrix[i][j], self.matrix[i][j+1] = self.matrix[i][j+1], self.matrix[i][j]

	def swap_west(self):
		i, j = self.get_empty_slot()
		self.matrix[i][j], self.matrix[i][j-1] = self.matrix[i][j-1], self.matrix[i][j]
