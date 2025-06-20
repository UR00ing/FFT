import	numpy				as		np
from	pydub				import	AudioSegment
from	scipy.io			import	wavfile
import	matplotlib.pyplot	as		plt
from	pydub.playback		import	play
from	pathlib				import	Path
from	FFT					import	mi_fft, mi_ifft, mi_fftfreq, mi_rfft, mi_irfft, mi_rfftfreq
import	io

# Configuración de carpetas
CurrentDir = Path(__file__).parent.absolute()
AUDIO_DIR = CurrentDir / 'audio'
NPY_DIR = CurrentDir / 'npy'

# Crear carpetas si no existen
AUDIO_DIR.mkdir(exist_ok=True)
NPY_DIR.mkdir(exist_ok=True)

def mp3_a_fft(nombre_base, nombre_salida=None, mostrar_grafico=False):
	"""
	Procesa un MP3 a FFT 
	"""
	# Construir rutas completas
	archivo_entrada	=	AUDIO_DIR	/	(nombre_base	+	'.mp3')
	archivo_salida	=	NPY_DIR		/	((nombre_salida if nombre_salida else nombre_base)	+	'.npy')

	# Leer el archivo MP3
	audio		=	AudioSegment.from_mp3(str(archivo_entrada))
	sample_rate	=	audio.frame_rate

	# Convertir a un arreglo de numpy
	samples	=	np.array(audio.get_array_of_samples())
	#  Convertir a mono si es estéreo
	if	audio.channels	>	1:
		samples	=	samples.reshape((-1, 2)).mean(axis=1)

	############################################
	####			Calcular la FFT			####
	############################################
	# Mi transformada
	fft_result	=	mi_fft(samples)
	frecuencias	=	mi_fftfreq(len(samples), d=1/sample_rate)
	# Transformada de numpy
	#fft_result	=	np.real(np.fft.fft(samples))
	#frecuencias	=	np.fft.fftfreq(len(samples), d=1/sample_rate)

	# Guardar los datos FFT
	np.save(str(archivo_salida), {'fft': fft_result, 'sample_rate': sample_rate})
	print('Datos FFT guardados en '	+	str(archivo_salida))

	# Mostrar gráfico si se solicitó
	if mostrar_grafico:
		plt.figure(figsize=(10, 4))
		plt.plot(frecuencias, np.abs(fft_result))
		plt.title('Espectro de Frecuencias')
		plt.xlabel('Frecuencia (Hz)')
		plt.ylabel('Amplitud')
		plt.xlim(0, sample_rate/2)
		plt.show()

	return fft_result, sample_rate, frecuencias, len(samples)

def fft_a_mp3(nombre_base, fft_base=None, sample_base=None, nombre_salida=None, bitrate='192k', len_base=None):
	"""
	Reconstruye MP3 desde FFT
	"""
	# Construir rutas completas
	archivo_fft		=	NPY_DIR		/	(nombre_base	+	'.npy')
	nombre_output	=	(nombre_base	+	'_reconstruido')	if	nombre_salida	is None	else	nombre_salida
	archivo_salida	=	AUDIO_DIR	/	(nombre_output	+	'.mp3')

	# Cargar los datos FFT
	if (fft_base is None) or (sample_base is None):
		datos		=	np.load(str(archivo_fft), allow_pickle=True).item()
		fft_result	=	datos['fft']
		sample_rate	=	datos['sample_rate']
	else:
		fft_result	=	fft_base
		sample_rate	=	sample_base

	################################################################
	####			Calcular la transformada inversa			####
	################################################################
	# Mi transformada
	audio_reconstruido	=	np.real(mi_ifft(fft_result))[:len_base]
	#	Transformada de numpy
	#audio_reconstruido	=	np.real(np.fft.ifft(fft_result))

	####nueva linea
	#if len_base !=	None:
	#	original_len		=	len_base
	#	audio_reconstruido	=	audio_reconstruido[:original_len]

	# Normalizar el audio
	#audio_reconstruido	=	np.int16(audio_reconstruido / np.max(np.abs(audio_reconstruido)) * 32767)
	audio_reconstruido	=	np.int16(audio_reconstruido * (32767 / np.max(np.abs(audio_reconstruido))))
	#audio_reconstruido = audio_reconstruido / np.max(np.abs(audio_reconstruido))  # Normalizar a [-1, 1]
	#audio_reconstruido = np.int16(audio_reconstruido * 32767)  # Escalar a int16

	# Convertir a bytes en formato WAV
	audio_bytes	=	io.BytesIO()
	wavfile.write(audio_bytes, sample_rate, audio_reconstruido)
	audio_bytes.seek(0)

	# Crear objeto AudioSegment y exportar a MP3
	audio	=	AudioSegment.from_wav(audio_bytes)
	audio.export(str(archivo_salida), format='mp3', bitrate=bitrate)

	print("Audio MP3 reconstruido guardado en "	+	str(archivo_salida))