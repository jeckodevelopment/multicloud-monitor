# Azure historical PIR collector

## Scope
This source supplements, and **does not replace**, the public RSS feed with Post Incident Reviews available at https://azure.status.microsoft/en-us/status/history.

Microsoft describes public status history as PIRs for its broadest Scenario 1 events. It is not an exhaustive account of service outages or tenant-specific impact.

## Collected fields
- Microsoft tracking ID, stable archive key pir:<tracking-id>
- PIR title and public history source URL
- Date of the PIR event (00:00 UTC is a placeholder for **date-only**, not downtime start)
- Short description from "What happened?"
- Textual indicators for Italy North and Germany West Central
- \`impact_minutes: null\` and \`impact_precision: not_region_specific\`

No region-specific impact time or SLA is derived from a global incident window. A textual mention of a region is indicative and subject to verification.

## Reliability
\`history_status\` in the JSON is one of:
- \`ok\`: public history produced parseable PIRs;
- \`no_pirs_extracted\`: the page was fetched but the parser could not find PIRs (potential markup change/client rendering);
- \`fetch_error\`: history request failed.

On any history failure the collector continues updating RSS and **retains** prior PIRs. Identifiers are deduplicated across runs. The first collection is limited to PIRs visible in the public history HTML fetched at that moment: it does **not** guarantee complete historical backfill.

## Testing
Run \`python -m unittest discover -s tests -v\`. Verify \`history_status\` and \`history_latest_count\` after the next workflow. Confirm entries with \`id:pir:...\` in \`docs/azure-feed.json\`, and that they appear in the Azure dashboard. No GCP module changes.
