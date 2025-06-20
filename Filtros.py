import numpy as np
from pathlib import Path

# Configuración de carpetas (ya definida en tu código)
CurrentDir = Path(__file__).parent.absolute()
NPY_DIR = CurrentDir / 'npy'

def pasa_bajas(fft, freq, sample_rate, cutoff_freq, file_name):
	fft_filtrado	=	fft.copy()
	fft_filtrado[freq	>	cutoff_freq] = 0
	# Guardar en NPY_DIR
	archivo_salida	=	NPY_DIR	/	(file_name	+	'.npy')
	np.save(str(archivo_salida), {'fft': fft_filtrado, 'sample_rate': sample_rate})
	print("Filtro pasa bajas guardado en: "	+	str(archivo_salida))
	return	fft_filtrado

def pasa_altas(fft, freq, sample_rate, cutoff_freq, file_name):
    fft_filtrado	=	fft.copy()
    fft_filtrado[freq	<	cutoff_freq] = 0
    # Guardar en NPY_DIR
    archivo_salida	=	NPY_DIR	/	(file_name	+	'.npy')
    np.save(str(archivo_salida), {'fft': fft_filtrado, 'sample_rate': sample_rate})
    print("Filtro pasa altas guardado en: "	+	str(archivo_salida))
    return	fft_filtrado

def pasa_banda(fft, freq, sample_rate, low_cutoff, high_cutoff, file_name):
    fft_filtrado	=	fft.copy()
    fft_filtrado[(freq	<	low_cutoff)	|	(freq	>	high_cutoff)]	=	0
    # Guardar en NPY_DIR
    archivo_salida	=	NPY_DIR	/	(file_name	+	'.npy')
    np.save(str(archivo_salida), {'fft': fft_filtrado, 'sample_rate': sample_rate})
    print("Filtro pasa bandas guardado en: "	+	str(archivo_salida))
    return	fft_filtrado

def notch(fft, freq, sample_rate, low_cutoff, high_cutoff, file_name):
    fft_filtrado	=	fft.copy()
    fft_filtrado[(freq	>=	low_cutoff)	&	(freq	<=	high_cutoff)]	=	0
    # Guardar en NPY_DIR
    archivo_salida	=	NPY_DIR	/	(file_name	+	'.npy')
    np.save(str(archivo_salida), {'fft': fft_filtrado, 'sample_rate': sample_rate})
    print("Filtro notch guardado en: "	+	str(archivo_salida))
    return	fft_filtrado
