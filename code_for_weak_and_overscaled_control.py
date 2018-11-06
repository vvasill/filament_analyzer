if data[x_max, y_max] > MAX_VAL:
		os.rename(filename, "overscaled/"+filename)
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
