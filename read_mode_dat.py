# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 16:56:08 2018

@author: Дмитрий
"""
import sys, glob, os
import struct
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

from operator import itemgetter

mpl.rc('text', usetex=True)
mpl.rcParams.update({'font.size': 20})
#mpl.rc('text.latex',unicode=True)
#mpl.rc('text.latex', preamble=r'\usepackage[utf8]{inputenc}')
#mpl.rc('text.latex', preamble=r'\usepackage[russian]{babel}')
mpl.rcParams['text.latex.preamble'] = [r'\boldmath']
mpl.rcParams['text.latex.preamble']=[r"\usepackage{amsmath}"]

old_path = os.getcwd()
folder_modes = sys.argv[1]
os.chdir(folder_ac)

filenames_modes = glob.glob('*_*.dat')
filenames_modes_info = [f.split("_") for f in filenames_ac]
filenames_modes_info = sorted(filenames_ac_info, key=itemgetter(0))

for filename in filenames_modes:
	with open(filename, "rb") as binary_file:
		data_bin = binary_file.read()
		# Read the whole file at once
		
	zero = struct.unpack('>H', data_bin[0:2])[0]
	width = struct.unpack('>H', data_bin[2:4])[0]
	zero = struct.unpack('>H', data_bin[4:6])[0]
	heigth = struct.unpack('>H', data_bin[6:8])[0]

	s = '>H'+'H'*(heigth*width - 1)
	data = np.fromiter(struct.unpack(s, data_bin[8:]), dtype='uint16')
	data = np.reshape(data, (width, heigth))

	new_name = filename.split('.')[0]+".txt"
	np.savetxt(new_name, data)

'''
	#Graph plotting
	plt.figure(figsize=(10.5, 9.0), dpi=600)
	plt.rcParams['text.latex.preamble'] = [r'\boldmath']
	plt.xlabel(r'\textbf{Time, sec}')
	plt.ylabel(r'\textbf{Amplitude, arb.\,un.}')
	plt.plot(t_array, waveform[5:], 'k', color='k', lw='1.5')
	plt.grid()
	plt.minorticks_on()
	plt.tick_params(axis='x', pad=7)
	plt.tick_params(axis='y', pad=5)
	plt.savefig(filename_ac.split(".bin")[0] + ".png", bbox_inches='tight')
	plt.close() '''
