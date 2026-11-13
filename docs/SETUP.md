# Azure public-status collection

The workflow `Update public Azure feed` reads only Microsoft's public RSS feed and stores a cumulative JSON archive at `docs/azure-feed.json`.

## Activation
1. Merge the feed collector PR.
2. In **Actions**, enable workflows if GitHub requests it.
3. In **Actions → Update public Azure feed → Run workflow**, run the first collection manually.
4. Ensure **Settings → Actions → General → Workflow permissions** allows `Read and write permissions`, as the workflow commits the JSON archive.
5. Check that `docs/azure-feed.json` exists and the workflow succeeded.

## Endpoint and visibility
**The repository was private at setup.** Anonymous browser requests to `raw.githubusercontent.com` will fail as long as it remains private. Choose an approved public distribution method for the public-only JSON. If you make *this repository* public (after checking relevant policies), its URL will be:

`https://raw.githubusercontent.com/jeckodevelopment/multicloud-monitor/main/docs/azure-feed.json`

Insert that URL in the Azure data source setting of the local Cloud Service Monitor HTML.

The HTML browser must allow HTTPS fetch from the chosen endpoint. If the corporate network blocks the host, use a network/security-approved static publication channel rather than a CORS bypass proxy.

## Notes
- Updates scheduled at minute 17 and 47 of each hour; GitHub schedules are best effort.
- GitHub Actions failure or RSS changes must be investigated; do not infer zero incidents from an outdated archive.
- Only public status incidents are collected. No tenant or company identifiers, metrics, Azure credentials, tickets, or confidential documents are accessed.
- RSS publication dates are not automatically equivalent to downtime durations or SLA measurements.
- Deduplication uses RSS GUID, preserving history as long as GUIDs remain stable.
