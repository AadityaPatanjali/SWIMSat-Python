#!/usr/bin/env python

import sys
import serial
import numpy as np
import time
from ax12 import *
from driver import Driver
from math import pi

class PhantomXController():

	def __init__(self,port = None,pan = 0,tilt = 3,gripper = 4):
		self.portName = port
		self.baud = 38400
		self.numServos = 5
		self.min_move = 0.1
		np.set_printoptions(precision=2)
		self.doPort()
		self.loadServos()
		self.setPan(pan)
		self.setTilt(tilt)
		self.setGripper(gripper)
		self.homePose = None
		self.setPoseLimits()
		self.setInterpolation()

	###########################################################################
	# Port Manipulation
	def findPorts(self):
		""" return a list of serial ports """
		self.ports = list()
		# windows first
		for i in range(20):
			try:
				s = serial.Serial("COM"+str(i))
				s.close()
				self.ports.append("COM"+str(i))
			except:
				pass
		if len(self.ports) > 0:
			return self.ports
		# mac specific next:		
		try:
			for port in os.listdir("/dev/"):
				if port.startswith("tty.usbserial"):
		 			self.ports.append("/dev/"+port)
		except:
			pass
		# linux/some-macs
		for k in ["/dev/ttyUSB","/dev/ttyACM","/dev/ttyS"]:
				for i in range(6):
					try:
						s = serial.Serial(k+str(i))
						s.close()
						self.ports.append(k+str(i))
					except:
						pass
		return self.ports

	def doPort(self):
		""" open a serial port """
		if self.portName == None:
			self.findPorts()
			print "\nAvailable ports are:" + str(self.ports) + "\n"
			try:
				index = int(input('Enter index of desired port from the list(First index is 0): '))
				self.portName = self.ports[index]
			except:
				print "Please select a valid port."
				return
		try:
			# print "Opening port: " + self.portName + "\n"
			# TODO: add ability to select type of driver
			self.port = Driver(self.portName, self.baud, True) # w/ interpolation
			print "Setting port: " + self.portName + " @",self.baud, "baud\n"
		except:
			self.port = None
			print "No valid port selected/found. Please check if the arm is plugged in/if permissions have been set: \nTry:\n sudo chown <your_username> /dev/<desired_port>"
			return
	
	def loadServos(self):
		print "Reading initial servo values:\n"
		self.servos = np.zeros([self.numServos,2],dtype=np.int)
		for servo in range(self.numServos):
			self.servos[servo] = self.port.getReg(servo+1,P_PRESENT_POSITION_L, 2)

	def setPan(self,pan):
		self.panIdx = pan

	def setTilt(self,tilt):
		self.tiltIdx = tilt

	def setGripper(self,gripper):
		self.gripperIdx = gripper

	def setPoseLimits(self):
		self.qmax = np.ones(self.numServos)*pi
		self.qmin = np.ones(self.numServos)*(-pi)

	def checkPoseValid(self,pose):
		if np.sum(pose[0:len(pose)-1])<pi:
			return True
		else:
			return False

	def doRelax(self):
		""" Relax servos so you can pose them. """
		if self.port != None:
			print "PyPose: relaxing servos..."
			for servo in range(self.numServos):
				self.port.setReg(servo+1,P_TORQUE_ENABLE, [0,])
		else:
			print "Port not selected."
			self.doPort()

	def relaxServos(self):
		""" Relax or enable a servo. """
		for servo in range(self.numServos):
			self.port.setReg(servo+1, P_TORQUE_ENABLE, [0,])

	def enableServos(self):
		for servo in range(self.numServos):
			self.port.setReg(servo+1,P_TORQUE_ENABLE, [1,])

	def convertToAngles(self):
		values = np.zeros(self.numServos,dtype=np.int)
		for servo,val in zip(self.servos,range(self.numServos)):
			values[val] = servo[0]+servo[1]*256
		values = values/1024.0*360.0-180.0
		return values

	def convertToPose(self,values):
		values = np.int_(np.round((values+180.0)/360.0*1024.0))
		servos = np.zeros([self.numServos,2],dtype="int")
		for pos in range(len(values)):
			servos[pos,:] = [values[pos]%256,values[pos]>>8]
		return servos

	def convertTo1024(self,values):
		return np.int_(np.round((values+180.0)/360.0*1024.0))

	def moveWithInterpolation(self,pose):
		# set pose size -- IMPORTANT!
		print "Setting pose size yo "+str(self.numServos)
		self.port.execute(253, 7, [self.numServos])
		# download the pose
		print "\n\n\n\n\n\n",pose
		self.port.execute(253, 8, [0] + pose)
		self.port.execute(253, 9, [0, self.deltaT%256,self.deltaT>>8,255,0,0])
		self.port.execute(253, 10, list())

	###########################################################################
	# Pose Manipulation
	def setPose(self,pose,interpolate=False):
		if interpolate:
			# print self.servos[1]
			# for servo in range(self.numServos):
			# 	self.port.setReg(servo+1, P_GOAL_POSITION_L, self.servos[servo,:].tolist())
			self.enableServos()
			self.port.interpolate = True
			flat_pose = [item for sublist in pose for item in sublist]
			print "Moving slowly", flat_pose
			self.moveWithInterpolation(flat_pose)
		else:	
			for servo in range(self.numServos):
				self.port.setReg(servo+1, P_GOAL_POSITION_L, pose[servo].tolist())

	def setPoseInAngles(self,pose,interpolate=False):
		self.setPose(self.convertToPose(pose),interpolate)

	def getPose(self):  
		""" Downloads the current pose from the robot. """
		# errors = "could not read servos: "
		# errCount = 0.0
		self.port.setDisplay(False)
		for servo in range(self.numServos):
			self.servos[servo,:] = self.port.getReg(servo+1,P_PRESENT_POSITION_L, 2)

	def setInterpolation(self,deltaT=500):
		# deltaT is in ms
		self.deltaT = deltaT

	def move(self,pan,tilt,gripper = 0,interpolate=False):
		if (abs(pan)<self.min_move) | (abs(tilt)<self.min_move):
			return
		# Pan and Tilt are in degrees
		self.getPose()
		poseInit = self.convertToAngles()
		# print "Initial angles: ",poseInit
		poseFinal = np.zeros(self.numServos,dtype=np.int)
		poseFinal[self.panIdx] = pan
		poseFinal[self.tiltIdx] = tilt
		poseFinal[self.gripperIdx] = gripper
		poseFinal = poseFinal + self.convertToAngles()
		# print "  Final angles: ",poseFinal
		# time.sleep(5)
		if self.checkPoseValid(poseFinal):
			self.setPose(self.convertToPose(poseFinal),interpolate)
		else:
			print "Pose out of bounds"

	def returnHome(self,interpolate=False):
		print "Returning to Home Position"
		self.setPoseInAngles(self.homePose,interpolate)

	def setHomePose(self,interpolate = False):
		self.relaxServos()
		while True:
			try:
				self.getPose()
				pose = self.convertToAngles()
				print (pose)
				time.sleep(0.5)
			except KeyboardInterrupt:
				break
		print "Setting home position to:",pose
		inp = raw_input("Ok? Y/N:").lower()
		if inp == "y":
			self.setPose(self.convertToPose(pose),interpolate)
			file = open('HomePose','w')
			file.write(str(pose))
			file.close()
			self.homePose = pose
			print "Home position set!"
			return
		elif inp == "n":
			self.setHomePose(interpolate)
		else:
			self.setHomePose(interpolate)

	def getHomePose(self,interpolate = False):
		# self.relaxServos()
		if self.homePose == None:
			try:
				file = open("HomePose",'r')
				line = file.read()
				self.homePose = np.int_(line.strip('[]').split(','))
			except IOError:
				print "Home Position not set yet.\n"
				self.setHomePose()
				return
			except ValueError:
				self.homePose = np.array(line.strip('[]').split()).astype(np.float)
		print "Home Position is: ", self.homePose
		inp = raw_input("Do you want to move to home pos? Y/N:").lower()
		if inp == 'y':
			print "Setting To Home Position"
			self.setPoseInAngles(self.homePose,interpolate)
		elif inp == 'n':
			inp = raw_input("Do you want reset the home pos? Y/N:").lower()
			while inp == 'y':
				if inp == 'y':
					self.setHomePose()
					return
				elif inp == 'n':
					print "Goodbye!"
					break
				else:
					inp = raw_input("Do you want reset the home pos? Y/N:").lower()
		else:
			self.getHomePose(interpolate)

	def setZeroPose(self):
		self.setPoseInAngles(np.zeros(5))

	def __del__(self):
		self.setPoseInAngles(self.homePose,False)
		print('Exiting PhantomXController!')
		# self.relaxServos()

if __name__=='__main__':
	try:
		port = sys.argv[1]
		arm = PhantomXController(port)
	except IndexError:
		arm = PhantomXController()
	try:
		arm.getHomePose()

	except KeyboardInterrupt:
		print('...\nExiting')