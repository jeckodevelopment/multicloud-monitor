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

## Estensione v3.1.7 — Azure Firewall

Fonte Microsoft: https://learn.microsoft.com/en-us/azure/firewall/deploy-availability-zone-powershell

| Prodotto | Variante | SLA pubblico | Condizioni |
|---|---|---:|---|
| Azure Firewall | Regional | 99,95% | Deployment regionale in region senza Availability Zones |
| Azure Firewall | Zone redundant | 99,99% | Deployment su almeno **due** Availability Zones |

La v3.1.7 aggiunge una variante preselezionata *solo come valore di riferimento*. Non è possibile derivare dalla lista servizi quale topologia sia effettivamente utilizzata in Italy North o Germany West Central. In particolare, la variante regionale non costituisce una garanzia applicabile a qualunque deployment in una region che supporta zone. La scelta deve essere verificata rispetto all'infrastruttura.

La dashboard ora mappa **17 servizi canonici** con SLA pubblico, non 17 voci necessariamente distinte in inventario. Restano servizi da qualificare, inclusi quelli con condizioni contrattuali particolari.

### Verifiche v3.1.7

- Apertura HTML locale e preselezione Azure Firewall.
- Due alternative nella configurazione SLA, con selezione mutuamente esclusiva.
- PDF Azure con pagina autonoma per registro incidenti Italy North e per Germany West Central.
- GCP e relativo layout PDF invariati.
- Non usare il PDF pubblico per dedurre minuti di downtime dai soli timestamp PIR.

## Estensione v3.1.8 — Varianti SLA multiple e topologia intra-region

La selezione delle varianti SLA **non è più mutuamente esclusiva** per servizio canonico in Azure. Lo stesso servizio può comprendere istanze con deployment diversi; nel PDF ogni variante selezionata occupa una propria riga. La selezione salvata è migrata al formato `multicloud-azure-sla-selections-v5` senza perdere le scelte precedenti.

**Impostazioni predefinite del perimetro dichiarato:**

| Servizio | Varianti contemporaneamente attive | Target pubblico |
|---|---|---:|
| Azure Virtual Machines | VM singola con disco Premium SSD / Ultra / Premium SSD v2 | 99,9% |
| Azure Virtual Machines | Almeno due VM in Availability Set, nella stessa region | 99,95% |
| Azure Database for PostgreSQL Flexible Server | Senza HA, server singolo | 99,9% |
| Azure Database for PostgreSQL Flexible Server | HA same-zone (standby nella stessa zona e region) | 99,95% |

La configurazione multi-region per Azure Cosmos DB **non è preselezionata**, perché il perimetro dell'utente comprende solo ridondanza interna a una singola region. Qualsiasi valore SLA dipende comunque dalla configurazione reale, che il monitor pubblico non può leggere.

**Google Cloud SQL** ha invece due varianti HA supportate dalla fonte pubblica, entrambe attive: Enterprise HA (99,95%) ed Enterprise Plus HA (99,99%). La documentazione SLA ufficiale non fornisce in quella tabella un obiettivo contrattuale per istanze Cloud SQL prive di HA: **non attribuire loro un valore SLA inventato**.

Fonti:
- https://learn.microsoft.com/en-us/azure/postgresql/configure-maintain/quickstart-create-server
- https://cloud.google.com/sql/sla
- https://cloud.google.com/compute/sla

### Report direzionale Azure
La frase "Il registro incidenti della region è riportato nella pagina successiva, per evitare interruzioni fra le tabelle SLA e gli eventi." è stata rimossa. I registri Italy North e Germany West Central continuano a iniziare ciascuno su una pagina dedicata.

### Comportamenti da collaudare
- [ ] Prima apertura: VM singola e Availability Set selezionate contemporaneamente.
- [ ] PostgreSQL Flexible Server: senza HA e HA same-zone selezionate contemporaneamente.
- [ ] Una terza variante dello stesso servizio si può selezionare senza deselezionare le prime.
- [ ] Le selezioni persistenti precedenti sono migrate al nuovo formato.
- [ ] PDF Azure con varianti multiple e pagine di registro incidenti separate, senza frase di rinvio.
- [ ] Google Cloud SQL: Enterprise HA 99,95% e Enterprise Plus HA 99,99% attive contemporaneamente; nessun target assegnato arbitrariamente a Cloud SQL senza HA.
