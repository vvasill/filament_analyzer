import sys, glob, os
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as plt

#setup filenames
path = sys.argv[1]
os.chdir(path)

if (os.path.isdir('weak') == False):
	os.makedirs('weak')
if (os.path.isdir('overscaled') == False):
	os.makedirs('overscaled')
filenames_txt = glob.glob('*_*.txt')
filenames_png = glob.glob('*_*.png')

#params setting
MAX_VAL = 1023

#analyzer
for filename in filenames_txt:

	data = np.loadtxt(filename)
	print(filename + ' is processing')
	f_name = filename.split(".txt")[0]
	f_params = f_name.split('_')[:]

	x_max, y_max = np.unravel_index(np.argmax(data), data.shape)

	if (data[x_max, y_max] > MAX_VAL):
		os.rename(filename, 'overscaled/' + filename)
		for f_n in filenames_png:
			f_name_png = f_n.split(".png")[0]
			f_png_params = f_name_png.split('_')[:]
			if (f_name_png_params[1:3] == f_params[0:2]):
				os.rename(f_n, 'overscaled/' + f_n)
				break
	else:
		s = 0.0
		for i in range(x_max-1, x_max+2):
			for j in range(y_max-1, y_max+2):
				if i != x_max or j != y_max:
					s += data[i,j]
	
		if (data[x_max, y_max] > s/4.0):
			os.rename(filename, 'weak/' + filename)
			for f_n in filenames_png:
				f_name_png = f_n.split(".png")[0]
				f_png_params = f_name_png.split('_')[:]
				if (f_png_params[1:3] == f_params[0:2]):
					os.rename(f_n, "weak/" + f_n)
					break
