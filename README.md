# Analisi complessità calcolo componenti fortemente connesse
Si vuole analizzare la complessità dell'algoritmo che calcola il numero di componenti fortemente connesse in un grafo diretto.

## Esperimento
Si generano casualmente grafi di diverse dimensioni, variando anche la probabilità di generazione degli archi. Si creano tre grafici in quali si riportano (valori medi su 10 test), in funzione del numero di nodi e della probabilità di generare gli archi:

+ numero di archi
+ numero di componenti fortemente connesse
+ tempo per il calcolo del numero di componenti fortemente connesse

Per eseguire l'esperimento:
`python3 exp.py`