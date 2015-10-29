import store as load
import RepConfig as rep

graph=load.loadObject('Physicalobject.txt')
rep.Rep_configuration.restore(graph)	
