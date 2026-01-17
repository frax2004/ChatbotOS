# ChatbotOS

### Requisiti
- Python
  - Package python: nltk
  - Package python: gensim
  - Package python: matplotlib
---

### Installazione
Per i seguenti requisiti si consiglia l'ultizzo di un virtual environment tramite il comando

```bash
python -m venv <nome_venv>
```
per generare il virtual environment, e poi per attivarlo eseguire il comando

```bash
.\venv\bin\activate.bat
```


Installazione delle librerie python
```bash
python -m pip install nltk
python -m pip install gensim
python -m pip install matplotlib
```

Per le dipendenze interne, occorre compilare i comandi: eseguire il file *compile_commands.py*

```bash
python compile_commands.py
```

Questo genererà i dataset dei comandi e salverà sul file *classifier.pickle* il modello del classificatore bayesiano utilizzato dal chatbot.

### Esecuzione

Eseguire il file python *main.py* per avviare una chat con **Eve**, enjoy!