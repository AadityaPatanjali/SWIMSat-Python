import matplotlib.pyplot as plt
import numpy as np

def main():
	file = open('Response.txt','r')
	line = file.read()
	file.close()
	var = np.int_([ele.rstrip('])') for ele in [ele.strip(' array([') for ele in (line.strip('[]').split(','))]])
	var_len = int(len(var)/3)
	var_new = (var.reshape(var_len,3))[:,0:2]
	f = plt.figure(1)
	t =  np.array(range(var_len))*0.01*20
	plt.plot(t,var_new)
	# plt.axis([0,var_len,np.min(var_new),np.max(var_new)])
	plt.grid(False)
	plt.xlabel('Time (s)')
	plt.ylabel('Relative position (pixels)')
	# plt.title('System Error Plot')
	# plt.title('Object Position with time')
	plt.legend(['x','y'])

	# file = open('ActualPosOfObj.txt','r')
	# line = file.read()
	# file.close()
	# var = np.int_([ele.rstrip('])') for ele in [ele.strip(' array([') for ele in (line.strip('[]').split(','))]])
	# var_len = int(len(var)/3)
	# var_new = (var.reshape(var_len,3))[:,0:2]
	f2 = plt.figure(2)
	# plt.plot(range(var_len),var_new)
	# plt.axis([0,var_len,np.min(var_new),np.max(var_new)])
	# t = 0.01*np.array(range(var_len))
	plt.plot(t,[np.linalg.norm(ele) for ele in var_new])
	plt.grid(False)
	plt.xlabel('Time (s)')
	plt.ylabel('Error (pixels)')
	# plt.title('Actual Position Plot')
	# plt.legend(['Euclidian distance'])

	f.show()
	f2.show()
	raw_input()

def main2():
	file = open('Response.txt','r')
	line = file.read()
	file.close()
	var = np.int_([ele.rstrip('])') for ele in [ele.strip(' array([') for ele in (line.strip('[]').split(','))]])
	var_len = int(len(var)/3)
	var_new = (var.reshape(var_len,3))[:,0:2]
	# var_new[:,0] = [ele + 320 if ele>0 else ele for ele in var_new[:,0]]
	# var_new[:,1] = [ele + 240 if ele>0 else ele for ele in var_new[:,1]]
	f = plt.figure(1)
	t =  np.array(range(var_len))*0.01*8
	
	file2 = open('PredTraj.txt','r')
	line2 = file2.read()
	file2.close()
	var2 = np.float_([ele.rstrip('])') for ele in [ele.strip(' array([') for ele in (line2.strip('[]').split(','))]])
	var_len2 = int(len(var2)/3)
	var_new2 = (var2.reshape(var_len2,3))[:,0:2]
	t2 = np.array(range(var_len2))*0.01*8

	plt.plot(t,var_new[:,0])
	plt.plot(t2,var_new2[:,0])
	# plt.axis([0,var_len,np.min(var_new),np.max(var_new)])
	plt.grid(False)
	plt.xlabel('Time (s)')
	plt.ylabel('Position (pixels)')
	plt.legend(['actual traj X','predicted traj X'])

	f2 = plt.figure(2)

	plt.plot(t,var_new[:,1])
	plt.plot(t2,var_new2[:,1])
	# plt.axis([0,var_len,np.min(var_new),np.max(var_new)])
	plt.grid(False)
	plt.xlabel('Time (s)')
	plt.ylabel('Position (pixels)')
	plt.legend(['actual traj Y','predicted traj Y'])

	f3 = plt.figure(3)
	plt.plot(t,[np.linalg.norm(ele) for ele in var_new])
	plt.plot(t2,[np.linalg.norm(ele) for ele in var_new2])
	plt.grid(False)
	plt.xlabel('Time (s)')
	plt.ylabel('Position (pixels)')
	plt.legend(['actual traj','predicted traj'])

	f.show()
	f2.show()
	f3.show()
	raw_input()

if __name__ == '__main__':
	main()