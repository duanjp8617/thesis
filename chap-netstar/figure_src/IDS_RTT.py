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

	CS = [486111, 1045915, 1947577, 7657746, 28566036]
	IDS_smp10 = [479520, 993857, 1850917, 7086868, 28046962]
	IDS_smp1 = [1755719, 1763218, 2051872, 7233768, 28282199]

	ns1core = [49.16, 49.11, 202.54]
	mos1core = [48.11, 47.06, 198.4323]
	netstar6core = [13.42, 27.82, 199.50]
	mos6core = [12.74, 28.90, 204.43]

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
	plt.ylabel("HTTP transaction\ncompletion time(ms)", fontsize=25, style='normal', color='black')
	plt.savefig("IDS_RTT.pdf", bbox_inches='tight', pad_inches=0)
	plt.show()

def main():

	#runtimes,received,dropped,time = read_log("temp")

	draw()



if __name__ == "__main__" :
	main()
