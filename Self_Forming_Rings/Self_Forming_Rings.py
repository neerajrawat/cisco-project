import time, getopt, sys
import cv2
import datetime
		 	
import Topology as mt
import GUI_topology as gui
import store as save
from rings import getAllRings,formatCycleEdgeList
import RepConfig as rep
from CreateDebugLog import Userlogger, Debuglogger
import store as load
from clearline import clearline
from statusbar import bar,barlen

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def get_args(opts):
	print opts
	for opt, arg in opts:
		if opt == '-h':
			print 'Usage :'
			print 'Sequence of Commands given below should be run in this sequence only to get the best result.'
			print 'Few commands in the sequence can be skipped. This information will be given along with the command description'
			print 'All commands must be given by the user as an input to the program'
			print 'Command Description is as follows:'
			print '1. Show_Topology/ST/st : This input command will show the GUI format of the physical topology of the switches'
			print '2. Show_Rings_Automated/SRA/sra : This command will show all the possible rings one by one with a time interval of N seconds, N can be provided the user too separated with a comma. for eg: \'sra,<N>\''
			print '3. Show_Rings_Manually/SRM/srm :  This command will show all the possible rings one by one manually by the user'
			print '4. Show_Optimal_Ring/SOR/sor : This command will show the optimal ring. It will select that cycle which will be having maximum number of nodes. In case of multiple such rings, any one of them will be OR all of them will be shown'
			print '5. Run_Rep_On_Optimal_Ring/RROR/rror : This command will run rep protocal on oprimal ring, and output will be shown on the terminal'
			print '6. showrep_topology/srt : This command shows the rep configuration on optimal ring, and output will be shown on terminal'
			print '7. Restore_Topology/RT/rt : With the use of this command we can reset the data and run whole program from the beginning. Note: This command is required to run only when command 5 has been executed on the Ring, else not required'
			print '8. Quit/Q/q : Quit the program'

			 


