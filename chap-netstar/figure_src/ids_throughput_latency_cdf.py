#!/usr/bin/env python2.7
import numpy as np
import math
import matplotlib.pyplot as plt
import random
import os
import optparse
import sys
import subprocess
import signal
import time


def read_file():
	without_ips_sample = []
	with_ips_sample = []

	f = open("stateless_ids_64bytes_100000flows_latency.txt")

	l = f.readlines()

	sample = l[0].split(", ")

	for item in sample:
		print item
		with_ips_sample.append(int(item))
	f.close()

	f = open("cb_ids_64bytes_100000flows_latency.txt")

	l = f.readlines()

	sample = l[0].split(", ")

	for item in sample:
		print item
		without_ips_sample.append(int(item))
	f.close()

	return without_ips_sample, with_ips_sample

def main():

	without_ips_sample, with_ips_sample = read_file()

	without_ips_sample = map(lambda i: float(i)/1000.0, without_ips_sample)
	without_ips_sample = filter(lambda f:f<1000.0, without_ips_sample)
	without_ips_array = np.array(without_ips_sample)

	with_ips_sample = map(lambda i: float(i)/1000.0, with_ips_sample)
	with_ips_sample = filter(lambda f:f<1000.0, with_ips_sample)
	with_ips_array = np.array(with_ips_sample)

	max_us = max(np.amax(without_ips_array), np.amax(with_ips_array))
	bin = np.arange(int(math.ceil(max_us))+1)

	without_ips_hist, without_ips_bin = np.histogram(without_ips_array, bins=bin, density=True)
	with_ips_hist, with_ips_bin = np.histogram(with_ips_array, bins=bin, density=True)

	without_ips_cum = np.append(np.cumsum(without_ips_hist), [1])
	with_ips_cum = np.append(np.cumsum(with_ips_hist), [1])

	#max_us = np.amax(with_ips_array)
	#print max_us
	#bin = np.arange(int(math.ceil(max_us))+1)

	#with_ips_hist, with_ips_bin = np.histogram(with_ips_array, bins=bin, density=True)
	#with_ips_cum = np.append(np.cumsum(with_ips_hist), [1])

	#plt.style.use('ggplot')#seaborn-white')
	#plt.style.use('ggplot')#seaborn-white')
	plt.style.use('ggplot')#seaborn-white')
	plt.style.use('ggplot')#seaborn-white')
	fig,ax1 = plt.subplots()
	fig = plt.figure(1)

	linelabels = ["FW-NAT-LB", "FW-NAT-IPS", "dynamic","HP,FW","FM,FW","FM,HP,FW"]

	ax1.plot(bin.tolist(), with_ips_cum.tolist(),  '--', label='Netstar', linewidth=3)
	ax1.plot(bin.tolist(), without_ips_cum.tolist(),  '-.', label='Callback', linewidth=3)


	ax1.set_ylabel('CDF', fontsize=23, style='normal', color='black')
	ax1.set_xlabel('Processing Latency (microseconds):\nIDS', fontsize=20, style="normal", color='black')

	# Now add the legend with some customizations.
	legend = ax1.legend(loc='lower right', shadow=False)


	# Set the fontsize
	for label in legend.get_texts():
		label.set_fontsize(18)

	for label in legend.get_lines():
		label.set_linewidth(3)  # the legend line width

	for tl in ax1.get_xticklabels():
		tl.set_fontsize(18)
		tl.set_fontstyle('normal')
	for tl in ax1.get_yticklabels():
		tl.set_fontsize(20)
		tl.set_fontstyle('normal')

	#ax1.set_yscale('log') # if want to linearly scale the y axis, comment this line

	plt.savefig("ids_throughput_latency_cdf.pdf", bbox_inches='tight', pad_inches=0)
	plt.show()


if __name__ == "__main__" :
	main()
