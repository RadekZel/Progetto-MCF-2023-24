import numpy
import matplotlib.pyplot as plt
from scipy import fft
from matplotlib.animation import FuncAnimation
from enum import Enum
import tkinter

#Classe dispersione: Contiene tutte le dispersioni consultabili
#La definizione di ogni dispersione avviene nella funzione "grafico"
class Dispersion(Enum):
    SCK = "sck"       # w = sqrt(c*k)
    CK = "ck"         # w = c*k
    SBCK2 = "sbck2"   # w = sqrt(b + c*k^2)
    CK2 = "ck2"       # w = c*k^2
    CDK = "cdk"       # w = c/k
    K4DC= "k4dc"      # w = k^4/c
    K2K = "k2k"       # w = k^2 - k

#Classe "Grafico": elenco del numero di componenti disponibili per la costruzione dei pacchetti d'onda
class Grafico(Enum):
    G2 = 2
    G20 = 20
    G100 = 100
    G200 = 200
    G300 = 300
    G400 = 400
    G500 = 500
    G600 = 600
    G700 = 700
    G800 = 800
    G900 = 900
    G1000 = 1000
    G2000 = 2000
    G3000 = 3000
    G4000 = 4000
    G5000 = 5000
    G10000 = 10000

#******Definizione delle funzioni********

'''
Funzione generatrice di un array di frequenze
Le frequenze vengono scelte tra quelle di un array (frequencies_array), generato tra "0" e "max_frequency", secondo -
- una probabilità data dalla "probability_distribution". Ad ogni elemento di "frequencies_array" corrisponde una probabilità -
- dell'array "probabilities". L'array finale, contenente le frequenze scelte, è "frequencies".
'''
def generate_frequencies(num_components, max_frequency):
    probability_distribution = lambda f: (6 / max_frequency**6) * f**5
    frequencies_array = numpy.linspace(1, max_frequency, 101)
    probabilities = probability_distribution(frequencies_array)
    probabilities /= probabilities.sum()
    frequencies = numpy.random.choice(frequencies_array, size = num_components, p = probabilities)
    return frequencies

'''
Funzione generatrice delle ampiezze. 
L'ampiezza viene scelta da una distribuzione uniforme tra "A_min" ed "A".
"A_min" è la ampiezza minima, che dipende dalla frequenza; "A" è una ampiezza massima, arbitraria; A_min < A
Viene passato come argomento una array di frequenze. Per ogni frequenza viene generato un A_min, che viene memorizzato -
- in un array di valori di A_min. Viene poi scelta una ampiezza da una distribuzione uniforme tra A_min ed A, per ogni A_min.
'''
def generate_amplitudes(frequencies_array, max_frequency, A):
    A_min_values = 0.9 * A * (frequencies_array / max_frequency)**2
    amplitudes_array = numpy.random.uniform(A_min_values, A)
    return amplitudes_array

#Funzione generatrice del pacchetto d'onda, sommando funzioni sinusoidali del tipo A*sin(k*x - w*t) (soluzione dell'equazione delle onde), ad un istante dato da "frame"
def generate_wave_packet(amplitudes_array, positions_array, frame, k_values, w_values):
    phase = k_values[:, numpy.newaxis] * positions_array - frame * w_values[:, numpy.newaxis]
    wave_packet = numpy.sum(amplitudes_array * numpy.sin(phase), axis = 0)
    return wave_packet

#Calcolo dello spettro di potenza del pacchetto d'onde attraverso fast Fourier transform
def calculate_power_spectrum(amplitudes_array, positions_array, frame, k_values, w_values):
    wave_packet = generate_wave_packet(amplitudes_array, positions_array, frame, k_values, w_values)
    power_spectrum = numpy.abs(fft.fft(wave_packet))**2
    return power_spectrum

A = 10
max_frequency = 100
b = 10

