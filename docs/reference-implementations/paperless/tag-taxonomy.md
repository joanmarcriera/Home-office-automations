# Reference Implementation: Paperless Tag Taxonomy

## Core Status Tags
- `inbox`: Document just arrived, needs manual or auto review.
- `needs-action`: Requires a human to perform a task (e.g. pay bill).
- `processed`: Automation has finished its work (e.g. calendar event created).
- `automation-failed`: LLM or script hit an error.

## Category Tags
- `Finance/Bill`
- `School/Correspondence`
- `Health/Record`
- `Admin/Government`

## Retention Tags
- `Keep-7-years`: Tax related.
- `Keep-forever`: Birth certificates, deeds.
- `Ephemeral`: Coupons, flyers.


## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-03-01

## Sources / References
- https://github.com/joanmarcriera/Home-office-automations
