# Azure — SLA pubblici: ampliamento catalogo v3.0.9

Data di verifica: 13 novembre 2026. Questa tabella integra la prima tranche di [AZURE_SLA_MATRIX.md](AZURE_SLA_MATRIX.md).

**Principio**: il target pubblico Microsoft può essere mostrato senza conoscere il tenant, ma **non** deve essere associato in automatico al deployment del cliente quando dipende da tier, numero di repliche, zone o metriche specifiche. Non si conclude conformità SLA in base alle sole PIR pubbliche.

| Servizio canonico | Target pubblico | Configurazione / metrica | Fonte Microsoft |
|---|---|---|---|
| Azure App Service | 99,95% | Web Apps, piani coperti (non Free/Shared) | https://learn.microsoft.com/it-it/azure/azure-resource-manager/management/azure-subscription-service-limits |
| Azure Front Door | 99,99% | Operazioni GET HTTP riuscite | https://learn.microsoft.com/en-us/azure/well-architected/reliability/metrics |
| Azure Container Apps | 99,95% | App distribuita raggiungibile tramite ingress integrato | https://learn.microsoft.com/en-us/azure/well-architected/reliability/metrics |
| Azure Private Link | 99,99% | Connettività Private Endpoint / Private Link | https://learn.microsoft.com/en-us/azure/well-architected/reliability/metrics |
| Azure SQL Database | 99,99% | SQL Database Basic / Standard / General Purpose, disponibilità servizio | https://learn.microsoft.com/en-us/answers/questions/400808/sla-of-azure-sql-database-standard-tier |
| Azure AI Search | 99,9% | Tier Dedicated con almeno 2 repliche per query o 3 per query e indicizzazione | https://learn.microsoft.com/en-us/azure/search/search-modeling-multitenant-saas-applications |
| Azure Cosmos DB | 99,99% | Account singola region, disponibilità | https://learn.microsoft.com/en-us/azure/cosmos-db/table/support |
| Azure Cosmos DB | 99,999% | Letture in account multi-region | https://learn.microsoft.com/en-us/azure/cosmos-db/table/support |
| Event Hubs | 99,9% | Standard | https://learn.microsoft.com/en-us/azure/well-architected/service-guides/azure-event-hubs |
| Event Hubs | 99,99% | Dedicated | https://learn.microsoft.com/en-us/azure/well-architected/service-guides/azure-event-hubs |
| Azure Load Balancer | 99,99% | Standard Load Balancer distribuito su Availability Zones | https://learn.microsoft.com/en-us/azure/well-architected/mission-critical/mission-critical-networking-connectivity |
| Service Bus | 99,9% | Queue e Topic, operazioni di messaggistica | https://learn.microsoft.com/en-us/answers/questions/351065/maintenance-of-underlying-infrastructure-runtime-f |

I valori sono riferimenti pubblici per le configurazioni elencate; la versione contrattuale applicabile resta quella del Microsoft SLA Online Services:
https://www.microsoft.com/licensing/docs/view/Service-Level-Agreements-SLA-for-Online-Services

## Dashboard HTML v3.0.9

La nuova dashboard locale visualizza **15 prodotti canonici** con almeno una configurazione mappata (inclusi i 5 originali e 10 aggiuntivi), con alias di inventario visualizzati separatamente ma non conteggiati due volte. I servizi senza target ancora verificato riportano la dicitura breve “Target pubblico in verifica” e il link alla fonte. Le voci commerciali, di billing o sottoposte ad altro accordo non ricevono un SLA tecnico fittizio.

L'acquisizione Azure appare come barra compatta con indicatore di salute della lettura del JSON; URL, import manuale e backup sono accessibili da un accordion. Lo stato verde indica **acquisizione riuscita e recente**, non uptime dei workload Azure.

La versione HTML v3.0.9 è distribuita separatamente come file locale, non è inclusa in questa PR documentale. Il codice Google Cloud e il PDF v2.9 non sono stati modificati.

## Test di accettazione

- Tab Azure: pannello dati compatto; dettagli aperti e chiusi senza perdere aggiornamento automatico.
- Errore JSON: indicatore di avviso, dati archiviati preservati; JSON recente: indicatore verde.
- SLA Azure: ricerca per servizio, visualizzazione target pubblici e delle varianti, selezioni persistenti, export JSON.
- PDF Azure: target configurazioni selezionate; nessuna falsa stima di downtime da PIR con date senza orario.
- Tab GCP: HTML, motore JS e report PDF senza modifiche.

## Estensione v3.1.4 — Application Gateway

Fonte Microsoft ufficiale: https://learn.microsoft.com/en-us/azure/application-gateway/overview-v2 e criteri di affidabilità https://learn.microsoft.com/en-us/azure/reliability/reliability-application-gateway-v2

| Servizio | Variante | Target pubblico | Condizioni e limiti |
|---|---|---:|---|
| Azure Application Gateway v2 | Basic (preview) | 99,9% | SKU preview, applicabilità contrattuale da verificare |
| Azure Application Gateway v2 | Standard_v2 | 99,95% | Gateway configurato correttamente, con autoscale o ridondanza di zona secondo la documentazione Microsoft |

Nel file HTML locale **v3.1.4** la variante `Standard_v2` è selezionata come riferimento pubblico, modificabile e *non* confermata per il deployment aziendale. Il catalogo copre così 16 prodotti canonici con almeno una variante SLA. Il report Azure usa adesso lo stesso linguaggio grafico e le stesse sezioni del PDF Google v2.9, mantenendo `n.d.` per minuti e disponibilità non supportati dalle evidenze pubbliche. Il modulo Google non cambia.

### Collaudo
- Verificare entrambe le varianti Application Gateway e la selezione predefinita unica.
- Generare un report Azure con 16 SLA: quattro pagine A4 landscape nel caso di test, con cover executive, due region e metodologia.
- Verificare che gli eventi PIR abbiano una data senza finto orario di disservizio e che le durate rimangano `n.d.`.
- Verificare il report Google precedente senza regressioni.
