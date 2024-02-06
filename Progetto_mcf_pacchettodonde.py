import numpy
import matplotlib.pyplot as plt
from scipy import fft
from matplotlib.animation import FuncAnimation
import argparse
from enum import Enum
import tkinter as tk

#Classe dispersione: Contiene tutte le dispersioni consultabili
#La definizione di ogni dispersione avviene nella funzione "grafico"
class Dispersion(Enum):
    SCK = "sck"
    CK = "ck"
    SBCK2 = "sbck2"
    CK2 = "ck2"
    CDK = "cdk"
    K4DC= "k4dc"
    K2K = "k2k"

#Classe "Grafico": elenco del numero di componenti possibili per la costruzione dei pacchetti d'onda
#Viene utilizzato nella definizione del main per la scelta tra le opzioni dell'argomento "--grafico"
class Grafico(Enum):
    G2 = "2"
    G20 = "20"
    G100 = "100"
    G200 = "200"
    G300 = "300"
    G400 = "400"
    G500 = "500"
    G600 = "600"
    G700 = "700"
    G800 = "800"
    G900 = "900"
    G1000 = "1000"
    G2000 = "2000"
    G3000 = "3000"
    G4000 = "4000"
    G5000 = "5000"
    G10000 = "10000"

#******Definizione delle funzioni********

#Funzione generatrice di un array di frequenze
#Le frequenze vengono scelte tra quelle di un array (frequencies_array), generato tra "0" e "max_frequency", secondo -
#- una probabilità data dalla "probability_distribution". Ad ogni elemento di "frequencies_array" corrisponde una probabilità -
#- dell'array "probabilities". L'array finale, contenente le frequenze scelte, è "frequencies".
def generate_frequencies(num_components, max_frequency):
    probability_distribution = lambda f: (6 / max_frequency**6) * f**5
    frequencies_array = numpy.linspace(1, max_frequency, 101)
    probabilities = probability_distribution(frequencies_array)
    probabilities /= probabilities.sum()
    frequencies = numpy.random.choice(frequencies_array, size = num_components, p = probabilities)
    return frequencies

#Funzione generatrice delle ampiezze. 
#L'ampiezza viene scelta da una distribuzione uniforme tra "A_min" ed "A".
#"A_min" è la ampiezza minima, che dipende dalla frequenza; "A" è una ampiezza massima, arbitraria; A_min < A
#Viene passato come argomento una array di frequenze. Per ogni frequenza viene generato un A_min, che viene memorizzato -
#- in un array di valori di A_min. Viene poi scelta una ampiezza da una distribuzione uniforme tra A_min ed A, per ogni A_min.
def generate_amplitudes(frequencies_array, max_frequency, A):
    A_min_values = 0.9 * A * (frequencies_array / max_frequency)**2
    amplitudes_array = numpy.random.uniform(A_min_values, A)
    return amplitudes_array


A = 10
max_frequency = 100
b = 10


#Funzione geenratrice del pacchetto d'onda, sommando funzioni sinusoidali del tipo Asin(kx - wt) (soluzione dell'equazione delle onde)
def generate_wave_packet(amplitudes_array, positions_array, frame, k_values, w_values):
    phase = k_values[:, numpy.newaxis] * positions_array - frame * w_values[:, numpy.newaxis]
    wave_packet = numpy.sum(amplitudes_array * numpy.sin(phase), axis = 0)
    return wave_packet

#Calcolo dello spettro di potenza del pacchetto d'onde attraverso fast Fourier transform
def calculate_power_spectrum(amplitudes_array, positions_array, frame, k_values, w_values, c):
    wave_packet = generate_wave_packet(amplitudes_array, positions_array, frame, k_values, w_values)
    power_spectrum = numpy.abs(fft.fft(wave_packet))**2
    return power_spectrum

#Funzione di costruzione dei grafici

