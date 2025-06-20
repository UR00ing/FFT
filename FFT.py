import numpy as np
import cmath

def	next_power_of_2(length):
	return	1	if	length	==	0	else	2	**	(length	-	1).bit_length()

########################################################################
####				Transformadas de Fourier incluyendo inversa		####
########################################################################
def FFT(a):
	"""
	Transformada Rapida de Fourier
	"""
	n		=	len(a)
	if n	<=	1:
		return	a
	pares	=	FFT(a[0::2]) #Recursiva con los indices pares
	impares	=	FFT(a[1::2]) #Recursiva con los indices impares

	y	=	np.zeros(n,dtype=complex)
	#Calculo de FFT
	for	k	in	range(n//2):
		w			=	cmath.exp(-2j	*	cmath.pi	*	k	/	n)
		y[k]		=	pares[k]	+	w	*	impares[k]
		y[k+n//2]	=	pares[k]	-	w	*	impares[k]
	
	return	y

def iFFT(a):
	"""
	Transformada Rapida de Fourier inversa
	"""
	n	=	len(a)
	if	n	<=	1:
		return	a
	pares	=	iFFT(a[0::2]) #Recursiva con los indices pares
	impares	=	iFFT(a[1::2]) #Recursiva con los indices impares

	y	=	np.zeros(n,dtype=complex)
	#Calculo de FFT
	for	k	in	range(n//2):
		w			=	cmath.exp(2j	*	cmath.pi	*	k	/	n)
		y[k]		=	(pares[k]	+	w	*	impares[k])
		y[k+n//2]	=	(pares[k]	-	w	*	impares[k])
	
	return	y
####################################################################################################
####			conversion de funciones equivalentes a las de numpy (rfft,irfft,etc.)			####
####################################################################################################
def mi_rfft(a):
	"""
	rFFT con conversion similar a numpy
	"""
	n	=	len(a)
	rfft	=	np.array(FFT(a))
	return	rfft[:n//2	+	1]

def mi_irfft(a):
	"""
	riFFT con conversion similar a numpy
	"""
	n	=	len(a)
	rfft	=	np.array(iFFT(a))
	return	rfft[:n//2	+	1]

def mi_rfftfreq(n, d=1.0):
	"""
	Implementación de rfftfreq (similar a np.fft.rfftfreq)
	"""
	val		=	1.0	/	(n	*	d)
	N		=	n	//	2	+	1
	results	=	np.arange(0, N, dtype=int)
	return results	*	val
################################################################################################
####			conversion de funciones equivalentes a las de numpy (fft,ifft,etc.)			####
################################################################################################
def	mi_fft(a):
	"""
	FFT con conversion similar a numpy
	"""
	n				=	next_power_of_2(len(a))
	n_original		=	len(a)
	new_a			=	np.zeros(n,dtype=complex)
	new_a[:n_original]	=	a
	return	FFT(new_a)[:n_original]

def	mi_ifft(a):
	"""
	iFFT con conversion similar a numpy
	"""
	n				=	next_power_of_2(len(a))
	n_original		=	len(a)
	new_a			=	np.zeros(n,dtype=complex)
	new_a[:n_original]	=	a
	return	iFFT(new_a)[:n_original]	/	n

def mi_fftfreq(n, d=1.0):
	"""
	Implementación de fftfreq (similar a np.fft.fftfreq)
	"""
	new_n	=	n
	val		=	1.0 / (new_n * d)
	results	=	np.empty(new_n)
	N		=	(new_n-1)//2 + 1  # Número de frecuencias positivas
	# Frecuencias positivas
	results[:N]	=	np.arange(0, N, dtype=float)	*	val
	# Frecuencias negativas
	results[N:]	=	np.arange(-(new_n//2), 0, dtype=float)	*	val

	return results
