import pickle
from CreateDebugLog import Userlogger, Debuglogger

def saveObject(obj, filename):
	"""This function saves the given object into persistent storage to the given filename using pickle"""
	Userlogger.info('\nSaving networkx object of the physical topology through pickle module in '+str(filename))

	output = open(filename,'wb')
	pickle.dump(obj,output)
	output.close()
	
def loadObject(filename):
	"""This function returns the object stored in the given pickle file"""
	Userlogger.info('\nLoading networkx object of the physical topology from  '+str(filename))
	pickle_file = open(filename,'rb')
	data = pickle.load(pickle_file)
	pickle_file.close()
	return data
	
