'''
This file defines the Constraint Search Problem -- which is to solve 
randomly generated sudoku board.
'''

from random import shuffle
import time
from itertools import permutations


#############################################################################################################

def goalTest(assignment, graph):
	if len(assignment) == len(graph.getVertices()): ## Checking if all variables are assigned
		## Writting constraints implicitly
		for v in graph.getVertices():
			for c in graph.getVertex(v).connection:
				if assignment[v] == assignment[c]:
					return False
		return True
	return False

def nextUnassignedVar(assignment, graph):
	for n in graph.getVertices() - assignment.keys():	## This gives a list of unassigned vertices
														## by overloading '-' operator
		return n

def nextUnassignedVarOrder(assignment, graph):
	## Most constraint = least domain size
	unassignedVars = [(n, len(graph.domain[n])) for n in graph.getVertices() - assignment.keys()]
	unassignedVarsSorted = sorted(unassignedVars, key = lambda x: x[1]) ## Sort using second element
	if unassignedVarsSorted:
		return unassignedVarsSorted[0][0]
	else:
		return None

def leastConstraintOrder(var, assignment, graph):
	'''
	FunctionUndefined: This will require some change in the structure of few other functions
	The idea behind implementing this function was to get a list of values for the passed var
	sorted in increasing order of their effect on domains of other variables of CSP.

	'''
	pass

def checkAssignmentConsistency(var, val, assignment, graph):
	for c in graph.getVertex(var).connection: ## graph.getVertex(var).connection returns list of 
											  ## child nodes of 'Vertex' var. Check graph and vertex classes
		if c in assignment: 				  ## if c not in dict assignment, assignment[c] will raise Error
			if assignment[c] == val:
				return False
	return True

def removeInconsistent(head, tail, graph):
	removed = False
	if head in graph.getVertex(tail).connection:
		for val in graph.domain[tail]:
			if graph.domain[head] == [val]:
				graph.domain[tail].remove(val)
				removed = True
	return removed

###############  Filter functions for Sudoku  ###############
def forwardCheckFiletr(var, assignment, graph):
	'''
	If any neighbour of vertex 'var' also has the same assignment -- 
	assignment[var], then return False
	'''
	for c in graph.getVertex(var).connection:
		if assignment[var] in graph.domain[c]:
			graph.domain[c].remove(assignment[var])

def arcConsistencyFilter(assignment, graph):
	arcs = list(permutations(graph.domain, 2))
	while arcs:
		head, tail = arcs.pop(0)
		if removeInconsistent(head, tail, graph):
			for x in graph.getVertex(tail).connection:
				arcs.append((x, tail))

def filterPass(assignment, graph):
	for n in graph.getVertices() - assignment.keys():
		if not graph.domain[n]:
			return False
	return True
###############  ###############  ###############  ###############

def restoreDomain(var, val, assignment, graph, SD = None):
	for c in graph.getVertex(var).connection:
		graph.domain[c].append(val)  ## re-add removed color to domain of neighbours
	if SD:
		graph.domain[var] = [x for x in SD]

def BacktrackSearch(graph):
	return RecursiveBackTrack(dict(), graph)

def RecursiveBackTrack(assignment, graph):
	## Apply ordering to variable selection: select most constraint variable
	var = nextUnassignedVarOrder(assignment, graph)
	if goalTest(assignment, graph):
		return assignment
	for val in graph.domain[var]:
		if checkAssignmentConsistency(var, val, assignment, graph):
			assignment[var] = val
			saved_domain = [color for color in graph.domain[var] if color != val]
			forwardCheckFiletr(var, assignment, graph)  ## Filetring added: Forward Check
			if not filterPass(assignment, graph):
				## If forward check filters makes domain of an unassigned vertex empty, Fail  
				restoreDomain(var, val, assignment, graph, SD = saved_domain)  ## restore affected vertices before deletion
				del assignment[var]
				continue  ## continue to explore remaining colors in current vertex domain; don't return to prev vertex

			saved_domain = graph.domain

			arcConsistencyFilter(assignment, graph)
			if not filterPass(assignment, graph):  
			## if first forwardCheck passes and this fails
			## then mistake made in forwardCheckFilter assigment, therefore
			## restore domain of graph and then call restoreDomain function
			## to restore domain to the state before assignment
				graph.domain = saved_domain
				restoreDomain(var, val, assignment, graph, SD = saved_domain)
				del assignment[var]
				continue

			result = RecursiveBackTrack(assignment, graph)
			if result:
				return result
			restoreDomain(var, assignment[var], assignment, graph)  ## restore affected vertices before deletion
			del assignment[var] ## Remove wrongly assigned variable and try next val
	return False

###################################################################################################################
