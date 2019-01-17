# Sudoku
This is the first project I undertook while learning AI

Currently I am doing a course by UCB; CS 188 where we learnt about CSP in the last couple of lectures. I had previously
created a sudoku generator while learning Python. I used the same file (sudokuGenerator.py) to generate a random valid Sudoku
board. I used backtracking algorithm to do this.

Next, I used graph data structure, the code for which I wrote while learning DSA (actually, this one's still in progress. I
have a seperate repository where I have archived all my DSA work and will make it pubic soon). The code for this is in graph.py
Then I used the graph data structure to define a graph for my sudoku board in sudokuSolver.py

Finally I defined a CSP for sudoku in CSP.py which is further optimized using:
1. Forward Check Filtering
2. Arc Consistency Filtering
3. Max Constraint variable ordering
4. Least Constraint value ordering (This is NOT implemented; though I left a note in the CSP.py file for future reference)

Hence, I combined a lot of pieces which I learnt from here and there to get this one done.

Thanks :)
