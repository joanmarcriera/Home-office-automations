# New Sources — Daily Intake Logs

This index tracks daily source-ingestion files. Each day gets a dedicated log file in `docs/new-sources/` to avoid overlap between concurrent agents.

## Daily Log Files

| Date | Log File | New | Integrated | Notes |
| :--- | :--- | :---: | :---: | :--- |
| 2026-02-26 | [2026-02-26](/new-sources/2026-02-26/) | 0 | 15 | Daily ingestion plus open-issue catch-up integrations |
| 2026-02-25 | [2026-02-25](/new-sources/2026-02-25/) | 0 | 9 | Initial daily migration |
| 2025-02-25 | [2025-02-25](/new-sources/2025-02-25/) | 0 | 5 | Legacy entries migrated from old monolithic inbox |

## Required Daily Log Schema

Each `docs/new-sources/YYYY-MM-DD.md` file must contain one table with this exact header:

`| Title | URL | Tags | Status | Canonical Page | Notes |`

Allowed values for `Status`:

- `new`
- `integrated`
- `duplicate`
- `needs-more-info`
- `low-confidence`

## Workflow Rules

1. New discoveries are appended only to today's file.
2. Integration updates should only modify status/canonical-page fields in the same row.
3. Do not create free-form sections or mixed formats in daily logs.
4. Keep this index updated with a row for each new day file.
5. In this index table, date links must use `/new-sources/YYYY-MM-DD/` (absolute site path).

## Related

- [Contributing Guide](CONTRIBUTING.md)
- [Standards](standards.md)
