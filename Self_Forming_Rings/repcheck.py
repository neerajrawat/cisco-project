import telnetlib
import pexpect
import time


def disable_switch(node,interface_list):
	
	node_data=node.split('\n')			
	child= pexpect.spawn('telnet ' +node_data[1]+' '+node_data[2])	#telnet to a switch through pexpect module			
	child.expect('Escape.*')
	child.sendcontrol('m')
	child.expect('>')		
	child.sendline('en')
	child.expect('#')
		
	for node_interface in interface_list:
		child.sendline('config t')
		child.expect('#')
		child.sendline('interface'+' '+node_interface)
		child.expect('#')		
		child.sendline('shutdown')				
		child.expect('#')	
		child.sendline('end')				
		child.expect('#')
			
	child.sendline('quit')
	child.expect(' ')
	child.sendcontrol('m')
	child.expect('>')				


def repp(node,node_port,i):
		node_data=node.split('\n')
		child= pexpect.spawn('telnet ' +node_data[1]+' '+node_data[2])	#telnet to a switch through pexpect module			
		child.expect('Escape.*')
		child.sendcontrol('m')
		child.expect('>')		
		child.sendline('en')
		child.expect('#')
		print "1 switch"
		j=1
		for node_interface in node_port:
			child.sendline('config t')
			child.expect('#')
			child.sendline('interface'+' '+node_interface)
			child.expect('#')
			child.sendline('no shutdown')
			child.expect('#')
			time.sleep(2)
			child.sendline('switchport trunk encapsulation dot1q')				
			child.expect('#')
			child.sendline('switchport  mode trunk')				
			child.expect('#')
			print j
			if i==1:
				if j==1:	
					child.sendline('rep segment 1 edge primary')	
					print 'rep primary -- %s' %str(node_data[0])			
					child.expect('#')	
					child.sendline('end')				
					child.expect('#')
					j+=1
				else:
					child.sendline('rep segment 1 edge')
					print 'rep seg edge -- %s' %str(node_data[0])				
					child.expect('#')	
					child.sendline('end')				
					child.expect('#')
					j+=1
			else:
				child.sendline('rep segment 1')	
				print 'rep seg -- %s' %str(node_data[0])			
				child.expect('#')	
				child.sendline('end')				
				child.expect('#')
				j+=1
		child.sendline('quit')
		child.sendcontrol('m')
		child.expect('>')		
				
		
def no_rep(node,interface_list):	
	node_data=node.split('\n')			
	child= pexpect.spawn('telnet ' +node_data[1]+' '+node_data[2])	#telnet to a switch through pexpect module			
	child.expect('Escape.*')
	child.sendcontrol('m')
	child.expect('>')		
	child.sendline('en')
	child.expect('#')
		
	for node_interface in interface_list:
		child.sendline('config t')
		child.expect('#')
		child.sendline('interface'+' '+node_interface)
		child.expect('#')		
		child.sendline('no rep segment 1')				
		child.expect('#')	
		child.sendline('no shutdown')				
		child.expect('#')	
		child.sendline('end')				
		child.expect('#')
			
	child.sendline('quit')
	child.expect(' ')
	child.sendcontrol('m')
	child.expect('>')				
	
"""
node='NCH_A\n10.106.19.200\n2026'				
node_port=['Gig4/0/12','Gig4/0/20','Gig4/0/22']
disable_switch(node,node_port)

node='NCH_B\n10.106.19.200\n2014'				
node_port=['Gig1/0/18','Gig1/0/13','Gig1/0/19']
disable_switch(node,node_port)

node='NCH_C\n10.106.19.201\n2035'				
node_port=['Gig1/0/37','Gig1/0/39','Gig1/0/41']
disable_switch(node,node_port)

node='NCH_D\n10.106.19.201\n2015'				
node_port=['Gig2/0/13','Gig2/0/23','Gig2/0/20']
disable_switch(node,node_port)


node='NCH_A\n10.106.19.200\n2026'				
node_port=['Gig4/0/12','Gig4/0/20']
repp(node,node_port,1)

node='NCH_B\n10.106.19.200\n2014'				
node_port=['Gig1/0/18','Gig1/0/13']
repp(node,node_port,2)

node='NCH_C\n10.106.19.201\n2035'				
node_port=['Gig1/0/37','Gig1/0/39']
repp(node,node_port,3)
"""


node='NCH_A\n10.106.19.200\n2026'				
node_port=['Gig4/0/12','Gig4/0/20','Gig4/0/22']
no_rep(node,node_port)

node='NCH_B\n10.106.19.200\n2014'				
node_port=['Gig1/0/18','Gig1/0/13','Gig1/0/19']
no_rep(node,node_port)

node='NCH_C\n10.106.19.201\n2035'				
node_port=['Gig1/0/37','Gig1/0/39','Gig1/0/41']
no_rep(node,node_port)

node='NCH_D\n10.106.19.201\n2015'				
node_port=['Gig2/0/13','Gig2/0/23','Gig2/0/20']
no_rep(node,node_port)

