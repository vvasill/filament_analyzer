import sys, glob, os
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as plt

#setup filenames
path = sys.argv[1]
os.chdir( path )
os.makedirs("weak", exist_ok = True)
os.makedirs("overscaled", exist_ok = True)
filenames_txt = glob.glob('*_*.txt')
filenames_png = glob.glob('*_*.png')

#params setting
MAX_VAL = 1023

#analyzer
for filename in filenames_txt:

	data = np.loadtxt(filename)
	print(filename + 'is processing')
	f_name = filename.split(".txt")[0]
	f_params = f_name_splitted.split('_')[:]

	x_max, y_max = np.unravel_index(np.argmax(data), data.shape)

	if data[x_max, y_max] > MAX_VAL:
		os.rename(filename, 'overscaled/' + filename)
		for f_n in filenames_png:
			f_name_png_splitted = filename_1.split(".png")[0]
			f_name_png_params = f_name_png_splitted.split('_')[:]
			if f_name_png_params[1:3] == f_params[0:2]:
				os.rename(filename_1, 'overscaled/' + f_n)
				break
		continue
	else:
		s = 0.0
		for i in range(x_max-1, x_max+2):
			for j in range(y_max-1, y_max+2):
				if i != x_max or j != y_max:
					s += data[i,j]
	
		if data[x_max, y_max] > s/4.0:
			os.rename(filename, 'weak/' + filename)
			for filename_1 in filenames_png:
				filename_png_splitted = filename_1.split(".png")[0]
				f_png_params = filename_png_splitted.split('_')[:]
				if f_png_params[1:3] == f_params[0:2]:
					os.rename(filename_1, "weak/"+filename_1)
					break
			continue
