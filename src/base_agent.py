import random
from utils import MIN_N, MAX_N
from copy import deepcopy
from state import State

class BaseNPuzzleSolver(object):
	def __init__(self, filepath) -> None:
		self.state = self.read_input(filepath)

		assert self.state.is_solvable(), "This matrix has no solution!"

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
