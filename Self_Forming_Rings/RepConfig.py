"""
To disable all the ports of a given networkx object, to enable rep on given networkx object, to enable all ports and disable rep on all ports for a given networkx object.

Class Rep_configuration has 3 static methods.

disable_switch() method takes networkx object as input and disables all ports for all nodes in networkx object. 

repp() method takes networkx object as input and enables and configures rep on all ports for all nodes in networkx object.

restore() method takes networkx object as input and enables all ports and disables rep on all ports for all nodes in networkx object.  
 
"""
import networkx as nx
import time

import RunCommands as run
from CreateDebugLog import Userlogger, Debuglogger
from clearline import clearline
from statusbar import bar,barlen


class Rep_configuration:

	@staticmethod	
	def disable_switch(graph):
		""" disable_switch() method takes networkx object as input and disables all ports for all nodes in networkx object. """
		#start the progressbar	
		bar.start()
		
		Userlogger.info("disable all the ports in network")
		Userlogger.info('\nDisabling all ports of Physical topology')	 		
		graph_nodes_list=graph.nodes()
		i=0
		while i< len(graph_nodes_list):
			try:
				node_data=graph_nodes_list[i].split('\n')
				Userlogger.info('\nDisabling all ports of '+str(node_data[0]))	
				run.Switch_commands.commandExecute(node_data[1],node_data[2],'config','shutdown','disable',graph.node[graph_nodes_list[i]]['node_port'])
				i=i+1
				#bar update
				bar.update((.4*barlen*i)/len(graph_nodes_list))	
			except:
				pass		
	
						
	@staticmethod	
	def repp(graph):
		""" repp() method takes networkx object as input and enables and configures rep on all ports for all nodes in networkx object. """
		
		Userlogger.info("enabling rep in network")
		Userlogger.info("\nEnabling rep on Selected logical topology")
		graph_nodes_list=graph.nodes()
		node_num=1
		i=0
		while i< len(graph_nodes_list):
			try:					
				node_data=graph_nodes_list[i].split('\n')		
				if node_num==1:
					Userlogger.info('Enabling rep on '+str(node_data[0])+ ' edge')
					run.Switch_commands.commandExecute(node_data[1],node_data[2],'config','rep segment 1','enable',graph.node[graph_nodes_list[i]]['node_port'],'edge')
				else:
					Userlogger.info('Enabling rep on '+str(node_data[0]))
					run.Switch_commands.commandExecute(node_data[1],node_data[2],'config','rep segment 1','enable',graph.node[graph_nodes_list[i]]['node_port'],' ')
						
				node_num+=1
				i = i+1	
				#bar update
				bar.update(.4*barlen+( (.6*barlen*i)/len(graph_nodes_list) ))	
				
			except:
				pass			
		#end the bar
		bar.finish()	
		
	@staticmethod
	def restore(graph):
		""" restore() method takes networkx object as input and enables all ports and disables rep on all ports for all nodes in networkx object. """
		bar.start()
		Userlogger.info("restoring the previous network topology")
		Userlogger.info('\nRestoring prevoius Physical topology and diabling rep')	
		graph_nodes_list=graph.nodes()	
		i=0
		while i< len(graph_nodes_list):
			try:
				node_data=graph_nodes_list[i].split('\n')
				run.Switch_commands.commandExecute(node_data[1],node_data[2],'config','no rep segment 1','restore',graph.node[graph_nodes_list[i]]['node_port'])
				i+=1
				#bar update
				bar.update( (barlen*i)/len(graph_nodes_list) )
			except:
				pass	
		#end the bar		
		bar.finish()	
						
	@staticmethod	
	def showrepp(graph):
		" shows the rep topology"
		node=graph.nodes()[0]
		node_data=node.split('\n')
		Debuglogger.info('\nin show repp function')
		Userlogger.info('\nshowing the rep configuration')						
		while 1:		
			try:
				run.Switch_commands.commandExecute(node_data[1],node_data[2],'exec','show rep topology')
				templog=open('tempLog.txt','r')
				lines=templog.readlines()
				i=5
				while i<len(lines):
					print lines[i]
					i+=1
				templog.close()
				break	
			except:
				pass
					
		
