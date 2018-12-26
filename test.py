#!/usr/bin/env python3
#test.py
import sys, glob, os
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as plt
import struct

import filamentyzer

#setup filenames
path = sys.argv[1]
mode = sys.argv[2]
os.chdir(path)

if (mode == "1"):
	#analyzer
	if (os.path.isdir('weak') == False):
		os.makedirs('weak')
	if (os.path.isdir('overscaled') == False):
		os.makedirs('overscaled')
	filenames_txt = glob.glob('*_*.txt')
	filenames_png = glob.glob('*_*.png')

	filter_over_weak(filenames_txt, filenames_png)

if (mode == "2"):
	#clean and print luminescence images
	if (os.path.isdir('out') == False):
		os.makedirs('out')
		if (os.path.isdir('images') == False):
			os.makedirs('images')
	filenames_dat = glob.glob('*_*.txt')

	lumin_clean(filenames_dat)
