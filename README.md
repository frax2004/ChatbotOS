# ChatbotOS

### Tasks
- **T1** **Creazione file**: Il sistema deve essere in grado di capire che la task richiesta è quella di creare un file, l'untente deve poter fornire la cartella di destinazione [opzionale] e almeno il nome del file con l'estensione se non è presente
- **T2** **Cambiare directory**: Il sistema deve essere in grado di capire che la task richiesta è quella di cambiare la directory corrente in una specificata dall'utente (parametro obbligatorio). Il chatbot deve anche assicurarsi che la cartella obiettivo esista. Il sistema di dialogo infine, chiederà all'utente il permesso di creare la cartella Se essa non esista.
- **T3** **Mostrare la cartella corrente**: Il sistema deve essere in grado di capire che la task richiesta è quella di mostrare la directory corrente. Il chatbot deve anche assicurarsi che la cartella obiettivo esista.
- **T4** **Rinomiare la cartella corrente**: Il sistema deve essere in grado di capire che la task richiesta è quella di rinominare la cartella corrente in un nome specificato dall'utente. 
  - Se la cartella non esiste, il chatbot chiederà il permesso di crearla.
  - Se il nome di destinazione coincide con una cartella gia esistente allora il chatbot dovrà avvertire l'utente e richidere il nome di destinazione
  - Se il percorso base di destinazione non coincide con il percorso base sorgente allora il chatbot dovrà avvertire l'utente e chiedere conferma di spostamento.



#### T1: Creazione file
`Frame`

|Campo|
|-|
|Nome del file|
|Estensione del file|
|[Directory]|

