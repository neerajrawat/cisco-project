
"""
To make the networkx object of the given network and draw the graph using the networkxobject.

Class Network_graph has 2 static methods.

makeGraph() method takes edges_info as input and returns a networkx object of the network. edges_info is a list with entries being the edges in the network. 
Edges are entered as two switchname+IPs+Ports and corresponding intefaces and type of link.
  
drawTopology() method takes networkx object of the network, filename of the image to create and creates image of the network with a given filename  

"""

import pydot
import networkx as nx
from CreateDebugLog import Userlogger, Debuglogger

class Network_graph:

	@staticmethod	
	def makeGraph(edges_info):
		""" makeGraph() method takes edges_info as input and returns a networkx object of the network. edges_info is a list with entries being the edges in the 		    network. Edges are entered as two switchname+IPs+Ports and corresponding intefaces and type of link. """
		
		Debuglogger.info("Making a graph object with a given Edge list")	
		
		graph = nx.Graph()			
		multigraph = nx.MultiGraph()
		for edge in edges_info:
			info = edge.split(' ')
			node1 = info[0]
			node2 = info[1]
			port = " ".join(info[2:-1])
			link_type = info[-1]
			if node1 not in graph:
				graph.add_node(node1,node_port=[])
				multigraph.add_node(node1,node_port=[])
			graph.node[node1]['node_port'].append(info[2])
			multigraph.node[node1]['node_port'].append(info[2])
			
			if node2 not in graph:
				graph.add_node(node2,node_port=[])
				multigraph.add_node(node2,node_port=[])	
			graph.node[node2]['node_port'].append(info[3])
			multigraph.node[node2]['node_port'].append(info[3])
			
			multigraph.add_edge(node1,node2, wt=port, link_type=link_type)
			graph.add_edge(node1,node2, wt=port, link_type=link_type)
			
		if len(multigraph.edges())>len(graph.edges()):
			return multigraph,True
		return graph,False
		
	@staticmethod
        def drawTopology(topology,isMultigraph,saveas):
        	""" drawTopology() method takes networkx object of the network, filename of the image to create and creates image of the network 
        	    with a given filename. """ 
        	
        	Debuglogger.info("Drawing graph with a given networkxobject")#
		G = pydot.Dot(graph_type='graph', dpi=300 , splines = "curved")
		G.set_node_defaults(style="filled", fillcolor="grey",fontsize=7.0)
		G.set_layout("circo")
		G.set_edge_defaults(fontsize=7.0)
		
		for edge in list(set(topology.edges())):
			node1=edge[0]
			node2=edge[1]
			if isMultigraph:
				for ed_info in topology[node1][node2]:
					if topology[node1][node2][ed_info]['link_type']=='Gig':	
						edge_style = 'bold'
					elif topology[node1][node2][ed_info]['link_type'] == 'Fas':
						edge_style = 'dotted'
					G.add_edge(pydot.Edge(node1,node2,style=edge_style,label=topology[node1][node2][ed_info]['wt']))           
			else:
					#print saveas
					if topology[node1][node2]['link_type']=='Gig':	
						edge_style = 'bold'
					elif topology[node1][node2]['link_type'] == 'Fas':
						edge_style = 'dotted'
					G.add_edge(pydot.Edge(node1,node2,style=edge_style,label=topology[node1][node2]['wt']))
		G.write_png(saveas)
		
