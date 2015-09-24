"""
Find all possible rings in a given topology or graph.

Required external modules:
python-networkx module
	
Usage:
import the module 	: import rings
call function 		: rings.getAllRings(graph, isMultigraph)							
where graph is the input networkx graph object
isMultigraph is True if graph is multigraph else False
						  
Algorithm explanation:
Input is a graph. Get the cycle basis of the graph. From it, get symmetric difference between the
edges of all combinations of cycle basis. Exclude non-cycles (if it contains node with degree!=2)
and disconnected graphs (e.g: 2 cyclic components in a graph)						  						  
"""

import networkx as nx
from itertools import combinations, product
from CreateDebugLog import Userlogger, Debuglogger
	
def isCycle(graph):
	"""	This function takes a networkx graph object as input and returns True if the graph is a cycle
		Note: A graph is a cycle iff degree of every node is two and the graph is connected.
	"""
	if graph:
		degree_hist = nx.degree_histogram(graph) 			# get frequency of degree of all nodes
		if degree_hist[2] == len(graph.nodes()) and nx.is_connected(graph):	# if all nodes have degree = 2 => cycle
			Debuglogger.debug("Is a cycle")
			return True
	Debuglogger.debug("Is not a cycle")
	return False	
	
def getCycleBasis(graph):
	"""	Input: networkx simple graph
		Returns list of graph objects that form cycle basis of the input graph
	"""
	Debuglogger.info("In getCycleBasis")
	cycle_basis_list = [] 								# list of list of edges of each cycle basis 
	for cycle in nx.cycle_basis(graph):
		Debuglogger.debug("cycle basis ->"+str(cycle))
		cycle_graph = nx.Graph()
		cycle_graph.add_cycle(cycle)
		cycle_basis_list.append(cycle_graph.edges())
	return cycle_basis_list

def formatCycleEdgeList(graph, isMultigraph, all_cycle_edge_list_tuple, SwitchList):
	"""	Input -> graph object, bool whether multigraph or not, list of list of edges forming a cycle, dictionary port-port mappin gfor each node
		Returns list of list of edges forming cycle with attribute information
	"""
	Debuglogger.info("In formatCycleEdgeList - isMultigraph: "+str(isMultigraph))
	all_cycle_edge_list_str = []
	for ring in all_cycle_edge_list_tuple:
		cycle_str = []
		for edge in ring:
			node1 = edge[0]
			node2 = edge[1]
			if not isMultigraph:
				edge_dict = graph[node1][node2]
			else:
				edge_dict = graph[node1][node2][edge[-1]]	
			if edge_dict['wt'] in SwitchList[node1]:
				edge = (node1, node2, edge_dict['wt'], edge_dict['link_type'])
			else: edge = (node2, node1, edge_dict['wt'], edge_dict['link_type'])
			edge = " ".join(edge)
			#Debuglogger.debug(edge)
			cycle_str.append(edge)
		Debuglogger.debug(cycle_str)
		all_cycle_edge_list_str.append(cycle_str)
	return all_cycle_edge_list_str

def getRingsMultigraph(multigraph, all_cycle_edge_list):
	""" Input -> multigraph object, list of cycles or rings got from simple graph
		Returns list of list of edges of a ring. Edge is represented as (node1.node2,edge_id)	
	"""
	Debuglogger.info("In getRingsMultigraph")
	all_cycle_edge_list_multi = []
	for ring in all_cycle_edge_list:
		Debuglogger.debug("Ring:"+str(ring))
		cycle = []
		multi_edge_list = []
		edge_index = []
		for edge in ring:
			Debuglogger.debug("Edge:"+str(edge))
			node1 = edge[0]
			node2 = edge[1]
			if len(multigraph[node1][node2])>1:
				Debuglogger.info("this ia a multi edge")
				single_multi_edge = []
				for edge_id in multigraph[node1][node2].keys():
					single_multi_edge.append((node1, node2, edge_id))
				edge_new = single_multi_edge[0]
				multi_edge_list.append(single_multi_edge)
				edge_index.append(ring.index(edge))
			else:
				edge_new = edge + (0,)
			cycle.append(edge_new)
		all_cycle_edge_list_multi.append(cycle)
		Debuglogger.debug("multi_edge_list:"+str(multi_edge_list))
		if multi_edge_list:
			for combination in product(*multi_edge_list):
				for i in range(len(combination)):
					idx = edge_index[i]
					temp = cycle[:idx]+[combination[idx]]
					if i<len(cycle):
						temp+=cycle[i+1:]
					cycle = temp
				if temp not in all_cycle_edge_list_multi:
					all_cycle_edge_list_multi.append(temp)
					Userlogger.info("Ring "+str(len(all_cycle_edge_list_multi))+" "+str(temp))
					Debuglogger.info("Ring "+str(len(all_cycle_edge_list_multi))+" "+str(temp))									
	return all_cycle_edge_list_multi
				
def getAllRings(graph, isMultigraph):
	""" Parameters: graph -> networkx graph or multigraph object,
		isMultigraph -> True if graph is multigraph else false
		Returns list of list of edges forming cycles in the graph.
	"""		
	if isMultigraph:
		multigraph, graph = graph, nx.Graph(graph)				
	all_cycle_edge_list = []
	Debuglogger.info("Getting cycle basis")
	cycle_basis_list = getCycleBasis(graph)								# get cycle basis of given graph
	
	Userlogger.info('\nGetting all the rings from physical topology')
	for i in range(1,len(cycle_basis_list)+1):							# form combinations of cycle basis
		Debuglogger.debug("Getting combinations of basis cycle picking "+str(i)+" items")
		for combination in combinations(cycle_basis_list,i):
			if combination:
				Debuglogger.debug("combination exists")
				edge_set = {}
				for basis in combination:								# find symmetric difference of
					edge_set = set(basis).symmetric_difference(edge_set)# members of each combination	
				ring = nx.Graph()
				ring.add_edges_from(list(edge_set))		
				if isCycle(ring):										#if the member is a connected cycle
					Debuglogger.debug("Is a connected cycle")
					all_cycle_edge_list.append(list(edge_set))			# add to list of all cycles
					Debuglogger.info("Ring "+str(len(all_cycle_edge_list))+" "+str(all_cycle_edge_list[-1]))
					Userlogger.info("Ring "+str(len(all_cycle_edge_list))+" "+str(all_cycle_edge_list[-1]))
	if isMultigraph:
		return getRingsMultigraph(multigraph, all_cycle_edge_list)
	return all_cycle_edge_list
	
def chooseOptimalRing(graph, list_rings_edges, **kwds):
	pass

	
