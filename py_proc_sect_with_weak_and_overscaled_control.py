from __future__ import division
#import StringIO
import sys, glob, os
import numpy as np
import scipy as sp
from numpy import *

import re 

from scipy.optimize import fsolve
import subprocess

import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rc('text', usetex=True)
mpl.rcParams.update({'font.size': 20})
mpl.rcParams['text.latex.preamble'] = [r'\boldmath']
mpl.rcParams['text.latex.preamble']=[r"\usepackage{amsmath}"]

import scipy.signal

old_path = os.getcwd()
folder = sys.argv[1]
koeff = float(sys.argv[2])
os.chdir(folder)

os.makedirs("weak", exist_ok = True)
os.makedirs("overscaled", exist_ok = True)

filenames_txt = glob.glob('*_*.txt')
filenames_png = glob.glob('*_*.png')

R = 10
XMIN = -1000.0
XMAX = 1000.0
eps = 0.0001
NMAX = 100
NUM_OF_MAX = 20
INIT_MIN_HW = 20 #integer
CONST_FOR_WIDTH = 2.0*np.arccosh(np.sqrt(2.0))

MAX_VAL = 1022

width_arr = np.zeros(len(filenames_txt))
file_count = 0

for filename in filenames_txt:

	data = np.loadtxt(filename)
	print(filename)
		
	filename_splitted = filename.split(".txt")[0]
	f_params = filename_splitted.split('_')[:]
		
	x_max, y_max = np.unravel_index(np.argmax(data), data.shape)

	if data[x_max, y_max] > MAX_VAL:
		os.rename(filename, "overscaled/"z+filename)
		for filename_1 in filenames_png:
			filename_png_splitted = filename_1.split(".png")[0]
			f_png_params = filename_png_splitted.split('_')[:]
			if f_png_params[1:3] == f_params[0:2]:
				os.rename(filename_1, "overscaled/"+filename_1)
				break
		continue
	else:
		s = 0.0
		for i in range(x_max-1,x_max+2):
			for j in range(y_max-1,y_max+2):
				if i != x_max or j != y_max:
					s += data[i,j]

		if data[x_max, y_max] > s/4.0:
			os.rename(filename, "weak/"+filename)
			for filename_1 in filenames_png:
				filename_png_splitted = filename_1.split(".png")[0]
				f_png_params = filename_png_splitted.split('_')[:]
				if f_png_params[1:3] == f_params[0:2]:
					os.rename(filename_1, "weak/"+filename_1)
					break
			continue
	
	indices = data.ravel().argsort()[::-1][:NUM_OF_MAX]
	x_coord, y_coord = unravel_index(indices, data.shape)

	#indices = data.argpartition(data.size - NUM_OF_MAX, axis=None)[-NUM_OF_MAX:][::-1]
	#x_coord, y_coord = unravel_index(indices, data.shape)

	#print("DATA_MAX")
	#for i in range(0, NUM_OF_MAX):
	#	print(x_coord[i], y_coord[i], data[x_coord[i], y_coord[i]])

	s = 0.0
	for i in range(x_coord[0]-1,x_coord[0]+2):
		for j in range(y_coord[0]-1,y_coord[0]+2):
			if i != x_coord[0] or j != y_coord[0]:
				s += data[i,j]
	
	data_coord = [x_coord[0], y_coord[0]]
	i = 0
	while (data[x_coord[i+1], y_coord[i+1]] < 4.0*data[x_coord[i], y_coord[i]]/5.0) or (data[x_coord[i], y_coord[i]] > s/4.0):
		print(i, "TRUE")
		s = 0.0
		i += 1
		for j in range(x_coord[i]-1,x_coord[i]+2):
			for k in range(y_coord[i]-1,y_coord[i]+2):
				if j != x_coord[i] or k != y_coord[i]:
					s += data[j,k]
		data_coord = [x_coord[i], y_coord[i]]
	
	s = x = y = 0.0
	for i in range(data_coord[0] - R-1, data_coord[0] + R+1):
		for j in range(data_coord[1] - R-1, data_coord[1] + R+1):
			if ((i - data_coord[0])**2 + (j - data_coord[1])**2 <= R**2):
				x = x + j * data[i, j]
				y = y + i * data[i, j]
				s = s + data[i, j]
	x = x/s
	y = y/s

	vert_sec = data[:,int(x)]
	hor_sec = data[int(y),:]

	y_arr = np.zeros_like(vert_sec)
	n = 0
	for i in range(-int(y)-1, data.shape[0] - int(y)-1):
		y_arr[n] = koeff*i
		n += 1

	arr_sec = np.array([y_arr, vert_sec])
	arr_sec_1 = np.transpose(arr_sec)
	
	def func(x, I, G, x_0, f_0):
		return I/(cosh(G*(x-x_0)))**2+f_0

	def min_max(width_min_max, minimums):
		flag = 0
		i = 0
		while (flag != 1) and (i+width_min_max < len(right)):
			is_it_min = 1
			for k in range(-width_min_max, width_min_max+1, 1):
				if vert_sec[right[i]+k] < vert_sec[right[i]]:
					is_it_min = 0
					break
			if (is_it_min == 1):
				flag = 1
			i += 1
		if i != 0:
			minimums[1] = right[i-1]
		else:
			minimums[1] = len(vert_sec)-1
		flag = 0
		i = 0
		while (flag != 1) and (i+width_min_max < len(left)):
			is_it_min = 1
			for k in range(-width_min_max, width_min_max+1, 1):
				if vert_sec[left[i]+k] < vert_sec[left[i]]:
					is_it_min = 0
					#print ("num_c = '{0}', num = '{1}', value = '{2}', value_min = '{3}'".format(left[i], left[i]+k, vert_sec[left[i]+k], vert_sec[left[i]]))
					break
			if is_it_min == 1:
					flag = 1
			i += 1
		if i != 0:
			minimums[0] = left[i-1]
		else:
			minimums[0] = 0

		return minimums

	def width_search(G):
		return CONST_FOR_WIDTH/abs(G)

	def width_simple(vert_sec, y_max, bg):
		av_max = np.average(vert_sec[y_max-2:y_max+3])
		height = av_max-bg
		this = av_max
		i = y_max+1
		while i<len(vert_sec)-1 and this >= height/2.0+bg:
			this = vert_sec[i]
			i+=1
			y_max_num = i
		i = y_max-1
		this = vert_sec[i]
		while i>0 and this >= height/2.0+bg:
			this = vert_sec[i]
			i-=1
		y_min_num = i
		return int(y_max_num - y_min_num)

	def running_mean(vert_sec, N):
		cumsum = np.cumsum(np.insert(vert_sec, 0, 0))
		return (cumsum[N:] - cumsum[:-N]) / float(N)

	bg = (np.sum(vert_sec[:10]) + np.sum(vert_sec[-10:]))/20.0
	#print ("bg = %f" % bg)

	#Searching of high maximums
	extrema = np.array(sp.signal.argrelextrema(vert_sec, np.less_equal))
	max_extr = vert_sec.argmax()

	#print ("max_extr = %d" % max_extr)
	right = extrema[extrema>max_extr]
	left = extrema[extrema<max_extr]
	left = left[::-1]
	
	#q = 0
	#for item in np.nditer(extrema, order = 'C'):
	#	print q, item, vert_sec[item]
	#	q += 1

	width = width_simple(vert_sec, max_extr, bg)
	width_min_max = int(width/5.2)
	#width_min_max_1 = width_min_max
	minimums = np.array([max_extr, max_extr])
	minimums = min_max(width_min_max, minimums)

	print("MINIMUMS = %s" % minimums)
	a_1 = (int(minimums[0])-y)*koeff
	a_2 = (int(minimums[1])-y)*koeff
	print("y_min = '{0}', y_max = '{1}'".format(a_1, a_2))
	
	#print ("minimums[0] = %d, minimums[1] = %d, max_extr = %d" % minimums[0], minimums[1], max_extr)

	#Initial fitting
	f_0 = bg
	I = data[data_coord[0], data_coord[1]] - f_0
	G = CONST_FOR_WIDTH/(width*koeff)
	x_0 = 1.0
	
	print("HERE!")

	solutions = np.array([0.0, 0.0])
	solutions_1 = np.array([XMIN, XMAX])

