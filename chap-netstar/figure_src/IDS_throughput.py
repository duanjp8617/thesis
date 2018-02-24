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

	CS = [2040618, 1014537, 535532, 142204, 36029]
	IDS_smp10 = [2039614, 1014520, 535529, 142101, 36029]
	IDS_smp1 = [569421, 565976, 486516, 142119, 36028]

	ns1core = [0.79, 5.09, 9.16]
	mos1core = [0.83, 5.10, 9.16]
	netstar6core = [3.94, 9.15, 9.16]
	mos6core = [3.95, 9.14, 9.15]

	plt.style.use('ggplot')#seaborn-white')

	fig,ax1 = plt.subplots()
	fig = plt.figure(1)

	runtimes = [1,2,3,4,5,6,7,8,9,10,11,12]
	colors = ['r','b','y','m','c','g','r','b','y']
	styles = ['-.', '--', ':', '-', '--', ':', '-','--']
	index = 0;

	x = np.arange(3)
	labels= ["7Byte","1KB","8KB"]

	width = 0.2
	ax1.bar(x+1*width, ns1core, width, label="Netstar 1thread", hatch="\\")
	ax1.bar(x+2*width, mos1core, width, label="mOS 1thread", hatch="")
	ax1.bar(x+3*width, netstar6core, width, label="Netstar 6threads", hatch="/")
	ax1.bar(x+4*width, mos6core, width, label="mOS 6threads", hatch="*")

	plt.xticks(x+2*width,labels)
	for tl in ax1.get_xticklabels():
		tl.set_fontsize(20)
		tl.set_fontstyle('normal')
	for tl in ax1.get_yticklabels():
		tl.set_fontsize(20)
		tl.set_fontstyle('normal')

	# Now add the legend with some customizations.
	legend = ax1.legend(loc='upper left', shadow=False)
	# Set the fontsize
	for label in legend.get_texts():
		label.set_fontsize(15)

	for label in legend.get_lines():
		label.set_linewidth(3)  # the legend line width

	plt.xlabel("HTTP response payload size", fontsize=25, style='normal', color='black')
	plt.ylabel("Throughput(Gbps)", fontsize=25, style='normal', color='black')
	plt.savefig("IDS_throughput.pdf", bbox_inches='tight', pad_inches=0)
	plt.show()

def main():

	#runtimes,received,dropped,time = read_log("temp")

	draw()



if __name__ == "__main__" :
	main()
