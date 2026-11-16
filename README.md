# Multicloud Monitor

Dashboard **Google Cloud + Microsoft Azure** in un unico file HTML, utilizzabile localmente su Windows 11 (e altri browser desktop) senza server web locale, installazione o credenziali dei cloud provider.

## Dashboard — versione 3.1.10

**[Scarica il file HTML v3.1.10](dashboard/cloud_service_monitor_multicloud_v3_1_10.html)**

1. Apri il file nella repository e usa **Download raw file** (oppure scaricalo dal link sopra).
2. Salvalo sul tuo PC e aprilo con un browser moderno (`file://`).
3. Seleziona la scheda **Google Cloud** o **Microsoft Azure**.
4. Esporta il report direzionale del mese con la stampa in PDF del browser.
5. Le preferenze sono conservate dal browser in `localStorage`; usa le funzioni di backup/ripristino prima di cambiare PC o browser.

Il codice HTML è autonomo: **non richiede build, npm, server, tenant Azure o accesso alle API aziendali**. Il recupero *automatico* degli incidenti pubblici richiede però accesso Internet ai domini Google Cloud e GitHub; senza rete si possono usare le funzioni di importazione/backup previste dalla dashboard. L'applicazione **non** misura direttamente la disponibilità dei workload aziendali.

### Perimetro e privacy

Questa repository è **pubblica**. Il file HTML incorpora il catalogo dei servizi cloud monitorati, le region di riferimento e le selezioni SLA iniziali; non pubblicare qui configurazioni, credenziali, dati di workload o dettagli aziendali non autorizzati. Verificare le policy aziendali prima di condividere o distribuire il file. Le preferenze salvate nel browser **non** vengono committate automaticamente su GitHub.

### SLA e report PDF

I target SLA pubblicati dai provider dipendono da SKU, ridondanza e architettura effettiva: quelli presenti nel catalogo sono **riferimenti selezionabili** e non attestano l'applicabilità contrattuale a specifici deployment. La disponibilità **stimata** nei report è ricavata soltanto dalle evidenze pubbliche disponibili e non costituisce prova di rispetto dello SLA né misurazione della disponibilità reale. In particolare, PIR Azure prive di finestre temporali verificabili non devono essere interpretate come assenza di downtime.

Il report Google mantiene l'impostazione approvata v2.9. Nel report Azure i registri incidenti di **Italy North** e **Germany West Central** occupano pagine dedicate.

## Raccoglitore pubblico Azure

GitHub Actions legge il feed RSS di Azure Status, raccoglie le PIR storiche ufficiali e aggiorna `docs/azure-feed.json`, **senza credenziali Azure**.

- Workflow: [`.github/workflows/update-azure-feed.yml`](.github/workflows/update-azure-feed.yml)
- Script: [`scripts/update_feed.py`](scripts/update_feed.py)
- Feed JSON: [`docs/azure-feed.json`](docs/azure-feed.json)
- Fonti: https://rssfeed.azure.status.microsoft/en-us/status/feed/ e https://azure.status.microsoft/

La schedulazione GitHub Actions è configurata **martedì, giovedì e sabato alle 07:17 UTC**, con intervalli previsti di 2–3 giorni. La dashboard segnala una fonte non recente quando l'ultimo `fetched_at` supera **4 giorni**; la soglia ammette ritardi della schedulazione GitHub. GitHub può comunque ritardare o saltare le esecuzioni: controllare `fetched_at` e lo stato del workflow prima di utilizzare i dati. L'assenza di eventi nel feed **non** implica disponibilità del 100%.

## Versioni e manutenzione

La dashboard versionata è in `dashboard/`. Dopo ogni modifica, verificare la sintassi degli script, l'apertura locale, la selezione SLA multipla e la stampa dei PDF per **entrambi** i provider. Non modificare il report Google approvato senza una richiesta esplicita. Lo storico della raccolta e delle estensioni SLA si trova nella cartella `docs/`.
