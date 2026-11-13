# Multicloud Monitor

Monitoraggio locale degli incidenti pubblici Google Cloud e Microsoft Azure.

## Raccoglitore Azure
GitHub Actions acquisisce il feed RSS pubblico Azure e mantiene uno storico JSON cumulativo (`docs/azure-feed.json`), senza credenziali Azure.

- Workflow: `.github/workflows/update-azure-feed.yml`
- Script: `scripts/update_feed.py`
- Fonte: https://rssfeed.azure.status.microsoft/en-us/status/feed/

**Avvertenza:** questa repository e attualmente privata. Finche rimane privata il JSON su `raw.githubusercontent.com` non e accessibile anonimamente dalla dashboard locale. Per renderlo fruibile, pubblicare il solo feed in un endpoint HTTPS autorizzato oppure rendere pubblica la repository (contenente esclusivamente dati pubblici), previa verifica delle policy.

Il feed RSS non prova l'impatto effettivo sui workload aziendali e non certifica gli SLA.
