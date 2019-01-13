#!/usr/bin/env python3
#test.py
import sys, glob, os
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as plt
import struct

from lumin_clean import *

os.chdir("./test/new")
filenames_dat = glob.glob('*_*.dat')

for filename in filenames_dat:
	data = open_dat(filename)
	left = data.shape[0]//2
	right = data.shape[1]
	data_rot = rotate(data, 30)
	data_trunc = trunc(data_rot, left, right)

	print_name = filename.split('.')[0]
	vmin = 200
	vmax = 500
	plot_heat_map(data_trunc, "./images/" + print_name, vmin, vmax)
