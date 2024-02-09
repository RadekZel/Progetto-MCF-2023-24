/***/ Nel seguente file sono contenute le istruzioni di esecuzione e visualizzazione dei contenuti del file progetto "ProjectPO.py" \**\

Il programma è in grado di costruire animazioni temporali di pacchetti d'onda e relativi spettri di potenza
con dispersioni e numero di componenti diversi, descrivendone il comportamento temporale.

All'esecuzione del programma verrà aperta una piccola finestra dove si potranno scegliere il numero di componenti per la costruzione del grafico,
la dispersione, il valore della costante "c", se mostrare lo spettro di potenza oppure sia spettro che pacchetto.

Le dispersioni disponibili per il consulto sono:
1) ---- w = sqrt(c * k)
2) ---- w = sqrt(b + c * k^2)
3) ---- w = c * k
4) ---- w = c * k^2
5) ---- w = c/k
6) ---- w = k^4/c
7) ---- w = k^2 - k

dove "b" e "c" sono costanti arbitrarie.

Il valore della costante "c" è preimpostata al valore di default 30.000. E' possibile modificarlo, anche se il valore di default è quello che fornisce una 
maggiore chiarezza a livello visivo dei grafici.
Per valori troppo bassi o troppo alti saranno visibili solo parti del grafico, in quanto fuori del limite superiore per l'asse x, oppure mostrerà un grafico troppo compatto e schiacciato lungo l'asse x. Valori di prova consigliati sono quelli che vanno da 10.000 a 300.000

-----------------------------------------ESECUZIONE----------------------------------------------------

Per eseguire il programma è sufficiente chamarlo da riga di comando, per esempio:

python3 ProjectPO.py

Verrà successivamente aperta una finestra di controllo dalla quale si potranno scegliere la dispersione desiderata, il numero di componenti per costruire il
pacchetto d'onda, attraverso menù a tendina, e si potrà scegliere se mostrarne lo spettro di potenza oppure sia spettro che pacchetto. Nel caso non si selezioni una opzione di visualizzazione verrà mostrato soltanto il pacchetto.

Le opzioni per le dispersioni tra cui scegliere sono quelle di elenco nelle definizioni date sopra per "w".

Il numero delle componenti disponibili per costruire i pacchetti sono:
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

!! NOTA: con un numero di componenti più grande di 2000 le animazioni potrebbero non essere molto fluide.

E' FACOLTATIVO poi cambiare valore alla costante c. Il valore preimpostato è 30.000, valore che rende una migliore chiarezza visiva dei grafici. 

