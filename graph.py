'''
This is the graph data structure file used for solving sudoku.
'''

class Vertex:
	
	def __init__(self, key):
		self.id = key
		self.connection = {}

	def __str__(self):
		return str(self.id) + ' connected to: ' + str([x for x in self.connection])


class Graph:

	def __init__(self):
		self.vertList = {}
		self.numVertex = 0
		self.domain = {}

	def __contains__(self, item):
		return item in self.vertList

	def __iter__(self):
		return iter(self.vertList.keys())

	def __setitem__(self, key, value):
		self.addVertex(key)

	def __getitem__(self, key):
		return self.getVertex(key).connection.keys()
		## returning dict.keys() is mandatory for the '-' operation used below
		## since (dict.keys() - set) is valid but (dict - set) is not

	def addVertex(self, vert):
		if vert not in self.vertList:
			newVert = Vertex(vert)
			self.vertList[vert] = newVert
			self.numVertex = self.numVertex + 1

	def addEdge(self, fromVert, toVert, weight = 0, twoWay = False):
		if fromVert not in self.vertList:
			self.addVertex(fromVert)
		if toVert not in self.vertList:
			self.addVertex(toVert)

		self.vertList[fromVert].connection[toVert] = weight

		if twoWay:
			self.vertList[toVert].connection[fromVert] = weight

	def getVertex(self, vertKey):
		if vertKey in self.vertList:
			return self.vertList[vertKey]
		else:
			return None

	def getVertices(self):
	 return self.vertList.keys()
	 
