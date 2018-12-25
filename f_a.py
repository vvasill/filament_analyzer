print(filename + ' is processing')
	f_name = filename.split(".txt")[0]
	f_params = f_name.split('_')[:]

	x_max, y_max = np.unravel_index(np.argmax(data), data.shape)

	if (data[x_max, y_max] > MAX_VAL):
		os.rename(filename, 'overscaled/' + filename)
		for f_n in filenames_png:
			f_name_png = f_n.split(".png")[0]
			f_png_params = f_name_png.split('_')[:]
			if (f_png_params[1:3] == f_params[0:2]):
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
				
