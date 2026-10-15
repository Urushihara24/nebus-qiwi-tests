# Security Policy

## Scope

Security reports are welcome for issues involving QIWI credential handling, payment-request safety, test-data isolation, CI configuration, dependency integrity, or accidental execution of live financial actions.

## Reporting

Do **not** publish QIWI tokens, account identifiers, authorization headers, payment identifiers tied to a real account, balances, transaction details, or exploit instructions in a public issue.

Use GitHub private vulnerability reporting when it is available for this repository. If a private report is not available, send a short sanitized summary through the work contact listed on the maintainer profile and keep secrets/payment data out of the initial message.

Include, when possible:

- affected commit and Python version;
- minimal reproduction steps using placeholders;
- expected vs actual behavior;
- whether a live payment, credential exposure, or test/CI isolation boundary is affected;
- sanitized request/response evidence with tokens, account IDs and transaction data removed.

## Live-payment boundary

Pull-request CI must remain non-financial: it may validate syntax, imports, test collection, dependencies, and security tooling, but it must not issue a real payment request.

The live suite includes a payment-creation scenario and must only be run with an explicitly authorized test account/environment where the financial effect is understood.

Never commit `.env`, `QIWI_TOKEN`, `QIWI_ACCOUNT`, production credentials, private payment data, or raw authenticated request captures.