#	x1 = np.arange(solutions_1[0], solutions_1[1], 0.1)
#	plt.figure(figsize=(10.5, 9.0), dpi=600)
#	plt.rcParams['text.latex.preamble'] = [r'\boldmath']
#	plt.plot(y_arr, vert_sec, 'o', markersize='7', color='#000000')
#	plt.plot(x1, func(x1, I, G, x_0, f_0), 'k', color='r', lw='1.5')
#	plt.xlim([XMIN,XMAX])
#	plt.xlabel(r'\textbf{y, $\mu$m}')
#	plt.ylabel(r'\textbf{Amplitude, arb.un.}')
#	plt.grid()
#	#plt.minorgrid_on()
#	plt.minorticks_on()
#	plt.tick_params(axis='x', pad=7)
#	plt.tick_params(axis='y', pad=5)
#	plt.savefig(the_file+".png", bbox_inches='tight')
#	plt.close()

	n = 0
	while (abs(solutions_1[0] - solutions[0]) > eps or abs(solutions_1[1] - solutions[1]) > eps) and n<NMAX:
		j = 0
		y_min_num = -1
		y_max_num = -1
		while (j < y_arr.shape[0]) and (y_arr[j] < solutions_1[1]):
			if (y_arr[j] >= solutions_1[0]) and (y_min_num < 0):
				y_min_num = j
			j += 1
		y_max_num = j-1
		
		solutions[:] = solutions_1[:]
		
		y_min_num = max(y_min_num, minimums[0])
		y_max_num = min(y_max_num, minimums[1])

		print ("n = '{0}', y_min_num = '{1}', y_max_num = '{2}'".format(n, y_min_num, y_max_num))
		b_1 = (int(y_min_num)-y)*koeff
		b_2 = (int(y_max_num)-y)*koeff
		print("y_min = '{0}', y_max = '{1}'".format(b_1, b_2))
		popt, pconv = sp.optimize.curve_fit(lambda x, I, G, x_0: func(x, I, G, x_0, f_0), y_arr[y_min_num:y_max_num], vert_sec[y_min_num:y_max_num], p0 = [I, G, x_0])
		I = popt[0]
		G = popt[1]
		x_0 = popt[2]
		#f_0 = popt[3]
		func_1 = lambda x : I/(cosh(G*(x-x_0)))**2 - I/20.0
		print(I, G, x_0, f_0)
		x_initial_guess = -0.7*abs(1.0/G) + x_0
		solutions_1[0] = fsolve(func_1, x_initial_guess)
		x_initial_guess = 0.7*abs(1.0/G) + x_0
		solutions_1[1] = fsolve(func_1, x_initial_guess)
		#width_min_max_1 = int(width_search(G)/koeff*0.15)
		#minimums = min_max(max(width_min_max, width_min_max_1), minimums)
		#print ("width_min_max = '{0}', width = '{1}', minimums = '{2}'".format(width_min_max, width_search(G), minimums))
		#a_1 = (int(minimums[0])-y)*koeff
		#a_2 = (int(minimums[1])-y)*koeff
		n += 1
		print ("n = %d" % n)
		#print ("solutions = '{0}', solutions_1 = '{1}'".format(solutions, solutions_1))
	
	#Width searching
	width_arr[file_count] = width_search(G)
	#print x_left
	#print x_right
	print ("width = %f" % width_arr[file_count])

	for filename_1 in filenames_png:
		filename_png_splitted = filename_1.split(".png")[0]
		f_png_params = filename_png_splitted.split('_')[:]
		if f_png_params[1:3] == f_params[0:2]:
			the_file = f_png_params[0]+"_"+filename_splitted+"_sec_v"

			x1 = np.arange(solutions_1[0], solutions_1[1], 0.1)
			plt.figure(figsize=(10.5, 9.0), dpi=600)
			plt.rcParams['text.latex.preamble'] = [r'\boldmath']
			plt.plot(y_arr, vert_sec, 'o', markersize='7', color='#000000')
			plt.plot(x1, func(x1, I, G, x_0, f_0), 'k', color='r', lw='1.5')
			plt.xlim([XMIN,XMAX])
			plt.xlabel(r'\textbf{y, $\mu$m}')
			plt.ylabel(r'\textbf{Amplitude, arb.un.}')
			plt.grid()
			#plt.minorgrid_on()
			plt.minorticks_on()
			plt.tick_params(axis='x', pad=7)
			plt.tick_params(axis='y', pad=5)
			plt.savefig(the_file+".png", bbox_inches='tight')
			plt.close()

			file_count += 1

	'''vert_sec_mean = running_mean(vert_sec, N_MEAN)
	plt.figure(figsize=(10.5, 9.0), dpi=600)
	plt.rcParams['text.latex.preamble'] = [r'\boldmath']
	plt.plot(y_arr[2:len(y_arr)-2], vert_sec_mean, 'o', markersize='7', color='#000000')
	plt.xlim([XMIN,XMAX])
	plt.xlabel(r'\textbf{y, $\mu$m}')
	plt.ylabel(r'\textbf{Amplitude, arb.un.}')
	plt.grid()
	#plt.minorgrid_on()
	plt.minorticks_on()
	plt.tick_params(axis='x', pad=7)
	plt.tick_params(axis='y', pad=5)
	plt.savefig(the_file+"mean.png", bbox_inches='tight')
	plt.close()

	'''#vert_sec_diff = np.diff(vert_sec_mean, n=1)
	#plt.figure(figsize=(10.5, 9.0), dpi=600)'''
	'''plt.rcParams['text.latex.preamble'] = [r'\boldmath']
	plt.plot(y_arr[2:len(y_arr)-3], vert_sec_diff, 'o', markersize='7', color='#000000')
	plt.xlim([XMIN,XMAX])
	plt.xlabel(r'\textbf{y, $\mu$m}')
	plt.ylabel(r'\textbf{Amplitude, arb.un.}')
	plt.grid()
	#plt.minorgrid_on()
	plt.minorticks_on()
	plt.tick_params(axis='x', pad=7)
	plt.tick_params(axis='y', pad=5)
	plt.savefig(the_file+"diff.png", bbox_inches='tight')
	plt.close()'''
	
print ("Width average = '{0}'".format(np.mean(width_arr)))
print ("Width std. err. = '%f'" % np.std(width_arr))
os.chdir(old_path)
