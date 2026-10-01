# Data Privacy and Repository Safety

This repository is public. Treat operational source data as potentially sensitive.

## Never commit

Do not commit raw dispatch workbooks or files containing:
- customer names,
- phone numbers,
- email addresses,
- exact street/house-number addresses,
- order-level personal notes,
- API keys/tokens,
- private credentials,
- address-level road/cache data that can reconstruct customer locations.

The historical 343-task workbook and other real operational inputs should remain outside the public repository unless explicitly sanitized.

## Allowed repository evidence

Prefer:
- code,
- configuration without secrets,
- synthetic or irreversibly sanitized fixtures,
- city/postcode-level aggregated diagnostics,
- summary metrics,
- tests built from invented examples,
- regression summaries that do not reveal customer-level data.

If a postcode is sufficiently granular to identify a household when combined with other fields, aggregate it further before committing.

## Working with real data

Agents may read real local/private data when authorized and available in their execution environment, but must keep it outside Git.

Generated reports intended for commit must be checked for personal data first.

## Release artifacts

Built EXE/ZIP outputs should not be committed directly to the source tree by default. Publish through an explicitly approved release process after review.

## Security incident rule

If sensitive data is accidentally committed, stop normal work and report the exact commit/path immediately. Do not assume deleting the file in a later commit removes it from Git history.
