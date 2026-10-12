# Data folder

Place a cleaned, appropriately licensed dataset here when one has been selected and reviewed. Do not commit private customer data, credentials, or files whose license prohibits redistribution.

The current app uses generated synthetic records and does not read a CSV from this folder. When integrating a real dataset:

1. Keep the original source separate from transformed outputs.
2. Record source URL, retrieval date, license, version, and any exclusions.
3. Map columns to the expected schema documented in `docs/KPI_Documentation.md`.
4. Run validation and reconcile totals against the source.
5. Update the app's ingestion layer and disclose unavailable KPIs instead of inventing fields.
