English version (IT below)
# Z
The program is started with:

`python3 Z_arduino.py`

A window pop up, and allows to select the lab experience (only armonic oscillator for the moment)

## Armonic oscillator 
After selecting the pbscillator, by pressing start a 'Start_oscillatore' object is created and the correspondent panel opened.
To start a data taking session iti is necessary to insert a path where to save the data and an aquisition time. Then click 'Begin' (without any path an error message is displayed).

'Clear' zeros all the fields.

'Display Data' permits to visualize the file specified in the path field.

With an existing path it is possible to select 'PlotFit' to open the fit and visualization window (an object of the class 'FitPanel' is created).

## PlotFit
'Fit' executes a fit to the data (all of them, unless further specified) and visualize the resulting curve and the fitted parameters. The initial values can be constrained in the right panel.

Attention: if you decide to constraint the parameters, you havo to do it for all of them.

## Data Generation
With:

`python gen_data.py`

A "sin_data.txt" data file is generated vased on the function used to fit (as a test the fit is working).

Italian version

# Z
Il programma si avvia con:

`python3 Z_arduino.py`

E si apre una schermata che permette di selezionare l'esperienza (al momento solo oscillatore)

## Oscillatore
Premendo start dopo aver selezionato oscillatore viene creato un oggetto della classe 'Start_oscillatore' e aperto il pannello corrispondente.
Da qui per iniziare una presa dati è necessario inserire un path dove salvare i dati ed un tempo di acquisizione, per poi cliccare 'Begin' (senza path o tempo viene visualizzato un messaggio di errore).

'Clear' azzera tutti i campi della schermata (compreso il plot).

'Display Data' permette di visualizzare il file specificato nel campo per il path.

Con un path esistente inserito è possibile cliccare 'PlotFit' per aprire la schermata di visualizzazione e fit (viene creato un oggetto della classe 'FitPanel').

## PlotFit
'Fit' esegue un fit ai dati (tutti, a meno di diverse indicazioni) e visualizza la curva risultante e i valori dei parametri fittati. I valori iniziali dei parametri possono essere costretti nel pannello sulla destra.

Attenzione: se si decide di costringere i parametri è necessario farlo per tutti (o aggiungere tantissime eccezioni nel codice)
## Generare dati 
Con:

`python gen_data.py`

Viene generato un file "sin_data.txt" di dati secondo la funzione con cui poi vengono fittati nel programma (solo per testare che il fit funzioni)
