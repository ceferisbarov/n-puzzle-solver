# Project 1 : Informed Search, Option 3 : N-Puzzle
**Jafar Isbarov, g35511671**
## Problem statement
Write a program that solves N-puzzle in n\*n grid such that you rearrange the square blocks of the puzzle to be in order with the fewest possible moves. The puzzle includes 1 to N numbers with one blank space and you can move the squares horizontally and vertically into the blank space. 8-puzzle is a 3\*3 grid labeled 1 though 8 and one blank square. 15-puzzle is a 4\*4 grid labelled 1 through 15 and one blank square. Use A* search algorithm in your implementation.

* **States:** N\*N matrices populated by values in range [1, N*N-1]. Remaining one cell is 0.
* **Actions:** NSEW
* **Successor:** swap the missing value with one of its neighbours
* **Goal test:** sort in ascending order from top-left

## Algorithm
It is stated that we have to implement A* algorithm to solve this problem. A* is a pathfinding algorithm that uses two cost functions: H and G. H represents the distance to the goal, while G represents the distance to the starting state. G is calculated easily: Increment by one every time you increase the depth. The tricky part is finding an admissible heuristic for H.

Admissible heuristic is a cost function that always gives us a value that is **less than or equal** to the actual cost. I initially used Hamming distance, but A* was too slow for larger values of N, so I switched to Linear conflict + Manhattan distance, which sped up the implementation considerably.

Manhattan distance of a cell is calculated as the number of slides/tiles away it is from its goal state. For example, in the following state, Manhattan distance of 8 is 4.
```
8 2 3
4 5 6
7 1 0
```
We calculate sum of Manhattan distances for all values except for 0.  
  
Linear conflict cost is calculated as number of cases, where two values are in the same row or column, also their goal positions are in the same row or column and the goal position of one of the tiles is blocked by the other tile in that row. For example, in the following state, numbers 1 and 4 are in linear conflict:
```
4 2 5
1 0 6
3 8 7
```
Our total H cost is Manhattan distance + Linear conflict cost.
  
## How to run

On Ubuntu:
```sh
# Clone the repo
git clone https://github.com/ceferisbarov/n-puzzle-solver

cd n-puzzle-solver

# Provide the input and output paths
python3 src/solve.py --input data/3.a.txt --output out/3.a.txt
```
Resulting matrix and the path will be saved to `out/3.txt` in the following format, from starting state to the goal state:
```
state 1
1	2	3
4	5	6
7	8	0
--------
state 2
1	2	3
4	5	0
7	8	6
--------
```
