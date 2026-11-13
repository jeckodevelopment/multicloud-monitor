# Azure — SLA standard, matrice iniziale (13 novembre 2026)

## Scopo
Inventario di riferimento: **72 voci Azure** (comprese denominazioni duplicate, commerciali e di billing). La prima tranche di mappatura documentata copre **5 prodotti canonici**, con **20 varianti**. Per tutte le restanti voci lo SLA resta **da qualificare** oppure **fuori perimetro di uno SLA tecnico Azure**, senza attribuire valori contrattuali presunti.

**Contratto ufficiale di riferimento:** https://www.microsoft.com/licensing/docs/view/Service-Level-Agreements-SLA-for-Online-Services

I valori seguenti sono target di riferimento solo nelle configurazioni indicate e devono essere verificati rispetto al testo contrattuale applicabile, SKU, condizioni ed eventuali esclusioni. Non rappresentano disponibilità misurata né conformità contrattuale.

| Prodotto | Configurazione/metrica | Target | Fonte pubblica |
|---|---|---:|---|
| Azure Kubernetes Service (AKS) | API server Standard/Premium, senza Availability Zones | 99,9% | [AKS tiers](https://learn.microsoft.com/en-us/azure/aks/free-standard-pricing-tiers) |
| Azure Kubernetes Service (AKS) | API server Standard/Premium, con Availability Zones | 99,95% | [AKS tiers](https://learn.microsoft.com/en-us/azure/aks/free-standard-pricing-tiers) |
| Azure Database for PostgreSQL | Flexible Server senza HA | 99,9% | [PostgreSQL reliability](https://learn.microsoft.com/en-us/azure/reliability/reliability-postgresql-flexible-server) |
| Azure Database for PostgreSQL | Flexible Server HA nella stessa zona | 99,95% | [PostgreSQL reliability](https://learn.microsoft.com/en-us/azure/reliability/reliability-postgresql-flexible-server) |
| Azure Database for PostgreSQL | Flexible Server HA zone-redundant | 99,99% | [PostgreSQL reliability](https://learn.microsoft.com/en-us/azure/reliability/reliability-postgresql-flexible-server) |
| Azure Storage | Richieste di lettura LRS / Hot | 99,9% | [Storage redundancy](https://learn.microsoft.com/en-us/azure/storage/common/storage-redundancy) |
| Azure Storage | Richieste di lettura RA-GRS / Hot | 99,99% | [Storage redundancy](https://learn.microsoft.com/en-us/azure/storage/common/storage-redundancy) |
| Azure Storage | Richieste di lettura RA-GZRS / Hot | 99,99% | [Storage redundancy](https://learn.microsoft.com/en-us/azure/storage/common/storage-redundancy) |
| Azure Storage | Richieste di scrittura, ridondanze supportate / Hot | 99,9% | [Storage redundancy](https://learn.microsoft.com/en-us/azure/storage/common/storage-redundancy) |
| Azure Virtual Machines | VM singola Premium SSD / Ultra / Premium SSD v2 | 99,9% | [VM availability](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/scenarios/azure-virtual-desktop/eslz-business-continuity-and-disaster-recovery) |
| Azure Virtual Machines | VM singola Standard SSD | 99,5% | [VM availability](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/scenarios/azure-virtual-desktop/eslz-business-continuity-and-disaster-recovery) |
| Azure Virtual Machines | VM singola Standard HDD | 95% | [VM availability](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/scenarios/azure-virtual-desktop/eslz-business-continuity-and-disaster-recovery) |
| Azure Virtual Machines | 2+ VM in Availability Set | 99,95% | [Availability Sets](https://learn.microsoft.com/en-us/azure/virtual-machines/availability-set-overview) |
| Azure Virtual Machines | 2+ VM in Availability Zones | 99,99% | [VM availability](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/scenarios/azure-virtual-desktop/eslz-business-continuity-and-disaster-recovery) |
| Azure Functions | Flex Consumption (Function App) | 99,95% | [Functions](https://azure.microsoft.com/en-us/products/functions/) |
| Azure Functions | App Service Plan (Function App) | 99,95% | [Functions](https://azure.microsoft.com/en-us/products/functions/) |

> Il catalogo HTML contiene 16 righe esplicitate in questa matrice: 2 AKS + 3 PostgreSQL + 4 Storage + 5 VM + 2 Functions = **16**, non 20. Il conteggio sorgente è la somma delle varianti effettivamente documentate.

## Esclusioni e stato non conclusivo
Non assegnare uno SLA Azure tecnico alle voci di billing o procurement, tra cui Reservations, Savings Plan, RoundingAdjustment e Bandwidth. Trattare Microsoft Fabric, Power Platform, GitHub Enterprise Cloud, Visual Studio e analoghi con il pertinente accordo specifico, senza dedurre che il loro SLA sia quello dell'infrastruttura Azure.

Per servizi con SLA diverso per tier, ridondanza, scenario di distribuzione o servizio incorporato, **non scegliere automaticamente una variante**.

## Integrazione dashboard
Nel file locale `Cloud Service Monitor v3.0.7` è disponibile la selezione persistente delle varianti SLA e un'esportazione JSON delle configurazioni scelte; il report PDF Azure riporta tali target separatamente dagli incidenti pubblici. Il modulo GCP v2.9 e il relativo layout PDF rimangono invariati.

## Cosa collaudare
- Aprire tab Azure; inventario 72 voci.
- Filtro Varianti documentate; verificare le **16 configurazioni** relative ai cinque prodotti.
- Selezione di una o più varianti; verifica di ricerca e aggiornamento del contatore.
- Aprire le fonti Microsoft, esportare le selezioni JSON.
- Generare PDF Azure e verificare tabella target separata dai conteggi incidenti.
- Verificare report PDF Google identico a v2.9 (nessuna modifica GCP).
