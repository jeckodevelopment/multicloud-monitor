# Cloud Service Monitor — v3.1.10 (baseline stabile approvata)

**Data di accettazione:** 16 novembre 2026  
**Stato:** approvata dall'utilizzatore dopo collaudo funzionale sul proprio ambiente aziendale.  
**Artefatto congelato:** [cloud_service_monitor_multicloud_v3_1_10.html](../dashboard/cloud_service_monitor_multicloud_v3_1_10.html)  
**SHA del blob Git:** `971cabbb3140e64a4ab5e35d53e98695a330eb05`

## Esito di collaudo

L'utilizzatore ha confermato esplicitamente il **16 novembre 2026**: «perfetto, funziona, ho collaudato il tutto». La conferma si riferisce alla dashboard multicloud v3.1.10 consegnata, nella configurazione concordata.

Il collaudo dichiarato dall'utilizzatore e i controlli automatici costituiscono evidenze distinte; non è disponibile in repository un verbale di test analitico con risultati per ogni singolo caso. Non presentare il test CI come sostituto del collaudo manuale.

## Perimetro approvato

- **Un unico HTML standalone** per Google Cloud e Microsoft Azure, apribile da file locale senza server.
- **Google Cloud:** struttura, report direzionale PDF e comportamento v2.9 approvati e conservati.
- **Microsoft Azure:** catalogo dei servizi del perimetro, selezioni multiple di varianti SLA per servizio, riferimenti di ridondanza nella stessa region, report PDF mensili con registri incidenti regionali su pagine dedicate.
- **SLA:** target pubblici di riferimento, distinti dalle stime di disponibilità ricavate dalle evidenze degli incidenti; nessuna attestazione di conformità contrattuale dei workload.
- **Acquisizione Azure:** GitHub Actions schedulata martedì, giovedì e sabato alle 07:17 UTC; tolleranza di freschezza quattro giorni; aggiornamento manuale sempre disponibile.

## Evidenze tecniche

- PR #21: adeguamento periodicità Azure e dashboard 3.1.10.
- Workflow `Validate standalone dashboard` riuscito sulla PR #21 e su `main` successivamente al merge (16 novembre 2026).
- Sono state osservate esecuzioni riuscite del raccoglitore Azure; la prima esecuzione con il **nuovo calendario** deve essere osservata quando si presenta lo slot programmato.
- I test statici verificano sintassi JavaScript, struttura della dashboard, catalogo Azure e integrità del codice Google congelato.

## Limitazioni note / manutenzione evolutiva

1. Alcune voci Azure sono ancora **da qualificare** rispetto allo SLA pubblico e al relativo SKU: non assegnare percentuali arbitrarie.
2. Incidenti/PIR pubblici Azure potrebbero non contenere una durata regionale verificabile; la disponibilità stimata **non** coincide con quella reale o contrattuale.
3. GitHub Actions può ritardare o saltare le esecuzioni programmate; la dashboard è destinata ad analisi periodiche e non ad allarmi in tempo reale.
4. La repository è **pubblica** e il file HTML include catalogo/region/target di riferimento. Qualsiasi condivisione deve rispettare le policy dell'organizzazione.

## Governance delle versioni

Questa baseline è **congelata funzionalmente**: non sostituire l'HTML v3.1.10 con versioni successive. Eventuali correzioni saranno pubblicate in un **nuovo file versionato**, con PR, test GCP/Azure e nuove note di collaudo. Mantenere l'accesso al file v3.1.10 anche dopo futuri rilasci.

La qualificazione "baseline stabile approvata" è una decisione di progetto registrata in questo documento; **non equivale alla creazione automatica di un tag o di una GitHub Release**, che richiedono operazioni separate.
