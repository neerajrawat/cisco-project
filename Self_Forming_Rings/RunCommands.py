
"""
To run the commands of the switch.

Class Switch_commands has 3 static methods.

commandExecute() method takes ip and port of switch,mode(exec or config),command to run and variable length argument as input.It runs the  given command corresponding to the mode and creates a 'tempLog.txt' file to store the command output.
For running rep on switch =Only 2 entries in  variable length argument. 1st entry will be interface list. 2nd entry will be either 'edge' or ' ' depending on whether we want that switch's interfaces to be configured as edge or not. 
For disabling rep on switch = Only 1 entry in variable length argument 1st entry will be interface list.
"""
import sys
import telnetlib
import pexpect
import time

from clearline import clearline,switch_exec
from CreateDebugLog import Userlogger, Debuglogger

class Switch_commands:

	@staticmethod
	def commandExecute(ip,port,mode,command,*param):
		""" commandExecute() method takes ip and port of switch,mode(exec or config),command to run and variable length argument as input.It runs the  given 			    command corresponding to the mode and creates a 'tempLog.txt' file to store the command output.
		    For running rep on switch =Only 2 entries in  variable length argument. 1st entry will be interface list. 2nd entry will be either 'edge' or ' ' 			    depending on whether we want that switch's interfaces to be configured as edge or not. 
		    For disabling rep on switch = Only 1 entry in variable length argument 1st entry will be interface list. """

		Debuglogger.info("Running: "+command)
			
		try:
			child= pexpect.spawn('telnet ' +ip+' '+port)	
			fout=open('tempLog.txt','w')					
			child.logfile=fout

			child.expect('Escape.*')
			child.sendcontrol('m')
			child.expect('>')		
			
			if mode=='exec':
				child.sendline(command)
				child.expect('>')
					
			elif mode=='config':
			 	child.sendline('en')
				child.expect('#')
				child.sendline('config t')
				child.expect('#')
				#print param[1]	 		
			 	#for diabling all ports in physical topology	
			 	if param[0]=='disable':
			 		for node_interface in param[1]:
						child.sendline('interface'+' '+node_interface)
						child.expect('#')		
						child.sendline(command)				
						child.expect('#')
						
				#for enabling rep all ports in selected topology
				elif param[0]=='enable':
					if param[2]=='edge':
						edge_config=['primary',' ']
					else:	
						edge_config=[' ',' ']
					i=0		
					for node_interface in param[1]:			
						child.sendline('interface'+' '+node_interface)
						child.expect('#')
						child.sendline('no shutdown')
						child.expect('#')
						#time.sleep(2)
						child.sendline('switchport trunk encapsulation dot1q')				
						child.expect('#')
						child.sendline('switchport  mode trunk')				
						child.expect('#')
						child.sendline(command+' '+param[2]+' '+edge_config[i])
						child.expect('#')
						Userlogger.info(node_interface+' '+command+' '+param[2]+' '+ edge_config[i])#	
						i+=1
					
				#for restoring Physical topology and disabling rep
				elif param[0]=='restore':
					for node_interface in param[1]:
						child.sendline('interface'+' '+node_interface)
						child.expect('#')		
						child.sendline(command)				
						child.expect('#')	
						child.sendline('no shutdown')				
						child.expect('#')
				else:
					pass			

				child.sendline('end')				
				child.expect('#')				
				child.sendline('quit')
				child.expect(' ')				
				child.sendcontrol('m')
				child.expect('>')
		 			
			child.logfile=sys.stdout
			child.close()
		
		except pexpect.EOF:
			print "Connection is refused. Clear the session" + '  Run clearLine() function with command line arguments as  '+ ip+ ' '+port
			Debuglogger.info("telnet to "+ip+' '+port+"Connection is refused. Clear the session")
			Userlogger.info("telnet to "+ip+' '+port+"Connection is refused. Clear the session")
			while 1:
				ip_user = raw_input('Please enter the IP of the switch, as displayed in previous exception message : ')
				port_user = 	raw_input('Please enter the PORT of the switch, as displayes in previous exception message : ')
				if(ip_user==ip and port_user==port):
					break
				else:
					print "wrong entry"								
			clearline(ip,port)
			
		except pexpect.TIMEOUT:
			print "Switch is in config or privledge mode. Come in exec mode" +' Run switch_exec() function with command line arguments as  '+ ip+ ' '+port
			Debuglogger.info("Switch ("+ip+' '+port+") is in config. Come in exec mode")
			Userlogger.info("Switch ("+ip+' '+port+") is in config. Come in exec mode")
			while 1:
				ip_user = raw_input('Please enter the IP of the switch, as displayed in previous exception message : ')
				port_user = 	raw_input('Please enter the PORT of the switch, as displayes in previous exception message : ')
				if(ip_user==ip and port_user==port):
					break
				else:
					print "wrong entry"
			clearline(ip,port)										
			switch_exec(ip,port)
	
			