def grafico(num_components, dispersione, num_frames, c, show_spectrum, show_all):
    frequencies_array = generate_frequencies(num_components, max_frequency) #generazione array di frequenze secondo la probabilità
    amplitudes_array = generate_amplitudes(frequencies_array, max_frequency, A) #generazione rispettive ampiezze
    positions_array = { #generazione del vettore delle posizioni: a seconda della dispersione il limite superiore cambia -
                        # - per rendere più chiara l'immagine del pacchetto
        Dispersion.SCK: numpy.linspace(0, 25, len(frequencies_array)),
        Dispersion.CK: numpy.linspace(0, 17000, len(frequencies_array)),
        Dispersion.SBCK2: numpy.linspace(0, 150, len(frequencies_array)),
        Dispersion.CK2: numpy.linspace(0, 5000, len(frequencies_array)),
        Dispersion.CDK: numpy.linspace(0, 10, len(frequencies_array)),
        Dispersion.K4DC: numpy.linspace(0, 20, len(frequencies_array)),
        Dispersion.K2K: numpy.linspace(0, 30, len(frequencies_array))
    }[Dispersion(dispersione)]

    k_values = { #calcolo dei valori del numero d'onda per ogni frequenza
                 # v(k) = w(k)/k, k = 2pi/lambda, lambda = v/f ----> k = 2*pi*f/v(k)
                 # v è la velocità di fase
                 #dw/dk = velocità di gruppo, != v per sistemi dispersivi
        Dispersion.SCK: (4 * numpy.pi**2 * frequencies_array**2) / c,                     #v = sqrt(c/k) ---> k = 4*pi^2*f^2/c, dw/dk = .5*v
        Dispersion.CK: (2 * numpy.pi * frequencies_array) / c,                            #v = c ---> k = 2*pi*f/c, dw/dk = v
        Dispersion.CK2: numpy.sqrt((2 * numpy.pi * frequencies_array) / c),               #v = c*k ---> k = sqrt(2*pi*f/c), dw/dk = 2v
        Dispersion.SBCK2: numpy.sqrt((4 * numpy.pi**2 * frequencies_array**2 - b) / c),   #v = sqrt(b/k^2 + c) ---> k = sqrt(4*pi^2*f^2/c - b/c)
        Dispersion.CDK: c / (2 * numpy.pi * frequencies_array),                           #v = c/k^2 ---> k = c/(2*pi*f), dw/dk = -v
        Dispersion.K4DC: (2 * numpy.pi * frequencies_array * c)**(.25),                   #v = k^3/c ---> k = (2*pi*f*c)^(.25), dw/dk = 4v
        Dispersion.K2K: (1 + numpy.sqrt(1 + 8 * numpy.pi * frequencies_array)) / 2
    }[Dispersion(dispersione)]
    
    w_values = 2 * numpy.pi * frequencies_array #calcolo valori di omega: w = k*v = 2*pi*f
    
    line_wave = None
    line_spectrum = None

    # Creazione del grafico iniziale (per t = 0)
    if show_spectrum: #se vera mostra solo lo spettro di potenza del relativo pacchetto d'onda
        fig, ax = plt.subplots()
        power_spectrum = calculate_power_spectrum(amplitudes_array, positions_array, 0, k_values, w_values, c)
        power_spectrum /= power_spectrum.max()
        power_spectrum = numpy.abs(power_spectrum)
        frequencies = fft.fftfreq(len(positions_array), frequencies_array[1] - frequencies_array[0])
        
        line_spectrum, = ax.plot(frequencies[1:], power_spectrum[1:], color="b")
        
        ax.set_xlabel("Frequenza")
        ax.set_ylabel("Potenza")
        ax.set_xscale("linear")
        ax.set_title(
            f"Evoluzione dello spettro di potenza - Dispersione: {dispersione}")
        
        ax.set_xlim(left = 0)
    
    elif show_all: #se vera mostra sia il pacchetto d'onda che il relativo spettro di potenza
        fig, ax = plt.subplots(2, 1, gridspec_kw={'height_ratios': [1, 1]})
        
        power_spectrum = calculate_power_spectrum(amplitudes_array, positions_array, 0, k_values, w_values, c)
        power_spectrum /= power_spectrum.max()
        power_spectrum = numpy.abs(power_spectrum)
        frequencies = fft.fftfreq(len(positions_array), frequencies_array[1] - frequencies_array[0])
        frequencies = frequencies[1:]
        
        line_spectrum, = ax[1].plot(frequencies, power_spectrum[1:], color = "b")
        line_wave, = ax[0].plot(positions_array, generate_wave_packet(amplitudes_array, positions_array, 0, k_values, w_values),
                                    color = "b")

        ax[1].set_xlabel("Frequenze")
        ax[1].set_ylabel("Potenza")
        ax[0].set_xlabel("Posizione")
        ax[0].set_ylabel("Ampiezza")
        ax[0].set_title(
            f"Evoluzione temporale del pacchetto d'onda - Dispersione: {dispersione}")
        ax[1].set_title("Evoluzione temporale dello spettro di potenza")

        ax[1].set_xlim(left = 0)

    else: #se show_spectrum == "False" and show_all == "False" allora mostra solo il pacchetto d'onda
        fig, ax = plt.subplots()
        
        line_wave, = ax.plot(positions_array, generate_wave_packet(amplitudes_array, positions_array, 0, k_values, w_values), color = "b")
        
        ax.set_xlabel("Posizione")
        ax.set_ylabel("Ampiezza")
        ax.set_title(f"Evoluzione del pacchetto d'onda - Dispersione: {dispersione}")
    
    #Funzione di aggiornamento del grafico iniziale (per t > 0)
    def update(frame, amplitudes_array, positions_array, k_values, w_values, c, line_spectrum, line_wave, show_spectrum, show_all):
        if show_spectrum:
            power_spectrum = calculate_power_spectrum(amplitudes_array, positions_array, frame, k_values, w_values, c)
            power_spectrum /= power_spectrum.max()
            power_spectrum = numpy.abs(power_spectrum)

            line_spectrum.set_xdata(fft.fftfreq(len(positions_array), frequencies_array[1] - frequencies_array[0]))
            line_spectrum.set_ydata(power_spectrum)
            
            return line_spectrum,

        elif show_all:
            power_spectrum = calculate_power_spectrum(amplitudes_array, positions_array, frame, k_values, w_values, c)
            power_spectrum /= power_spectrum.max()
            power_spectrum = numpy.abs(power_spectrum)

            wave_packet = generate_wave_packet(amplitudes_array, positions_array, frame, k_values, w_values)

            line_spectrum.set_xdata(fft.fftfreq(len(positions_array), frequencies_array[1] - frequencies_array[0]))
            line_spectrum.set_ydata(power_spectrum)
            line_wave.set_xdata(positions_array)
            line_wave.set_ydata(wave_packet)

            return line_spectrum, line_wave,

        else:
            wave_packet = generate_wave_packet(amplitudes_array, positions_array, frame, k_values, w_values)

            line_wave.set_xdata(positions_array)
            line_wave.set_ydata(wave_packet)
            
            return line_wave,
    
    #settaggio della distanza tra frames in relazione alla dispersione, per regolare la velocità di animazione
    frame_interval = {
        Dispersion.SCK: .0015,
        Dispersion.CK: .0015,
        Dispersion.SBCK2: .0015,
        Dispersion.CK2: .0015,
        Dispersion.CDK: .0045,
        Dispersion.K4DC: .0035,
        Dispersion.K2K: .0030,
    }[Dispersion(dispersione)]

    # Funzione di animazione
    animation = FuncAnimation(
        fig, update, frames = numpy.arange(0, num_frames, frame_interval), fargs = (amplitudes_array, positions_array, k_values, w_values, c, line_spectrum, line_wave, show_spectrum, show_all),
        interval = .01, blit = True)

    plt.show()
        

