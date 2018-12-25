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
MAX_VAL = 1022

#analyzer
for filename in filenames_txt:

	data = np.loadtxt(filename)

break
