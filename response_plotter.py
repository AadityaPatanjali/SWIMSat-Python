import matplotlib.pyplot as plt
import numpy as np

def main():
	file = open('Response.txt','r')
	line = file.read()
	file.close()
	var = np.int_([ele.rstrip('])') for ele in [ele.strip(' array([') for ele in (line.strip('[]').split(','))]])
	var_len = len(var)/3
	print(var_len)
	var_new = (var.reshape(var_len,3))[:,0:2]
	plt.plot(range(var_len),var_new)
	plt.axis([0,var_len,np.min(var_new),np.max(var_new)])
	plt.grid(True)
	plt.xlabel('Sample')
	plt.ylabel('Pixel Difference')
	plt.title('System Response')
	plt.legend(['x','y'])
	plt.show()

if __name__ == '__main__':
	main()