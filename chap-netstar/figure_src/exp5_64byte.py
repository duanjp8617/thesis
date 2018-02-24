#!/usr/bin/env python2.7
import os
import optparse
import sys
import subprocess
import signal
import time
import numpy as np
import matplotlib.pyplot as plt


def read_log(filename):
	runtimes = []
	received = []
	dropped = []
	time = []
	with open(filename) as f:
		for line in f:
			if line.find("[RESULT]") != -1:
				numbers = line.split(' ')
				received.append(float(numbers[1]))
				dropped.append(float(numbers[2]))
				time.append(float(numbers[3]))

	return runtimes, received, dropped, time 

def read_data():
        gpu = []
        memory = []
        r1=0
        r2=0
        i=0

        while i<20:
                time.sleep(0.1)
                p=os.popen('nvidia-smi -i 1 --query-gpu=utilization.gpu --format=csv,noheader','r')
                line=p.readlines()[0]
                r1=int(line.split('%')[0])
                gpu.append(r1)

                q=os.popen('nvidia-smi -i 1 --query-gpu=utilization.memory --format=csv,noheader','r')
                line=q.readlines()[0]
                r2=int(line.split('%')[0])
                memory.append(r2)
                i=i+1
        return gpu,memory
def draw():

	netstar=[6695552,6470112,6503972,2957225]
	netstar = map(lambda f:f/1000000.0, netstar)

#	opennf=map(float,opennf)
	callback=[6844728,6460241,6613238,2956752]
	callback = map(lambda f:f/1000000.0, callback)

	

#	nfa=map(float,nfa)
	
	plt.style.use('ggplot')#seaborn-white')

	fig,ax1 = plt.subplots()
	fig = plt.figure(1)

	runtimes = [1,2,3,4,5,6,7,8,9,10,11,12]
	colors = ['r','b','y','m','c','g','r','b','y']
	styles = ['-.', '--', ':', '-', '--', ':', '-','--']
	index = 0;

	x = np.arange(4)

	
	labels= ["Firewall","Load-balancer","NAT","IDS"]

	width = 0.3
	#x1 = map(lambda f:f+width, x)
	#x2 = map(lambda f:f+2*width, x)

	ax1.bar(x+width, netstar, width, label="Netstar", hatch="/")
	ax1.bar(x+2*width, callback, width, label="Callback", hatch="\\")
	

	plt.xticks(x+1.5*width,labels)
	for tl in ax1.get_xticklabels():
		tl.set_fontsize(15)
		tl.set_fontstyle('normal')
	for tl in ax1.get_yticklabels():
		tl.set_fontsize(20)
		tl.set_fontstyle('normal')

	# Now add the legend with some customizations.
	legend = ax1.legend(loc='upper right', shadow=False)
	# Set the fontsize
	for label in legend.get_texts():
		label.set_fontsize(15)

	for label in legend.get_lines():
		label.set_linewidth(3)  # the legend line width

	plt.xlabel("Input packet size: 64 Byte", fontsize=25, style='normal', color='black')
	plt.ylabel("Throughtput(Mpkts/s)", fontsize=25, style='normal', color='black')
	plt.savefig("StatelessNF_throughput_comparison_64byte.pdf", bbox_inches='tight', pad_inches=0)
	plt.show()

def main():

	#runtimes,received,dropped,time = read_log("temp")

	draw() 



if __name__ == "__main__" :
	main()