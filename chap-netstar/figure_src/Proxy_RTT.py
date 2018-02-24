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

	CS = [21649, 24585, 28179, 71076, 278111]
	seastar_native = [49107, 55025, 68903, 94756, 281269]
	seastar_kernel = [84416, 100494, 109481, 298664, 374623]
	HAProxy = [85104, 101898, 111997, 250670, 382917]
	Tinyproxy = [697969, 665676, 730122, 937572, 2807009]
	CS = map(lambda f:f/1000.0, CS)
	seastar_native = map(lambda f:f/1000000.0, seastar_native)
	seastar_kernel = map(lambda f:f/1000000.0, seastar_kernel)
	HAProxy = map(lambda f:f/1000000.0, HAProxy)
	Tinyproxy = map(lambda f:f/1000000.0, Tinyproxy)
#	nfa=map(float,nfa)
#	base_line=[4171072,4155680,3486624,2332160,1192747]
#	base_line=map(float,base_line)
#	nfa=map(float,nfa)

	plt.style.use('ggplot')#seaborn-white')

	fig,ax1 = plt.subplots()
	fig = plt.figure(1)

	runtimes = [1,2,3,4,5,6,7,8,9,10,11,12]
	colors = ['r','b','y','m','c','g','r','b','y']
	styles = ['-.', '--', ':', '-', '--', ':', '-','--']
	index = 0;

	x = np.arange(5)
	labels= ["7Byte","1KB","2KB","8KB","32KB"]

	width = 0.2
	#ax1.bar(x+width, CS, width, label="without proxy", hatch="/")
	ax1.bar(x+1*width, seastar_native, width, label="NetStar", hatch="\\")
	ax1.bar(x+2*width, HAProxy, width, label="HAProxy", hatch="|")
	#ax1.bar(x+4*width, seastar_kernel, width, label="NetStar (kernel stack)", hatch="|")
	ax1.bar(x+3*width, Tinyproxy, width, label="Tinyproxy",hatch="")

	plt.xticks(x+2.5*width,labels)
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
		label.set_fontsize(20)

	for label in legend.get_lines():
		label.set_linewidth(3)  # the legend line width

	plt.xlabel("HTTP response\npayload size", fontsize=25, style='normal', color='black')
	plt.ylabel("HTTP Transaction\nCompletion Time(us)", fontsize=25, style='normal', color='black')
	plt.savefig("Proxy_RTT.pdf", bbox_inches='tight', pad_inches=0)
	plt.show()

def main():

	#runtimes,received,dropped,time = read_log("temp")

	draw()



if __name__ == "__main__" :
	main()
