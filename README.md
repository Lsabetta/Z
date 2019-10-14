# Z
Il programma si avvia con:

`python3 Z_arduino.py`

E si apre una schermata che permette di selezionare l'esperienza (al momento solo oscillatore)

## Oscillatore
Premendo start dopo aver selezionato oscillatore viene creato un oggetto della classe 'Start_oscillatore' e aperto il pannello corrispondente.
Da qui per iniziare una presa dati è necessario inserire un path dove salvare i dati ed un tempo di acquisizione, per poi cliccare 'Begin' (senza path o tempo viene visualizzato un messaggio di errore).

'Clear' azzera tutti i campi della schermata (compreso il plot).

'Display Data' permette di visualizzare il file specificato nel campo per il path.

Con un path esistente inserito è possibile cliccare 'PlotFit' per aprire la schermata di visualizzazione e fit.

## PlotFit
'Fit' esegue un fit ai dati (tutti, a meno di diverse indicazioni) e visualizza la curva risultante e i valori dei parametri fittati. I valori iniziali dei parametri possono essere costretti nel pannello sulla destra.

Attenzione: se si decide di costringere i parametri è necessario farlo per tutti (o aggiungere tantissime eccezioni nel codice)
## Generare dati 
Con:

`python gen_data.py`

Viene generato un file "sin_data.txt" di dati secondo la funzione con cui poi vengono fittati nel programma (solo per testare che il fit funzioni)
