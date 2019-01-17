'''
This file generates a valid Sudoku board from scratch using Backtrack mechanism.
After a full board is generated, random number of blocks are hidden to generate a valid 
unsolved sudoku board.
'''

import random

######################  Validating Board  ######################
def checkRow(board,i,val):
	if val in board[i]:
		return True
	return False
	
def checkCol(board,j,val):
	for X in board:
		if X[j] == val:
			return True
	return False
	
def checkGrid(board,i,j,val):
	if i%3==1:
		if j%3==0 \
		 and val in (board[i-1][j+1],board[i-1][j+2]):
			return True
		elif j%3==1 \
		 and val in (board[i-1][j-1],board[i-1][j+1]):
			return True
		elif j%3==2 \
		 and val in (board[i-1][j-1],board[i-1][j-2]):
			return True					
	elif i%3==2:
		if j%3==0 \
		 and val in (board[i-1][j+1],board[i-1][j+2],board[i-2][j+1],board[i-2][j+2]):
			return True
		elif j%3==1 \
		 and val in (board[i-1][j-1],board[i-1][j+1],board[i-2][j-1],board[i-2][j+1]):
			return True
		elif j%3==2 \
		 and val in (board[i-1][j-1],board[i-1][j-2],board[i-2][j-1],board[i-2][j-2]):
			return True
	return False

######################  Using Backtrack to generate a new board  ######################  
def makeBoard():
    board = [[None for _ in range(9)] for _ in range(9)]

    def fillBoard(c=0):
        i, j = divmod(c, 9)
        numbers = list(range(1, 10))
        random.shuffle(numbers)
        for x in numbers:
            if (checkRow(board,i,x)==False                     
                and checkCol(board,j,x)==False
                and checkGrid(board,i,j,x)==False):          
                board[i][j] = x
                if c + 1 >= 81 or fillBoard(c + 1):
                    return board
        else:
            board[i][j] = None
            return None

    return fillBoard()

######################  Hide random number of blocks from the board  ######################
def setDifficulty(board,diff):
	Board=board
	cells=list(range(81))
	random.shuffle(cells)
	for i in range(0,diff):
		x,y = divmod(cells[i],9)
		Board[x][y]=0
	return Board

######################  Utility function to display board  ######################    
def displayBoard(board):
	for i in range(9):
		if i%3 == 0:
			print('++===++===++===++===++===++===++===++===+')
		else:
			print('+---+---+---+---+---+---+---+---+---+---+')
		print('||',end=' ')
		for j in range(9):
			if j %3 == 2:
				if board[i][j]==0:
					print(' ',end=' || ')
				else:
					print(board[i][j],end=' || ')
			else:
				if board[i][j]==0:
					print(' ',end=' | ')
				else:
					print(board[i][j],end=' | ')
		print()
	print('++===++===++===++===++===++===++===++===+')

###################### driver function  ######################
def main():
	board=makeBoard()
	D = random.randint(30,40)
	Board=setDifficulty(board,D)
	return Board
