"""
To find the topology of the Network
Class Network_Topology has 2 class variables,3 class and 1 static methods.

SwitchList={} is a dictionary with keys being the Switch name,IP and port and the values corresponding to the keys will be
interfaces pair connected to that switch

EdgeList=[] is a list with each entry being two switchname with IP and port and corresponding interfaces and type of link (gig or Fast)

cdpread() method runs cdp command through commandExecute() defined in RunCommands module  to find the neighbours. It calls findname() 
and addedge() to find the name of switch and finding edges corresponding to that switch respectively.

findname() method finds the name of switch from cdp data.

addedge() method finds the edge from the cdp data and calls eList() to add the edge entry (two switch name and corresponding interfaces and type of link) in EdgeList.

eList() method adds the edge entry as two switch name and corresponding interfaces and type of link in EdgeList

eList_Modify() method modifies the EdgeList such as that instead of switchname it replaces the switchname with switchname+IP+Port.   
"""

#!/usr/bin/python
from CreateDebugLog import Userlogger, Debuglogger
import RunCommands as run

class Network_topology:
	
	SwitchList={}								
	EdgeList=[]
	
										
	def __init__(self,ip=None,portno=None,Name=""):
		""" constructor to initialize the class instance variables. """
							
		self.host=ip
		self.port=portno
		self.SwitchName=Name
				
	def findname(self):							
		""" findname() finds the name of switch from cdp data. """
		
		Debuglogger.info("Finding name through cdp data")
		fout=open('tempLog.txt','r')
		lines=fout.readlines()
		for line in lines:
			if '>' in line:
				break
		self.SwitchName=line[0:line.index('>')]
		fout.close()
						
        def cdpread(self):
		""" cdpread() method runs cdp command through commandExecute() defined in RunCommands module  to find the neighbours. It calls findname() 
		    and addedge() to find the name of switch and finding edges corresponding to that switch. """

		Debuglogger.info("In network topology")		
			
		run.Switch_commands.commandExecute(self.host,self.port,'exec','show cdp ne')				
		self.findname()   
		Userlogger.info('\nLogged into : '+self.SwitchName+' '+self.host+' '+self.port)
		Userlogger.info(self.SwitchName+'is connected to :')							
		Network_topology.SwitchList[self.SwitchName+'\n'+self.host+'\n'+self.port]=[]			
		self.addedge()	
		Userlogger.info('\n')

	def addedge(self):
		""" addedge() finds the edge from the cdp data and calls eList() to add the edge entry (two switch name and corresponding interfaces and type of link) 			    in EdgeList. """
	
		Debuglogger.info("Finding Edges")
		
		fCDP=open('tempLog.txt','r')
		lines=fCDP.readlines()	
		i=0
		#to get to that line which has switch information
		for line in lines:
			if "Device ID" in lines[i]:
				i+=1
				break
			i+=1
		
		while i< len(lines):
			currentline_info=lines[i].split()		
			Ln=len(currentline_info)			
			if Ln==0:
				break
			
			#this is to include if switch name is too long	then it interface information comes to next line
			elif Ln==1:
				i=i+1
				nextline_info=lines[i].split()
				destSwitch=currentline_info[0]
				source_interface=nextline_info[0]+nextline_info[1]				
				dest_interface=nextline_info[-2]+nextline_info[-1]
				i=i+1	
			else:
				destSwitch=currentline_info[0]
				source_interface=currentline_info[1]+currentline_info[2]				
				dest_interface=currentline_info[-2]+currentline_info[-1]	
				i=i+1		

			Network_topology.SwitchList[self.SwitchName+'\n'+self.host+'\n'+self.port].append(source_interface+' '+dest_interface)
			self.eList(destSwitch, source_interface, dest_interface)
			
			Userlogger.info(destSwitch)
		fCDP.close()

		
	def eList(self,destswitch,Sport,Dport):
			""" eList() adds the edge entry as two switch name and corresponding interfaces and type of link in EdgeList. """
			
			if 'Fas' in Dport or 'Fas' in Sport:
				typeport='Fas'	 
			else:
				typeport='Gig'
			
			edge_line=str(self.SwitchName+' '+destswitch+' '+Sport+' '+Dport+' '+typeport)			#to be appended
			inverted_edge_line=str(destswitch+' '+self.SwitchName+' '+Dport+' '+Sport+' '+typeport)		#inverted name	
			
			if inverted_edge_line not in Network_topology.EdgeList:
				Network_topology.EdgeList.append(edge_line)
	@staticmethod
	def eList_Modify():
		""" eList_Modify() modifies the EdgeList such as that instead of switchname it replaces the switchname with switchname+IP+Port. """
	
		Debuglogger.info("Modifying the Edge List in Network")#
		
		for switch_info in Network_topology.SwitchList.keys():
			switch_name= switch_info.split('\n')[0]						
			for i in range(0,len(Network_topology.EdgeList)):
				Network_topology.EdgeList[i]=Network_topology.EdgeList[i].replace(switch_name,switch_info)

