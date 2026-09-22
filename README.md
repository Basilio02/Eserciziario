# 📚 Eserciziari Informatica

Repository per la creazione di eserciziari in LaTeX per studenti delle materie informatiche (TPS, TIC, ...). Ogni libro genera automaticamente esercizi dinamici utilizzando script Python integrati.

---

## 📖 Indice

- [Panoramica](#panoramica)
- [Struttura della Repository](#struttura-della-repository)
- [Come Creare un Nuovo Libro](#come-creare-un-nuovo-libro)
- [Funzionamento degli Script Python](#funzionamento-degli-script-python)
- [Requisiti](#requisiti)
- [Licenza](#licenza)

---

## Panoramica

Questo progetto permette di creare eserciziari didattici per istituti tecnici informatici combinando **LaTeX** per l'impaginazione e **Python** per generare esercizi dinamici. Ogni libro è contenuto in una cartella autonoma e può essere compilato indipendentemente dagli altri.

---

## Struttura della Repository

```
repository/

├── Libro1/
│   ├── libro.png
│   ├── main.tex
│   ├── libraries.tex
│   ├── generate.sh
│   └── generate/
│       ├──script1.py
|       └──...
├── Libro2/
│   └── ...
├── scripts/
│   ├── Dec2Bin.py
│   ├── SommaBinaria.py
│   └── ...
└── README.md
```

---

## Come Creare un Nuovo Libro

### 1. Creare la Cartella del Libro

All'interno della cartella `libri/`, crea una nuova cartella con il nome del tuo libro (es. `TPS_2025`):

```bash
cd libri
mkdir TPS_2025
cd TPS_2025
```

### 2. Aggiungere la Copertina

Inserisci nella cartella appena creata un'immagine chiamata **`libro.png`**. Questa sarà usata come copertina del libro.

### 3. Copiare la Struttura Base

Copia tutti i file da uno dei libri esistenti (es. `Libro1`) nella tua nuova cartella:

```bash
cp ../Libro1/* .
```

In alternativa, puoi copiare manualmente i file essenziali:
- `main.tex` (il file LaTeX principale)
- `libraries.tex` (il file LaTeX contenente le librerie necessarie per il libro)
- `generate.sh` (lo script di compilazione)

### 4. Personalizzare il Libro

Apri il file `main.tex` e modifica le seguenti sezioni:

#### Cambiare il Colore Principale

Nella prima riga del file `libraries.tex`, trova la definizione del colore:

```latex
\definecolor{maincolor}{RGB}{0,102,204}
```

Modifica i valori RGB per cambiare il colore tema del libro.

#### Cambiare l'Immagine di Background

Alla **riga 19**, trova l'inclusione della grafica:

```latex
\includegraphics[width=\paperwidth,height=\paperheight]{libro.png}
```

Assicurati che il file `libro.png` nella cartella sia l'immagine che vuoi usare come copertina.

#### Scrivere il Contenuto del Libro

Ogni esercizio va inserito in un ambiente esercizio, specificando la difficoltà (da 1 a 3) come parametro, al suo interno scrivere il testo dell'esercizio; successivamente grazie al if soluzioni è possibile preparare anche le soluzioni per l'esercizio.

```latex
\begin{esercizio}[1]
    Testo dell'esecizio
    \ifsoluzioni
        \solution

        Soluzione dell'esercizio
    \fi
\end{esercizio}
```


Dopo la sezione iniziale, puoi iniziare a scrivere i capitoli e gli esercizi del tuo libro. Per includere esercizi generati dinamicamente, usa la sintassi mostrata nella sezione [Funzionamento degli Script Python](#funzionamento-degli-script-python).

### 5. Compilare il Libro

Per generare il PDF, esegui lo script `generate.sh` **due volte** dalla cartella del libro, per generare il file del libro e il libro con le soluzioni

```bash
chmod +x generate.sh  # Solo la prima volta, per rendere eseguibile lo script
./generate.sh
./generate.sh
```

> ⚠️ **Nota:** La prima esecuzione genera i file temporanei con gli esercizi Python; la seconda compilazione include correttamente questi file nel documento finale.

Lo script esegue automaticamente:
```bash
pdflatex -shell-escape main.tex
```

L'opzione `-shell-escape` è necessaria per permettere a LaTeX di eseguire gli script Python esterni.

---

## Funzionamento degli Script Python

Gli script Python nella cartella `scripts/` generano dinamicamente contenuti LaTeX che vengono inclusi nel documento finale. Ecco come funziona il meccanismo:

### Sintassi di Integrazione

Nel file `main.tex`, usa questa struttura per chiamare uno script Python:

```latex
\immediate\write18{python3 ./../scripts/NomeScript.py "argomenti" > temp/nome_output.tex}
\input{./temp/nome_output.tex}
```

### Esempi Pratici

**Esempio 1: Conversione Decimale-Binario**

```latex
\immediate\write18{python3 ./../scripts/Dec2Bin.py 18 > temp/somme_ex_2.tex}
\input{./temp/somme_ex_2.tex}
```

Questo comando:
1. Esegue `Dec2Bin.py` passando il numero `18` come argomento
2. Reindirizza l'output LaTeX generato in `temp/somme_ex_2.tex`
3. Include il file generato nel documento

**Esempio 2: Somma Binaria**

```latex
\immediate\write18{python3 ./../scripts/SommaBinaria.py "41+18" > temp/somme_ex_3.tex}
\input{./temp/somme_ex_3.tex}
```

Questo comando:
1. Esegue `SommaBinaria.py` passando l'espressione `"41+18"`
2. Genera automaticamente l'esercizio con la soluzione in formato LaTeX
3. Include il risultato nel documento

### Come Funzionano gli Script

Ogni script Python:
1. **Riceve argomenti** dalla riga di comando (es. numeri, espressioni matematiche)
2. **Elabora i dati** (conversioni, calcoli, verifiche)
3. **Stampa output in formato LaTeX** (comandi LaTeX, tabelle, esercizi strutturati)
4. L'output viene **catturato da `\write18`** e salvato in un file `.tex` temporaneo
5. Il file temporaneo viene **incluso nel documento** con `\input{}`

Questo approccio permette di creare **eserciziari infiniti** con valori sempre diversi, ideali per verifiche e esercitazioni.

---

## Requisiti

Per compilare i libri è necessario avere installato:

- **TeX Live** o **MiKTeX** (con supporto a `pdflatex`)
- **Python 3** (per eseguire gli script di generazione esercizi)
- **Bash** (per eseguire `generate.sh` su Linux/macOS; su Windows usa WSL o Git Bash)

Assicurati che LaTeX sia configurato per permettere l'esecuzione di comandi shell (`-shell-escape`).

---

## Licenza

Questo progetto è distribuito sotto licenza [MIT](LICENSE).

---

## 📧 Contatti

Per segnalazioni, problemi o contributi, apri una issue su GitHub o contatta i maintainer della repository.