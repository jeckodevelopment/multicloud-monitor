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


## Historical backfill from official PIR tracking IDs
The public history page's default HTML contains only the most recent PIRs. Some earlier incidents remain accessible through the official URL \`https://azure.status.microsoft/en-us/status/history/?trackingId=ID\`.

The curated public identifiers in \`docs/azure-history-seeds.json\` are routing references only. The script imports the incident description, region indications and date **exclusively from Microsoft's page**. Existing records are skipped on subsequent runs; each ID is imported only once and deduplicated with the live collection.

The seed list does not imply comprehensive coverage. Source notices are not customer-specific SLA proof; all historic entries retain \`impact_minutes: null\`. A failed or missing tracking ID is reported in \`history_seed_failures\` and is never invented.

Review the official PIR before adding a new ID to the seed list.
