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
	tp = []
	i = 0
	with open(filename) as f:
		for line in f:
			i+=1
			print line
			tp.append(float(line))
			if i==50 :
				break
	return tp

def draw(l1, l2, without_ips_sum_libcaf, with_ips_sum_libcaf):
	l1 = map(lambda i : (float(i)/1000000.0), l1)
	l2 = map(lambda i : (float(i)/1000000.0), l2)

	lines = [l1,l2]

	#plt.style.use('ggplot')#seaborn-white')
	#plt.style.use('ggplot')#seaborn-white')
	fig,ax1 = plt.subplots()
	fig = plt.figure(1)

	l1_x = [1, 2, 3, 4, 5, 6]
	l2_x = [1, 2, 3, 4, 5, 6]
	colors = ['r','b','y','m','c','g','r','b','y']
	styles = ['s-.', 'o--', '<:', '^:', 'D:', 'p:', 'x:','*:']
	index = 0;
	line_index = 0;
	linelabels = ["FW-NAT-LB", "FW-NAT-IPS", "FW-NAT-LB,\nlibcaf","HP,FW","FM,FW","FM,HP,FW"]

	ax1.plot(l1_x, l1,  's-.', label=linelabels[0], linewidth=3,  markersize=10)
	ax1.plot(l2_x, l2,  'o--', label=linelabels[1], linewidth=3,  markersize=10)
	ax1.plot(l2_x, without_ips_sum_libcaf,  '<:', label=linelabels[2], linewidth=3,  markersize=10)
	#ax1.plot(l2_x, with_ips_sum_libcaf,  'o--', label=linelabels[3], linewidth=3)

	ax1.set_ylabel('Throughput(Mpps)', fontsize=23, style='normal', color='black')
	ax1.set_xlabel('# of replication\nsource runtimes', fontsize=23, style="normal", color='black')

	# Now add the legend with some customizations.
	legend = ax1.legend(loc='upper left', shadow=False)


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

	xticks = np.array([1,2,3,4,5,6])
	for i in range(len(xticks)):
		xticks[i] = int(xticks[i])
	ax1.set_xticks(xticks)

	#ax1.set_yscale('log') # if want to linearly scale the y axis, comment this line

	plt.savefig("rep_scaling.pdf", bbox_inches='tight', pad_inches=0)
	plt.show()

def main():

	#without_ips_sum = [1335427.546,1330938.152,1298602.692,1331237.696,1279095.092,1287455.754]
	#with_ips_sum =    [958693.534,960217.2214,953182.6428,967498.4898,965291.0813,963060.8399]

	#without_ips_sum = map(sum, map(lambda i: without_ips_sum[0:i], [1,2,3,4,5,6]))
	#with_ips_sum = map(sum, map(lambda i: with_ips_sum[0:i], [1,2,3,4,5,6]))

	without_ips_sum = [1335427.546, 2666365.698, 3964968.3899999997, 5222421, 5232392.17799999, 5221247.931999999]
	with_ips_sum = [958693.534, 1918910.7554000001, 2872093.3982, 3839591.8880000003, 4804882.9693, 5234124]

	#without_ips_sum_libcaf = [0.201, 0.209, 0.203, 0.202, 0.200, 0.198]
	#with_ips_sum_libcaf    = [0.192, 0.202, 0.205, 0.197, 0.201, 0.217]

	#without_ips_sum_libcaf = map(sum, map(lambda i: without_ips_sum_libcaf[0:i], [1,2,3,4,5,6]))
	#with_ips_sum_libcaf = map(sum, map(lambda i: with_ips_sum_libcaf[0:i], [1,2,3,4,5,6]))

	#print without_ips_sum_libcaf
	#print with_ips_sum_libcaf

	without_ips_sum_libcaf = [0.201, 0.41000000000000003, 0.613, 0.815, 1.015, 1.2129999999999999]
	with_ips_sum_libcaf = [0.192, 0.394, 0.599, 0.796, 0.9970000000000001, 1.2140000000000002]

	draw(without_ips_sum, with_ips_sum, without_ips_sum_libcaf, with_ips_sum_libcaf)

if __name__ == "__main__" :
	main()
