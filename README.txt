/***/ Nel seguente file sono contenute le istruzioni di esecuzinoe del file progetto "Progetto_mcf_pacchettodonde.py" \**\

Il programma è in grado di costruire grafici di pacchetti d'onda e relativi spettri di potenza
con dispersioni e numero di componenti diversi, e animazioni che ne descrivono il comportamento temporale.

Le dispersioni disponibili per il consulto sono:
1) ---- w = sqrt(c * k)
2) ---- w = sqrt(b + c * k^2)
3) ---- w = c * k
4) ---- w = c * k^2
dove "b" e "c" sono costanti arbitrarie.

Il numero delle componenti disponibili sono:
* --- 2
* --- 20
* --- 100
* --- 200
* --- 300
* --- 400
* --- 500
* --- 600
* --- 700
* --- 800
* --- 900
* --- 1000
* --- 2000
* --- 3000
* --- 4000
* --- 5000
* --- 10000
!! NOTA: con un numero di componenti più grande di 3000 le animazioni potrebbero non essere fluide e quindi soggette a scatti.

Le opzioni di selezione della costante "c" disponibili sono contenute in un vettore di numeri INTERI da 0 a 3.000.000 compresi.
!! Il valore di default di "c" è 30.000. Per valori troppo bassi o troppo alti saranno visibili solo parti del grafico, in quanto
fuori del limite superiore per l'asse x, oppure mostrerà un grafico troppo compatto e schiacciato lungo l'asse x. Si consiglia di
provare soltanto valori che vanno da 10.000 a 300.000

Per eseguire il programma è NECESSARIO specificare, in ordine: la dispersione che si vuole "--dispersione" seguito da una delle
seguenti opzioni(che corrispondono per numero di elenco a quelle sopra per "w"):
1) ---- sck
2) ---- sbck2
3) ---- ck
4) ---- ck2

; il numero di componenti con il quale costruire il pacchetto d'onda attraverso "--grafico" seguito da una delle opzioni esposte precedentemente
(2, 20, 100,...)

; è FACOLTATIVO poi scegliere i valori della costante "c" (--c seguito dalle opzioni sopra).
Nel caso questa non venga specificata verrà consederato il valore di default c = 30.000.


E' disponibile l'opzione "--show_spectrum" che, se vera, mostra lo spettro di potenza del pacchetto d'onda
generato, mostrandone anche l'evoluzioine temporale.

E' disponibile l'opzione "--show_all" che, se vera, mostra sia il pacchetto di onde generato con le volute specifiche, sia
il sorrispondente spettro di potenza.

Alcuni esempi di chiamate sono:

1) python3 Progetto_mcf_pacchettodonde.py --dispersione sck --grafico 2000
2) python3 Progetto_mcf_pacchettodonde.py --dispersione sck --grafico 2000 --c 22000  
3) python3 Progetto_mcf_pacchettodonde.py --dispersione sbck2 --grafico 1000 --c 15000 --show_spectrum
3) python3 Progetto_mcf_pacchettodonde.py --dispersione sbck2 --grafico 3000 --c 25000 --show_all

I primi due esempi mostrano il pacchetto d'onda con dispersione sck, generato sommando 2000 componenti
e con valori della costante "c" = 30.000 (default) nel primo caso e 22000 nel secondo.
Il terzo esempio costruisce un pacchetto d'onda con dispersione sbck2, generato sommando 1000 componenti e valore
di "c" = 15000, e ne mostra soltanto lo spettro di potenza.
Il quarto esmepio mostra sia il pacchetto d'onde generato sommando 3000 componenti sia il suo spettro di potenza.
