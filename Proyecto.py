# main.py
from	Conversores	import	mp3_a_fft, fft_a_mp3
from	Filtros		import	pasa_bajas, pasa_altas, pasa_banda, notch
#	nombre de la cancion a deeescomponer
Name	=	'Do_You_Want_To_Know_A_Secret'
################################################################################################
####			Desconposicion de la cancion para realizar transformada de fourier			####
################################################################################################
fft_result, sample_rate, frecuencias, len_a	=	mp3_a_fft(
	nombre_base		=	Name,
	nombre_salida	=	Name	+	'_original',	# Guarda la FFT original
	mostrar_grafico	=	True				# Muestra el gráfico del espectro
)
####################################################
####			Aplicacion de filtros			####
####################################################
# Aplicar filtro pasa bajas y guardar
fft_filtrado	=	pasa_bajas(
	fft			=	fft_result,
	freq		=	frecuencias,
	sample_rate	=	sample_rate,
	cutoff_freq	=	1200,
	file_name	=	Name	+	'_pasa_bajas_1k2Hz'
)
# Aplicar filtro pasa altas y guardar
fft_filtrado	=	pasa_altas(
	fft			=	fft_result,
	freq		=	frecuencias,
	sample_rate	=	sample_rate,
	cutoff_freq	=	1200,
	file_name	=	Name	+	'_pasa_altas_1k2Hz'
)
# Aplicar filtro pasa bandas y guardar
fft_filtrado	=	pasa_banda(
	fft			=	fft_result,
	freq		=	frecuencias,
	sample_rate	=	sample_rate,
	low_cutoff	=	600,
	high_cutoff	=	1400,
	file_name	=	Name	+	'_pasa_bandas_1k4Hz_600Hz'
)
# Aplicar filtro notch y guardar
fft_filtrado	=	notch(
	fft			=	fft_result,
	freq		=	frecuencias,
	sample_rate	=	sample_rate,
	low_cutoff	=	600,
	high_cutoff	=	1400,
	file_name	=	Name	+	'_elimina_bandas_1k4Hz_600Hz'
)
################################################################
####			Reconstruccion de archivos a mp3			####
################################################################
# reconstruccion de archivo original
fft_a_mp3(
	nombre_base		=	Name	+	'_original',
	sample_base		=	sample_rate,
	nombre_salida	=	Name	+	'_reconstruido',
	len_base=len_a
)
# reconstruccion de archivos filtrados
fft_a_mp3(
	nombre_base		=	Name	+	'_pasa_bajas_1k2Hz',
	nombre_salida	=	Name	+	'_pasa_bajas_1k2Hz'
)

fft_a_mp3(
	nombre_base		=	Name	+	'_pasa_altas_1k2Hz',
	nombre_salida	=	Name	+	'_pasa_altas_1k2Hz'
)

fft_a_mp3(
	nombre_base		=	Name	+	'_pasa_bandas_1k4Hz_600Hz',
	nombre_salida	=	Name	+	'_pasa_bandas_1k4Hz_600Hz'
)

fft_a_mp3(
	nombre_base		=	Name	+	'_elimina_bandas_1k4Hz_600Hz',
	nombre_salida	=	Name	+	'_elimina_bandas_1k4Hz_600Hz'
)
