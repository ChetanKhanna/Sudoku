"""
This is a self initiated learning project inspired from UCB CS-188.

Roadmap:- 1) genrate random sudoku board.
		  2) solve using baktracking CSP
		  3) optimize CSP using filtering -- forward checking and arc consistency
"""

import random
import time
import itertools


####################################  SOLVING RANDOM SUDOKU BOARD  ####################################
import graph

def makeSudokuGraph(sudokuList):
	"""
	sudokuList is assumed to be a list of list containing some valid 
	sudoku values and None for blocks to be filled. Each list of 
	sudokuList is considered to be a row in sudoku board.
	"""
	## Initializing graph object
	sudokuGraph = graph.Graph()
	## Making constraint graph:
	for i in range(9):
		for j in range(9):
			if not sudokuList[i][j]:
				sudokuGraph.addVertex((i,j))
	## Row-constraints
	for i in range(9):
		row  = [(i,j) for j in range(9) if (i,j) in sudokuGraph]
		for n1, n2 in itertools.combinations(row, 2):
			sudokuGraph.addEdge(n1, n2, twoWay = True)
	## Col-constraints
	for i in range(9):
		col  = [(j,i) for j in range(9) if (j,i) in sudokuGraph]
		for n1, n2 in itertools.combinations(col, 2):
			sudokuGraph.addEdge(n1, n2, twoWay = True)
	## Grid-constraints
	for i in range(9):
		for j in range(9):
			if i%3 == 1:
				if j%3 == 0:
					if (i,j) in sudokuGraph:
						if (i-1, j+1) in sudokuGraph:
							sudokuGraph.addEdge((i,j), (i-1,j+1), twoWay = True)
						if (i-1, j+2) in sudokuGraph:
							sudokuGraph.addEdge((i,j), (i-1,j+2), twoWay = True)
				elif j%3 == 1:
					if (i,j) in sudokuGraph:
						if (i-1, j-1) in sudokuGraph:
							sudokuGraph.addEdge((i,j), (i-1,j-1), twoWay = True)
						if (i-1, j+1) in sudokuGraph:	
							sudokuGraph.addEdge((i,j), (i-1,j+1), twoWay = True)
				elif j%3 == 2:
					if (i,j) in sudokuGraph:
						if (i-1, j-2) in sudokuGraph:
							sudokuGraph.addEdge((i,j), (i-1,j-2), twoWay = True)
						if (i-1, j-1) in sudokuGraph:
							sudokuGraph.addEdge((i,j), (i-1,j-1), twoWay = True)
			if i%3 == 2:
				if j%3 == 0:
					if (i,j) in sudokuGraph:
						if (i-2, j+1) in sudokuGraph:
							sudokuGraph.addEdge((i,j), (i-2,j+1), twoWay = True)
						if (i-2, j+2) in sudokuGraph:
							sudokuGraph.addEdge((i,j), (i-2,j+2), twoWay = True)
						if (i-1, j+1) in sudokuGraph:
							sudokuGraph.addEdge((i,j), (i-1,j+1), twoWay = True)
						if (i-1, j+2) in sudokuGraph:
							sudokuGraph.addEdge((i,j), (i-1,j+2), twoWay = True)
				elif j%3 == 1:
					if (i,j) in sudokuGraph:
						if (i-2, j-1) in sudokuGraph:
							sudokuGraph.addEdge((i,j), (i-2,j-1), twoWay = True)
						if (i-2, j+1) in sudokuGraph:
							sudokuGraph.addEdge((i,j), (i-2,j+1), twoWay = True)
						if (i-1, j-1) in sudokuGraph:
							sudokuGraph.addEdge((i,j), (i-1,j-1), twoWay = True)
						if (i-1, j+1) in sudokuGraph:
							sudokuGraph.addEdge((i,j), (i-1,j+1), twoWay = True)
				elif j%3 == 2:
					if (i,j) in sudokuGraph:
						if (i-2, j-1) in sudokuGraph:
							sudokuGraph.addEdge((i,j), (i-2,j-1), twoWay = True)
						if (i-2, j-1) in sudokuGraph:
							sudokuGraph.addEdge((i,j),(i-2,j-1), twoWay = True)
						if (i-1, j-2) in sudokuGraph:
							sudokuGraph.addEdge((i,j), (i-1,j-2), twoWay = True)
						if (i-1, j-1) in sudokuGraph:
							sudokuGraph.addEdge((i,j), (i-1,j-1), twoWay = True)
	## Adding domain:
	for v in sudokuGraph.getVertices():
		i, j = v
		blockedRowVals = [_ for _ in range(1,10) if _ in sudokuList[i]]
		blockedColVals = [_ for _ in range(1,10) if _ in list(zip(*sudokuList))[j]]
		blockedGridVals = []
		if i%3 == 0:
			if j%3 == 0:
				temp = (sudokuList[i+1][j+1], sudokuList[i+1][j+2],
								sudokuList[i+2][j+1], sudokuList[i+2][j+2])
				for _ in temp:
					blockedGridVals.append(_)
			elif j%3 == 1:
				temp = (sudokuList[i+1][j-1], sudokuList[i+1][j+1],
								sudokuList[i+2][j-1], sudokuList[i+2][j+1])
				for _ in temp:
					blockedGridVals.append(_)
			elif j%3 == 2:
				temp = (sudokuList[i+1][j-1], sudokuList[i+1][j-2],
								sudokuList[i+2][j-1], sudokuList[i+2][j-2])
				for _ in temp:
					blockedGridVals.append(_)
		elif i%3 == 1:
			if j%3 == 0:
				temp = (sudokuList[i-1][j+1], sudokuList[i-1][j+2],
								sudokuList[i+1][j+1], sudokuList[i+1][j+2])
				for _ in temp:
					blockedGridVals.append(_)
			elif j%3 == 1:
				temp = (sudokuList[i-1][j-1], sudokuList[i-1][j+1],
								sudokuList[i+1][j-1], sudokuList[i+1][j+1])
				for _ in temp:
					blockedGridVals.append(_)
			elif j%3 == 2:
				temp = (sudokuList[i-1][j-1], sudokuList[i-1][j-2],
								sudokuList[i+1][j-1], sudokuList[i+1][j-2])
				for _ in temp:
					blockedGridVals.append(_)
		elif i%3 == 2:
			if j%3 == 0:
				temp = (sudokuList[i-1][j+1], sudokuList[i-1][j+2],
								sudokuList[i-2][j+1], sudokuList[i-2][j+2])
				for _ in temp:
					blockedGridVals.append(_)
			elif j%3 == 1:
				temp = (sudokuList[i-1][j-1], sudokuList[i-1][j+1],
								sudokuList[i-2][j-1], sudokuList[i-2][j+1])
				for _ in temp:
					blockedGridVals.append(_)
			elif j%3 == 2:
				temp = (sudokuList[i-1][j-1], sudokuList[i-1][j-2],
								sudokuList[i-2][j-1], sudokuList[i-2][j-2])
				for _ in temp:
					blockedGridVals.append(_)
		totalBlockedVals = blockedGridVals + blockedColVals + blockedRowVals
		sudokuGraph.domain[v] = [_ for _ in range(1,10) if _ not in totalBlockedVals]
	## return constraint graph:
	return sudokuGraph

#############################################################################################################

## Preparing sudoku board ##
import sudokuGenerator
board = sudokuGenerator.main()

## printing the unsolved board ##
print('Generating sudoku...')
sudokuGenerator.displayBoard(board)
print('done.')

## Converting to sudokuSolver format ##
for i in range(9):
	for j in range(9):
		if board[i][j] == 0:
			board[i][j] = None

## Making graph from list of list
print('Generating graph for sudoku board...')
G = makeSudokuGraph(board)
print('done.')

## Calling the filter function to solve board ##
import CSP
print('solving board...')
startTime = time.clock()
assgn = CSP.BacktrackSearch(G)
endTime = time.clock()
print('done.')

for i, j in assgn:
	board[i][j] = assgn[(i,j)]

sudokuGenerator.displayBoard(board)
print('Time taken to solve board:',endTime - startTime)