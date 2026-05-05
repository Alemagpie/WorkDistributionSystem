Email -> Task:
- Email arriva
- Ogni 30s l'applicazione fa un fetch dell'IMAP
- Un parsing avviene sulla mail: corpo, oggetto e allegati sono letti
- Nel db è aggiunta una nuova task con stato "nuovo"
- Dopo x ore dall'assegnazione allo stato "completato", il lavoro è rimosso dalla vista e rimane nel db