import numpy as np
from math import pi

class PhantomX():
	def __init__(self):
		self.d = np.array([40,0,0,0])
		#self.theta = np.array([0,0,0,0])
		self.a = np.array([0,105,105,105])
		self.alpha = np.array([pi/2,0,0,0])

	def T0e(self,theta):
		cost = np.cos(np.radians(theta))
		sint = np.sin(np.radians(theta))
		cosa = np.cos(self.alpha)
		sina = np.sin(self.alpha)
		T_total = np.eye(4) #matrix([1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1])
		for i in range(4):
			T = np.matrix([\
				[ cost[i], -sint[i]*cosa[i], sint[i]*sina[i], self.a[i]*cost[i]],\
				[ sint[i],  cost[i]*cosa[i],-cost[i]*sina[i], self.a[i]*sint[i]],\
				[       0,          sina[i],         cosa[i],         self.d[i]],\
				[       0,                0,               0,                 1]],np.float16)
			T_total = np.matmul(T_total,T)
		return T_total

	def Te0(self,theta):
		T = self.T0e(theta)
		return np.linalg.inv(T)

if __name__ == '__main__':
	arm = PhantomX()
	theta = [90,0,52,33]
	T = arm.Te0(theta)
	print(T)