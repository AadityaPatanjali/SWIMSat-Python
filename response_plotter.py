import matplotlib.pyplot as plt
import numpy as np

def main():
	# file = open('Response.txt','r')
	file = open('Object_center.txt','r')
	line = file.read()
	file.close()
	var = np.int_([ele.rstrip('])') for ele in [ele.strip(' array([') for ele in (line.strip('[]').split(','))]])
	var_len = int(len(var)/3)
	var_new = (var.reshape(var_len,3))[:,0:2]
	f = plt.figure(1)
	plt.plot(range(var_len),var_new)
	plt.axis([0,var_len,np.min(var_new),np.max(var_new)])
	plt.grid(True)
	plt.xlabel('Sample')
	plt.ylabel('Pixel Value')
	# plt.title('System Error Plot')
	plt.title('Object Position with time')
	plt.legend(['x','y'])

	# file = open('ActualPosOfObj.txt','r')
	file = open('Camera_center.txt','r')
	line = file.read()
	file.close()
	var = np.int_([ele.rstrip('])') for ele in [ele.strip(' array([') for ele in (line.strip('[]').split(','))]])
	var_len = int(len(var)/3)
	var_new = (var.reshape(var_len,3))[:,0:2]
	f2 = plt.figure(2)
	plt.plot(range(var_len),var_new)
	plt.axis([0,var_len,np.min(var_new),np.max(var_new)])
	plt.grid(True)
	plt.xlabel('Sample')
	plt.ylabel('Pixel Value')
	# plt.title('Actual Position Plot')
	plt.title('Camera Position with time')
	plt.legend(['x','y'])

	f.show()
	f2.show()
	raw_input()

if __name__ == '__main__':
	main()