def main():
    parser = argparse.ArgumentParser(
        description = "Studio di pacchetti d'onda generati da onde sinusoidali in numero crescente",
        formatter_class = argparse.RawTextHelpFormatter
    )

    parser.add_argument("--dispersione", choices = [disp.value for disp in Dispersion], required = True,
                        help = "sck --- seleziona pacchetti con dispersione sqrt(c*k) \n"
                             "ck --- selziona pacchetti con dispersione c*k \n"
                             "sbck2 --- seleziona pacchetti con dispersione sqrt(b + c*k^2) \n"
                             "ck2 --- seleziona pacchetti con dispersione c*k^2")
    parser.add_argument("--grafico", choices = [graf.value for graf in Grafico], required = True,
                        help = "Il numero rappresenta il numero di componenti che generano il pacchetto d'onda. \n"
                             "Scegliere tra: 2, 20, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 2000, 3000, 4000, 5000, 10000"
                            )
    
    parser.add_argument("--num_frames", type = int,
                        default = 100000, help = "Numero di frame per l'animazione")
    
    c_choices = numpy.arange(0, 3000001)
    c_choices = c_choices.tolist()
    
    parser.add_argument("--c", type = float, choices = c_choices,
                        default = 30000, help = "Seleziona la velocità di dispersione \n"
                        "opzioni: un valore INTERO in [0, 3000000] \n"
                        "default: 30000")
    
    parser.add_argument("--show_spectrum", action = "store_true",
                        help = "Visualizza lo spettro di potenza del corrispondente pacchetto d'onda")
    
    parser.add_argument("--show_all", action = "store_true",
                        help = "Visualizza il pacchetto d'onda e relativo spettro di potenza")

    args = parser.parse_args()
    c = args.c
    grafico(int(args.grafico), args.dispersione, args.num_frames, c, args.show_spectrum, args.show_all)
    
   
if __name__ == "__main__":
    main()                   