#Funzione di costruzione dei grafici
def grafico(num_components, dispersione, num_frames, c, show_spectrum, show_all):
    frequencies_array = generate_frequencies(num_components, max_frequency)
    amplitudes_array = generate_amplitudes(frequencies_array, max_frequency, A)
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
    
    '''
    Calcolo dei valori del numero d'onda per ogni frequenza componente il pacchetto, a seconda della dispersione.
        ---v(k) è la velocità di fase
        ---v(k) = w(k)/k, k = 2pi/lambda, lambda = v/f ----> k = 2*pi*f/v(k)
        ---dw/dk = velocità di gruppo, != v per sistemi dispersivi
    '''
    k_values = { 
        Dispersion.SCK: (4 * numpy.pi**2 * frequencies_array**2) / c,                     #v = sqrt(c/k) ---> k = 4*pi^2*f^2/c, dw/dk = .5*v
        Dispersion.CK: (2 * numpy.pi * frequencies_array) / c,                            #v = c ---> k = 2*pi*f/c, dw/dk = v
        Dispersion.CK2: numpy.sqrt((2 * numpy.pi * frequencies_array) / c),               #v = c*k ---> k = sqrt(2*pi*f/c), dw/dk = 2v
        Dispersion.SBCK2: numpy.sqrt((4 * numpy.pi**2 * frequencies_array**2 - b) / c),   #v = sqrt(b/k^2 + c) ---> k = sqrt(4*pi^2*f^2/c - b/c)
        Dispersion.CDK: c / (2 * numpy.pi * frequencies_array),                           #v = c/k^2 ---> k = c/(2*pi*f), dw/dk = -v
        Dispersion.K4DC: (2 * numpy.pi * frequencies_array * c)**(.25),                   #v = k^3/c ---> k = (2*pi*f*c)^(.25), dw/dk = 4v
        Dispersion.K2K: (1 + numpy.sqrt(1 + 8 * numpy.pi * frequencies_array)) / 2        #v = k - 1 ---> k = 1/2 + sqrt(1 + 8*pi*f)/2, dw/dk = 2v
    }[Dispersion(dispersione)]
    
    w_values = 2 * numpy.pi * frequencies_array #calcolo valori di omega: w = k*v = 2*pi*f
    
    line_wave = None
    line_spectrum = None

    # Creazione del grafico iniziale (per t = 0)
    if show_spectrum: #se vera mostra solo lo spettro di potenza del relativo pacchetto d'onda
        fig, ax = plt.subplots()
        power_spectrum = calculate_power_spectrum(amplitudes_array, positions_array, 0, k_values, w_values)
        power_spectrum /= power_spectrum.max()
        power_spectrum = numpy.abs(power_spectrum)
        frequencies = fft.fftfreq(len(positions_array), frequencies_array[1] - frequencies_array[0])
        
        line_spectrum, = ax.plot(frequencies[1:], power_spectrum[1:], color = "b")
        
        ax.set_xlabel("Frequenza")
        ax.set_ylabel("Potenza")
        ax.set_xscale("linear")
        ax.set_title(
            f"Evoluzione dello spettro di potenza - Dispersione: {dispersione}")
        
        ax.set_xlim(left = 0)
    
    elif show_all: #se vera mostra sia il pacchetto d'onda che il relativo spettro di potenza
        fig, ax = plt.subplots(2, 1, gridspec_kw = {'height_ratios': [1, 1]})
        
        power_spectrum = calculate_power_spectrum(amplitudes_array, positions_array, 0, k_values, w_values)
        power_spectrum /= power_spectrum.max()
        power_spectrum = numpy.abs(power_spectrum)
        frequencies = fft.fftfreq(len(positions_array), frequencies_array[1] - frequencies_array[0])
        frequencies = frequencies[1:]
        
        line_spectrum, = ax[1].plot(frequencies, power_spectrum[1:], color = "b")
        line_wave, = ax[0].plot(positions_array, generate_wave_packet(amplitudes_array, positions_array, 0, k_values, w_values), color = "b")

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
            power_spectrum = calculate_power_spectrum(amplitudes_array, positions_array, frame, k_values, w_values)
            power_spectrum /= power_spectrum.max()
            power_spectrum = numpy.abs(power_spectrum)

            line_spectrum.set_xdata(fft.fftfreq(len(positions_array), frequencies_array[1] - frequencies_array[0]))
            line_spectrum.set_ydata(power_spectrum)
            
            return line_spectrum,

        elif show_all:
            power_spectrum = calculate_power_spectrum(amplitudes_array, positions_array, frame, k_values, w_values)
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
    
    '''
    definizione della distanza tra frame per regolare la velocità di animazione a seconda della
    dispersione e del numero di componenti del pacchetto d'onda
    '''
    frame_interval = {
        (Dispersion.SCK, Grafico.G2): 0.00015,
        (Dispersion.SCK, Grafico.G20): 0.00015,
        (Dispersion.SCK, Grafico.G100): 0.00015,
        (Dispersion.SCK, Grafico.G200): 0.00015,
        (Dispersion.SCK, Grafico.G300): 0.00015,
        (Dispersion.SCK, Grafico.G400): 0.00015,
        (Dispersion.SCK, Grafico.G500): 0.00015,
        (Dispersion.SCK, Grafico.G600): 0.00035,
        (Dispersion.SCK, Grafico.G700): 0.00035,
        (Dispersion.SCK, Grafico.G800): 0.0005,
        (Dispersion.SCK, Grafico.G900): 0.0005,
        (Dispersion.SCK, Grafico.G1000): 0.0005,
        (Dispersion.SCK, Grafico.G2000): 0.0035,
        (Dispersion.SCK, Grafico.G3000): 0.0065,
        (Dispersion.SCK, Grafico.G4000): 0.007,
        (Dispersion.SCK, Grafico.G5000): 0.01,
        (Dispersion.SCK, Grafico.G10000): 0.1,
        
        (Dispersion.CK, Grafico.G2): 0.00015,
        (Dispersion.CK, Grafico.G20): 0.00015,
        (Dispersion.CK, Grafico.G100): 0.00015,
        (Dispersion.CK, Grafico.G200): 0.00015,
        (Dispersion.CK, Grafico.G300): 0.00015,
        (Dispersion.CK, Grafico.G400): 0.00015,
        (Dispersion.CK, Grafico.G500): 0.00015,
        (Dispersion.CK, Grafico.G600): 0.00035,
        (Dispersion.CK, Grafico.G700): 0.00035,
        (Dispersion.CK, Grafico.G800): 0.00035,
        (Dispersion.CK, Grafico.G900): 0.00035,
        (Dispersion.CK, Grafico.G1000): 0.00035,
        (Dispersion.CK, Grafico.G2000): 0.0015,
        (Dispersion.CK, Grafico.G3000): 0.004,
        (Dispersion.CK, Grafico.G4000): 0.004,
        (Dispersion.CK, Grafico.G5000): 0.01,
        (Dispersion.CK, Grafico.G10000): 0.1,

        (Dispersion.SBCK2, Grafico.G2): 0.00015,
        (Dispersion.SBCK2, Grafico.G20): 0.00015,
        (Dispersion.SBCK2, Grafico.G100): 0.00015,
        (Dispersion.SBCK2, Grafico.G200): 0.00015,
        (Dispersion.SBCK2, Grafico.G300): 0.00015,
        (Dispersion.SBCK2, Grafico.G400): 0.00015,
        (Dispersion.SBCK2, Grafico.G500): 0.00025,
        (Dispersion.SBCK2, Grafico.G600): 0.00035,
        (Dispersion.SBCK2, Grafico.G700): 0.00035,
        (Dispersion.SBCK2, Grafico.G800): 0.00035,
        (Dispersion.SBCK2, Grafico.G900): 0.0004,
        (Dispersion.SBCK2, Grafico.G1000): 0.0045,
        (Dispersion.SBCK2, Grafico.G2000): 0.002,
        (Dispersion.SBCK2, Grafico.G3000): 0.004,
        (Dispersion.SBCK2, Grafico.G4000): 0.004,
        (Dispersion.SBCK2, Grafico.G5000): 0.01,
        (Dispersion.SBCK2, Grafico.G10000): 0.1,

        (Dispersion.CK2, Grafico.G2): 0.00015,
        (Dispersion.CK2, Grafico.G20): 0.00015,
        (Dispersion.CK2, Grafico.G100): 0.00015,
        (Dispersion.CK2, Grafico.G200): 0.00015,
        (Dispersion.CK2, Grafico.G300): 0.00015,
        (Dispersion.CK2, Grafico.G400): 0.00015,
        (Dispersion.CK2, Grafico.G500): 0.00035,
        (Dispersion.CK2, Grafico.G600): 0.00035,
        (Dispersion.CK2, Grafico.G700): 0.00035,
        (Dispersion.CK2, Grafico.G800): 0.00034,
        (Dispersion.CK2, Grafico.G900): 0.00045,
        (Dispersion.CK2, Grafico.G1000): 0.00055,
        (Dispersion.CK2, Grafico.G2000): 0.0015,
        (Dispersion.CK2, Grafico.G3000): 0.005,
        (Dispersion.CK2, Grafico.G4000): 0.006,
        (Dispersion.CK2, Grafico.G5000): 0.015,
        (Dispersion.CK2, Grafico.G10000): 0.15,

        (Dispersion.CDK, Grafico.G2): 0.00015,
        (Dispersion.CDK, Grafico.G20): 0.00015,
        (Dispersion.CDK, Grafico.G100): 0.00015,
        (Dispersion.CDK, Grafico.G200): 0.00015,
        (Dispersion.CDK, Grafico.G300): 0.00015,
        (Dispersion.CDK, Grafico.G400): 0.00015,
        (Dispersion.CDK, Grafico.G500): 0.00035,
        (Dispersion.CDK, Grafico.G600): 0.00045,
        (Dispersion.CDK, Grafico.G700): 0.0005,
        (Dispersion.CDK, Grafico.G800): 0.00055,
        (Dispersion.CDK, Grafico.G900): 0.0007,
        (Dispersion.CDK, Grafico.G1000): 0.001,
        (Dispersion.CDK, Grafico.G2000): 0.006,
        (Dispersion.CDK, Grafico.G3000): 0.01,
        (Dispersion.CDK, Grafico.G4000): 0.03,
        (Dispersion.CDK, Grafico.G5000): 0.1,
        (Dispersion.CDK, Grafico.G10000): 10,

        (Dispersion.K4DC, Grafico.G2): 0.00015,
        (Dispersion.K4DC, Grafico.G20): 0.00015,
        (Dispersion.K4DC, Grafico.G100): 0.00015,
        (Dispersion.K4DC, Grafico.G200): 0.00015,
        (Dispersion.K4DC, Grafico.G300): 0.00015,
        (Dispersion.K4DC, Grafico.G400): 0.00015,
        (Dispersion.K4DC, Grafico.G500): 0.00035,
        (Dispersion.K4DC, Grafico.G600): 0.0004,
        (Dispersion.K4DC, Grafico.G700): 0.00045,
        (Dispersion.K4DC, Grafico.G800): 0.00055,
        (Dispersion.K4DC, Grafico.G900): 0.0006,
        (Dispersion.K4DC, Grafico.G1000): 0.001,
        (Dispersion.K4DC, Grafico.G2000): 0.002,
        (Dispersion.K4DC, Grafico.G3000): 0.004,
        (Dispersion.K4DC, Grafico.G4000): 0.005,
        (Dispersion.K4DC, Grafico.G5000): 0.01,
        (Dispersion.K4DC, Grafico.G10000): 0.1,

        (Dispersion.K2K, Grafico.G2): 0.00015,
        (Dispersion.K2K, Grafico.G20): 0.00015,
        (Dispersion.K2K, Grafico.G100): 0.00015,
        (Dispersion.K2K, Grafico.G200): 0.00015,
        (Dispersion.K2K, Grafico.G300): 0.00015,
        (Dispersion.K2K, Grafico.G400): 0.00015,
        (Dispersion.K2K, Grafico.G500): 0.00035,
        (Dispersion.K2K, Grafico.G600): 0.00035,
        (Dispersion.K2K, Grafico.G700): 0.0004,
        (Dispersion.K2K, Grafico.G800): 0.00045,
        (Dispersion.K2K, Grafico.G900): 0.00055,
        (Dispersion.K2K, Grafico.G1000): 0.0006,
        (Dispersion.K2K, Grafico.G2000): 0.002,
        (Dispersion.K2K, Grafico.G3000): 0.004,
        (Dispersion.K2K, Grafico.G4000): 0.006,
        (Dispersion.K2K, Grafico.G5000): 0.02,
        (Dispersion.K2K, Grafico.G10000): 0.1,
    }[Dispersion(dispersione), Grafico(num_components)]

    # Funzione di animazione
    animation = FuncAnimation(
        fig, update, frames = numpy.arange(0, num_frames, frame_interval), fargs = (amplitudes_array, positions_array, k_values, w_values, c, line_spectrum, line_wave, show_spectrum, show_all),
        interval = .01, blit = True)

    plt.show()

