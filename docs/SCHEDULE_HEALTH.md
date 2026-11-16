# GitHub Actions — raccolta periodica Azure

La dashboard non è un sistema di allarme in tempo reale. A partire dalla **v3.1.10**, il raccoglitore Azure viene eseguito **martedì, giovedì e sabato alle 07:17 UTC** (`17 7 * * 2,4,6`), con intervalli nominali di **2–3 giorni**.

## Criteri operativi
- Un'esecuzione con `event=schedule` e risultato `success` conferma una raccolta; una `push` o `workflow_dispatch` non prova la regolarità della schedulazione.
- Il campo `fetched_at` del JSON pubblico indica quando è stata effettivamente eseguita la raccolta, anche con RSS senza nuovi eventi.
- La dashboard mostra un avviso di fonte non recente dopo **4 giorni** (5760 minuti) senza raccolta, soglia comprensiva di margine rispetto all'intervallo normale.
- GitHub Actions può ritardare o saltare run programmate. L'assenza di incidenti nel feed pubblico non prova disponibilità al 100% né il rispetto degli SLA.
- Esecuzione manuale disponibile con `workflow_dispatch` per aggiornare il feed prima di un report direzionale.

Workflow: https://github.com/jeckodevelopment/multicloud-monitor/actions/workflows/update-azure-feed.yml

### Verifiche da svolgere
1. Controllare che la successiva run `schedule` dopo la PR usi il nuovo calendario.
2. Verificare che `docs/azure-feed.json` si aggiorni e preservi lo storico PIR.
3. Aprire l'HTML v3.1.10 e verificare che un feed di 3 giorni non sia marcato come obsoleto; dopo 4 giorni deve scattare l'avviso.
4. Verificare che il backup e i report Google/Azure funzionino come prima.

La cronologia prima della v3.1.10 conteneva run programmate riuscite ma con intervalli irregolari rispetto all'originaria frequenza di 30 minuti; quel requisito è stato esplicitamente ritirato.
