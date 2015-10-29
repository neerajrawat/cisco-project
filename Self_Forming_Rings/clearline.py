import pexpect
import telnetlib
from CreateDebugLog import Userlogger, Debuglogger

def clearline(ip,port):
		
	""" clear the line of the given switch with ip and port """ 
	Debuglogger.info("In Clearline function")
	Debuglogger.info("Clear the line of switch with  "+ip+' '+port)
	Userlogger.info("Clear the line of switch with  "+ip+' '+port)
		
	child= pexpect.spawn('telnet '+ip)				        
	child.expect('Password:')
	child.sendline('lab')
	child.expect('>')
	child.sendline('en')
	child.expect('Password:')
	child.sendline('lab')
	child.expect('#')
	child.sendline('clear line '+str(int(port)%100))
	child.sendcontrol('m')	
	child.expect('#')	
	child.close()
	print "line is cleared"
	
def switch_exec(ip,port):
		""" makes the switch in exec mode instead of config mode. """			
		Debuglogger.info("In switch_exec function")
		Debuglogger.info("makes switch ("+ip+' '+port+") in exec mode")
		Userlogger.info("makes switch ("+ip+' '+port+") in exec mode")
		
		child= pexpect.spawn('telnet '+ip+' '+port)	 
		child.expect('Escape.*')
		child.sendcontrol('m')
		child.expect('#')
		child.sendline('end')				
		child.expect('#')				
		child.sendline('quit')
		child.expect(' ')				
		child.sendcontrol('m')
		child.expect('>')

	
