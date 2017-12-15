import numpy as np

class Test():
	def __init__(self):
		self.numServos = 5

	def poseToAngles(self,servos = None):
		servos = self.servos if servos is None else servos
		values = np.zeros(self.numServos,dtype=np.int)
		for servo,val in zip(servos,range(self.numServos)):
			values[val] = servo[0]+servo[1]*256
		values = values/1024.0*360.0-180.0
		return values

	def anglesToPose(self,values):
		values = np.int_(np.round((values+180.0)/360.0*1024.0))
		servos = np.zeros([self.numServos,2],dtype="int")
		for pos in range(len(values)):
			servos[pos,:] = [values[pos]%256,values[pos]>>8]
		return servos

	def anglesTo1024(self,values):
		return np.int_(np.round((values+180.0)/360.0*1024.0))

	def _1024ToAngles(self,values):
		return np.array(values)/1024.0*360.0-180.0

if __name__ == '__main__':
	test = Test()
	pose = input('Enter pose values in 1024: ')
	print test._1024ToAngles(pose)