#to show Topology GUI on the screen
def show_topology():
	
	cv2.startWindowThread()
	img = cv2.imread('graph.png',0)
	cv2.namedWindow('dst_rt', cv2.WND_PROP_FULLSCREEN)
	cv2.setWindowProperty('dst_rt', cv2.WND_PROP_FULLSCREEN, cv2.cv.CV_WINDOW_FULLSCREEN)
	cv2.imshow('dst_rt',img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()	
	for i in range (1,5):
    		cv2.waitKey(1)
	
#to show all the possible rings of the topology. 
#view to different rings can be automated with time interval set by the user
#and it can be manual, by clicking arrow button to go to next image
def show_rings(timer):
	print "Press q or Q to quit"
	time.sleep(2)
	timer = timer * 1000
	
	cv2.namedWindow('dst_rt', cv2.WND_PROP_FULLSCREEN)
	cv2.setWindowProperty('dst_rt', cv2.WND_PROP_FULLSCREEN, cv2.cv.CV_WINDOW_FULLSCREEN)	
	
	if len(rings_list)>0:
		for i in range(1,len(rings_list)+1):
			name='ring'+str(i)+'.png'
			img = cv2.imread(name,0)
			cv2.imshow('dst_rt',img)
			ch=cv2.waitKey(timer)
			if ch==81 or ch==113:
				break			
	else:
		print "No rings are there in Physical Topology"
		sys.exit(0)
	cv2.destroyAllWindows()
	for i in range (1,5):
    		cv2.waitKey(1)	
    		
#to show all optimal rings, here optimal ring means that ring having maximum number of nodes
def show_optimal_ring():
	print "Press q or Q to quit"
	time.sleep(2)
	
	global rings_list
	max_nodes=0
	i=0
	optimal_rings = []
	for ring in rings_list:
		if len(ring) > max_nodes:
			max_nodes = len(ring)
	
	cv2.namedWindow('dst_rt', cv2.WND_PROP_FULLSCREEN)
	cv2.setWindowProperty('dst_rt', cv2.WND_PROP_FULLSCREEN, cv2.cv.CV_WINDOW_FULLSCREEN)	
	for ring in rings_list:
		if max_nodes == len(ring):
			i += 1
			ring_object,isMultigraph=gui.Network_graph.makeGraph(ring) 
			optimal_rings.append(ring_object)	
			gui.Network_graph.drawTopology(ring_object,False,'optimal_ring'+str(i)+'.png')
			img = cv2.imread('optimal_ring'+str(i)+'.png',0)
			cv2.imshow('dst_rt',img)
			ch=cv2.waitKey(0)
			if ch==81 or ch==113: 
				break

			
	cv2.destroyAllWindows()
	for i in range (1,5):
    		cv2.waitKey(1)
	return optimal_rings


#to run rep on any one optimal ring
def rror(topology, opt_rings):
	rep.Rep_configuration.disable_switch(topology)
	#for ring in opt_rings:
	rep.Rep_configuration.repp(opt_rings[0])
	print "wait for 10 seconds for rep to configure"
	bar.start()
	for i in range(0,10):
		bar.update((i+1)*10)
		time.sleep(1)
	bar.finish()	

#to restore the initial settings of the switches
def restore_topology():
	graph=load.loadObject('Physicalobject.txt')
	rep.Rep_configuration.restore(graph)

def showrep_topology(opt_rings):
	rep.Rep_configuration.showrepp(opt_rings[0])
	
	

#it will handle all the erorrs and warnings 
def errhandler(command):
	if command == "sra" or command == "srm":
		print "Warning : Please Run Show_topology command first"

	elif command == "sor":
		if not Topo_Flag:
			print "Warning : It seems you have not run \'st\' and \'show_ring\' command before running this command"
		elif not Ring_Flag:
			print "Warning : Please run show ring command first"
		
	elif command == 'rror':
		if not Topo_Flag:
			print "Warning : It seems you have not run \'st\' and \'show_ring\' and not even show optimal ring command before running this command. you need to have an optimal ring to rum rror command on"
		elif not Ring_Flag:
			print "Warning : Before running rror command, run show ring and then show optimal ring command"
		elif Optimal_Flag:
			print "Warning : Please find an optimal ring first, run show optimal ring command. take help of the script"

	elif command == 'showrep':
		if not Topo_Flag:
			print "Warning : It seems you have not run \'st\' and \'show_ring\' and not even show optimal ring command and not run_rep_on_optimal_ring command before running this command. you need to have an rep configured on optimal ring to run showrep command on"			
		elif not Ring_Flag:
			print "Warning : Before running showrep command, run show ring, show optimal ring command and then run run_rep_on_optimal_ring "
		elif not Optimal_Flag:
			print "Warning : Please find an optimal ring first, run show optimal ring command and then run run_rep_on_optimal_ring"
				
	elif command == "rt":
		print "Warning : If you have run rror command, then there is no need to run restore command" 
	



#Entry point of the program

try:
	opts, args = getopt.getopt(sys.argv[1:],"hel")
except getopt.GetoptError:
	print 'To Take the help, Run command : \"python Self_Forming_Rings.py\" -h'
	sys.exit(2)

if len(opts) > 0:
	get_args(opts)
	sys.exit(1)
	
#start the progressbar	
bar.start()
Userlogger.info('\n\n\t'+'  ' + str(datetime.datetime.now()) )
# get topology
fout=open('4.txt','r')
lines=fout.readlines()

i=0
while i<len(lines):
	try:
		line=lines[i]
		Switch = mt.Network_topology(line.split()[0],line.split()[1])
		Switch.cdpread()		
		i+=1
		#bar update
		bar.update((.4*barlen)*(i)/len(lines))
	except:
		pass
		
mt.Network_topology.eList_Modify()

#draw Physical Topology	
Userlogger.info('\nCreating networkx object of the physical topology')
topology,isMultigraph=gui.Network_graph.makeGraph(mt.Network_topology.EdgeList)
Userlogger.info('Drawing the physical topology through networkx object')
gui.Network_graph.drawTopology(topology,isMultigraph,'graph.png')

#bar update
bar.update((.2*barlen))

#saving object of Physicaltopology
save.saveObject(topology,'Physicalobject.txt')
	
# get the rings  
rings_list = getAllRings(topology, isMultigraph)
rings_list = formatCycleEdgeList(topology, isMultigraph, rings_list, mt.Network_topology.SwitchList)
#bar update
bar.update(.4*barlen+(.2*barlen))

i = 0
ring_nx=[]
for ring in rings_list:
	i += 1
	ring_object,isMultigraph=gui.Network_graph.makeGraph(ring) 
	ring_nx.append(ring_object)
	gui.Network_graph.drawTopology(ring_object,False,'ring'+str(i)+'.png')
	#bar update
	bar.update(.6*barlen+(.4*barlen)*(i)/len(rings_list))

	
Topo_Flag=False
Ring_Flag=False
Optimal_Flag=False
Rep_Flag=False

Take_Action =  {
	"show_topology" : show_topology,
	"st" : show_topology,
	"show_rings_automated" : show_rings,
	"sra" : show_rings,
	"show_rings_manually" : show_rings,
	"srm" : show_rings, 
	"show_optimal_ring" : show_optimal_ring,
	"sor" : show_optimal_ring,
	"run_rep_on_optimal_ring" : rror,
	"rror" : rror,
	"restore_topology" : restore_topology,
	"rt" : restore_topology,
	"quit" : quit,
	"q" : quit,
	"showrep" :showrep_topology,
	"srt":showrep_topology 
}

#end the bar
bar.finish()

opt_rings = None

while True:
	print 'What would like to run?'
	inputs = raw_input("Command : ")
	inputs = inputs.lower()


	if inputs == "show_Topology" or inputs == "st":
		Topo_Flag = True
		Take_Action.get(inputs,errhandler)()
		
	elif inputs == "show_rings_automated" or inputs == "sra":
		if Topo_Flag:
			while True:
				print 'Please enter the time interval (in seconds) for automated graph representation'	
				timer = raw_input()
				if RepresentsInt(timer):
					break
				else:
					print 'Please enter the integer value only'

			t = int(timer)
			Take_Action.get(inputs,errhandler)(t)
			Ring_Flag = True
		else:
			inputs = "dummy"
			Take_Action.get(inputs,errhandler)("sra")	

	elif inputs == "show_rings_manually" or inputs == "srm":
		if Topo_Flag:
			Take_Action.get(inputs,errhandler)(0)
			Ring_Flag = True
		else:
			inputs = "dummy"
			Take_Action.get(inputs,errhandler)("srm")

	elif inputs == "show_optimal_ring" or inputs == "sor":
		if Topo_Flag and Ring_Flag:
			opt_rings = Take_Action.get(inputs,errhandler)()
			Optimal_Flag = True
		else:
			inputs = "dummy"
			Take_Action.get(inputs,errhandler)("sor")

	elif inputs == "run_rep_on_optimal_ring" or inputs == "rror":
		if Topo_Flag and Ring_Flag and Optimal_Flag:
			Take_Action.get(inputs,errhandler)(topology,opt_rings)
			Rep_Flag = True
		else:
			inputs = "dummy"
			Take_Action.get(inputs,errhandler)("rror")

	elif inputs =="showrep" or inputs =="srt":
		if Topo_Flag and Ring_Flag and Optimal_Flag:
			Take_Action.get(inputs,errhandler)(opt_rings)
		else:
			inputs = "dummy"
			Take_Action.get(inputs,errhandler)("showrep")

	elif inputs == "restore_topology" or inputs == "rt":
		if Rep_Flag:
			Take_Action.get(inputs,errhandler)()
		else:
			inputs = "dummy"
			Take_Action.get(inputs,errhandler)("rt")

	elif inputs == "quit" or inputs == "q":
		sys.exit(0)

	else:
		print "Use -h to see the usage of the script"

			


