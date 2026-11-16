# Verifica pre-release — Cloud Service Monitor v3.1.9

Verifica eseguita il **16 novembre 2026** sulla dashboard autonoma già pubblicata. Questo documento non equivale a collaudo su PC aziendale.

## Raccolta Azure

- Il workflow `Update public Azure feed` è presente su `main`, con cron dichiarato `13,43 * * * *`.
- Sono state osservate **11 run con `event=schedule`**, tutte `success` al momento della verifica (13–16 novembre 2026).
- Ultima esecuzione osservata: **2026-11-16T07:15:10Z**.
- Ultimo `docs/azure-feed.json` osservato: **2026-11-16T07:15:16Z**, con 11 PIR storiche e `history_status=ok`.
- **Criticità aperta:** gli intervalli effettivi fra run osservate sono di varie ore, non di 30 minuti. Il cron definisce la frequenza desiderata ma il servizio GitHub Actions non garantisce puntualità. Il successo del job non comprova il rispetto della cadenza.

**Criterio di accettazione:** osservare per almeno 24 ore la successione delle run programmate e registrare età del JSON e slot saltati. Per requisiti rigorosi di freschezza serve uno scheduler con garanzie e monitoraggio dedicato; la schedulazione GitHub gratuita non deve essere rappresentata come un servizio con SLA di 30 minuti.

## Inventario Azure e SLA

Audit statico del catalogo HTML v3.1.9:

| Stato | Voci inventario |
|---|---:|
| Varianti SLA pubbliche documentate | 20 |
| Target da qualificare | 42 |
| Non applicabili come SLA tecnico Azure | 10 |
| **Totale** | **72** |

Le 20 voci includono alias di prodotti canonici, e quindi **non** costituiscono 20 prodotti distinti. Non assegnare target numerici alle 42 voci senza prova Microsoft ufficiale e precisa corrispondenza di tier, region e metrica. Le varianti predefinite restano ipotesi di riferimento, non prova di configurazione aziendale.

Categorie da affrontare per prime: database (MySQL, Redis), rete (ExpressRoute, NAT Gateway, Key Vault), integrazione e messaggistica (Event Grid, Logic Apps, SignalR), piattaforma dati (Data Factory, Databricks). Seguire la documentazione contrattuale Microsoft, non articoli non ufficiali.

## Report e controlli

La v3.1.9 conserva:
- Report PDF Google v2.9 e relativo script applicativo congelati: il test automatico controlla l'hash SHA-256 dello script Google.
- PDF Azure: registri regionali Italy North e Germany West Central su pagine dedicate; stima di disponibilità solo quando supportata dalle finestre pubbliche disponibili; dati inconcludenti distinti da indisponibilità zero.
- Catalogo con più varianti SLA selezionabili per stesso servizio.
- File HTML autonomo apribile localmente senza server web.

### Collaudi non sostituibili dalla CI

- Aprire il file via `file://` nel browser aziendale.
- Verificare accessibilità della fonte JSON pubblica e gestione del caso rete non disponibile.
- Eseguire backup/ripristino e prova di migrazione delle selezioni esistenti.
- Generare i PDF di entrambi i provider su diversi mesi e con registri lunghi.
- Controllare che il file pubblicato e il perimetro in chiaro siano autorizzati alla pubblicazione nella repository **pubblica**.

## Test automatici

La workflow `Validate standalone dashboard` esegue `tests/test_dashboard_release.py`: integrità script Google, struttura pannelli e PDF, conteggi dei 72 servizi e parsing/sintassi JavaScript con Node. Questa è una **protezione minima contro regressioni statiche**, non un collaudo end-to-end né una verifica della correttezza contrattuale di ciascuno SLA.
