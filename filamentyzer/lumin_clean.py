#!/usr/bin/env python3
#lumin_clean.py
"""
luminiscence images cleaning procedure
"""

import sys, glob, os
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as plt
import struct
import scipy.ndimage as ndimg

def lumin_clean(filenames_dat):
	"""
	Function averages luminescence image and subtracts a background
	"""
	#read data
	data = open_dat(filename)

	#rotate		
	rot_data = rotate(data, angle)
	
	#clean

def rotate(data, angle):
	rot_data = ndimg.interpolation.rotate(input=data, angle=angle)
	return rot_data

def trunc(data, left, right):
	"""
	Function truncates an array. 
	"""
	trunc_data = data[:,left:right]
	
	return trunc_data

def open_dat(filename):
	"""
	Function opens binary file. 
	"""

	#binary data file reading
	with open(filename, "rb") as binary_file:
		data_bin = binary_file.read()
			
	zero = struct.unpack('>H', data_bin[0:2])[0]
	width = struct.unpack('>H', data_bin[2:4])[0]
	zero = struct.unpack('>H', data_bin[4:6])[0]
	height = struct.unpack('>H', data_bin[6:8])[0]
	
	s = '>H'+'H'*(height*width - 1)
	data = np.fromiter(struct.unpack(s, data_bin[8:]), dtype='uint16')
	data = np.reshape(data, (width, height))

	new_name = filename.split('.')[0]+".txt"
	np.savetxt(new_name, data)

	print(str(filename) + ' ' + str(width) + ' ' + str(height))	
	return data

def plot_heat_map(data, filename, vmin, vmax):
	"""
	Function plots heat maps of data numpy 2d array and save result to filename.png.
	"""
	#heat map plotting
	plt.figure(figsize=(20,10)) #fig_size
	mpl.rcParams.update({'font.size': 22}) #fontsize
	plt.xlabel(r'$x$')
	plt.ylabel(r'$y$')
	plt.grid(True)
	plt.minorticks_on()
	plt.tick_params(axis='x', pad=7)
	plt.tick_params(axis='y', pad=5)

	plt.imshow(data, cmap='magma', vmin=vmin, vmax=vmax)
	plt.colorbar()
	plt.savefig(filename + ".png", bbox_inches='tight')

	plt.close()
	
	return True
	
