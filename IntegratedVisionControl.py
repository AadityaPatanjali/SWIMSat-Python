import sys
import numpy as np
import time
import threading
from threading import Thread
from RobotVision import RobotVision
from PhantomXController import PhantomXController
from PID import PID

class IntegratedVisionControl():

	def __init__(self,delay=0.01,P=4.0,I=0.05,D=0.5,args='/dev/ttyUSB0'):
		self.tlock = threading.Lock()
		self.vision = RobotVision()
		self.initController(args)
		self.threadImage = Thread(target=self.runImage)
		self.curr_time = None
		self.setDelay(delay)
		self.out = []
		self.pan = PID(P,I,D)
		self.tilt = PID(P,I,D)
		self.exit = False
		self.thread = Thread(target=self.run)
		# self.threadImage.start()
		# print('ThreadImage executed')
		self.thread.start()
		self.runImage()

	def __del__(self):
		print('Goodbye!')
		sys.exit()

	def runImage(self):
		self.vision.main()
		self.exit = True
		print "exit = ", self.exit
		file = open('Response.txt','w')
		file.write(str(self.out))
		file.close()
		self.arm.__del__()

	def setDelay(self,delay):
		self.delay = delay

	def run(self,wait=True):
		homingCount = 0
		max_error = 50
		max_homing_count = 1000
		while True:
			if self.exit:
				self.arm.returnHome(interpolate=False)
				self.__del__()
				break
			try:
				# print np.where(max(error)>max_error)
				time.sleep(self.delay)
				error = self.vision.getError();
				self.out.append(error)
				if not error[2]:
					homingCount +=1
					if homingCount >= max_homing_count:
						homingCount = 0
						self.arm.returnHome(interpolate=False)
						break
				else:
					print error
					pan = self.pan.update(error[0]/256.0*2.0)
					tilt = self.tilt.update(error[1]/256.0*2.0)
					# print pan,tilt, count
					if wait:
						self.tlock.acquire()
					self.arm.move(pan,tilt,interpolate=False)
					if wait:
						self.tlock.release()
			except KeyboardInterrupt:
				return

	def initController(self,args):
		try:
			print args
			port = args
			self.arm = PhantomXController(port)
		except IndexError:
			self.arm = PhantomXController()
		try:
			self.arm.getHomePose()

		except KeyboardInterrupt:
			print('...\nExiting')

if __name__=='__main__':
	system = IntegratedVisionControl(args=sys.argv[1])
	system.thread.join()