# Costruzione dell'interfaccia grafica
def run_gui():
    
    def start_animation(): #funzione di inizio animazione

        #inizializzazione delle variabili da passare alla funzione "grafico"
        num_components = int(entry_num_components.get())
        dispersione = entry_dispersione.get()
        num_frames = 100000
        c = float(entry_c.get())
        show_spectrum = var_spectrum.get() == 1
        show_all = var_show_all.get() == 1

        grafico(num_components, dispersione, num_frames, c, show_spectrum, show_all)

    #costruzione dell'interfaccia e definizione delle variabili in ingresso
    root = tkinter.Tk()
    root.title("Simulatore di pacchetti d'onda")
    root.geometry("400x300")

    label_num_components = tkinter.Label(root, text = "Numero di componenti:")
    label_num_components.pack()
    entry_num_components = tkinter.Entry(root)
    entry_num_components.pack()

    label_dispersione = tkinter.Label(root, text = "Tipo di dispersione:")
    label_dispersione.pack()
    entry_dispersione = tkinter.Entry(root)
    entry_dispersione.pack()

    label_c = tkinter.Label(root, text = "Valore della costante c:")
    label_c.pack()
    entry_c = tkinter.Entry(root)
    entry_c.pack()

    var_spectrum = tkinter.IntVar()
    checkbox_spectrum = tkinter.Checkbutton(root, text = "Mostra lo spettro di potenza", variable = var_spectrum)
    checkbox_spectrum.pack()

    var_show_all = tkinter.IntVar()
    checkbox_show_all = tkinter.Checkbutton(root, text = "Mostra pacchetto d'onda e spettro", variable = var_show_all)
    checkbox_show_all.pack()

    button_start = tkinter.Button(root, text = "Inizia simulazione", command = start_animation)
    button_start.pack()

    root.mainloop()

run_gui()                  

