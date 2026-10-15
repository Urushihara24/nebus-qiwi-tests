# Nebus / QIWI Payment API Validation Suite

QA automation implementation for payment-gateway flows based on the QIWI API contract. The repository covers service availability, account balance validation, payment creation, payment-state verification, authenticated test data, and an equivalent Postman collection.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11%20%7C%203.12-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/pytest-34A853?style=for-the-badge&logo=pytest&logoColor=white" alt="pytest">
  <img src="https://img.shields.io/badge/Playwright-APIRequestContext-45BA4B?style=for-the-badge&logo=playwright&logoColor=white" alt="Playwright">
  <img src="https://img.shields.io/badge/Postman-Collection-FF6C37?style=for-the-badge&logo=postman&logoColor=white" alt="Postman">
  <img src="https://img.shields.io/badge/REST-Payment_API-005571?style=for-the-badge" alt="REST API">
  <a href="https://github.com/Urushihara24/nebus-qiwi-tests/actions/workflows/ci.yml"><img src="https://github.com/Urushihara24/nebus-qiwi-tests/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://github.com/Urushihara24/nebus-qiwi-tests/actions/workflows/security.yml"><img src="https://github.com/Urushihara24/nebus-qiwi-tests/actions/workflows/security.yml/badge.svg" alt="Security"></a>
</p>

## Scope

| Area | Validation |
|---|---|
| Service availability | authenticated payment-history request and response structure |
| Funding sources | RUB account discovery and positive-balance validation |
| Payment creation | unique payment ID, amount/currency and transaction state |
| Payment status | follow-up request and transition to `SUCCESS` |
| Test data | credentials and account values supplied only through environment variables |
| API tooling | Python/Playwright suite plus Postman collection |

## Stack

- **Python 3.11 / 3.12**
- **pytest**
- **Playwright `APIRequestContext`** for API-level requests
- **python-dotenv** for local credential loading
- **Postman** collection for manual/interactive contract checks
- **GitHub Actions** for syntax/import/test-collection verification without live payment execution
- **pip-audit** for scheduled and dependency-change security checks

## Repository structure

```text
nebus-qiwi-tests/
├── test_qiwi_api.py
├── Nebus_Qiwi_API.postman_collection.json
├── requirements.txt
├── .gitignore
└── .github/workflows/
    ├── ci.yml
    └── security.yml
```

## Environment

Create a local `.env` file with authorized test data:

```dotenv
QIWI_BASE_URL=https://edge.qiwi.com
QIWI_TOKEN=your_authorized_test_token
QIWI_ACCOUNT=your_authorized_test_account
```

Do not commit tokens, account identifiers, production credentials, or payment data.

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -v -s test_qiwi_api.py
```

> [!CAUTION]
> The suite contains a real payment-creation request. Run live tests only against an account/environment where payment actions are explicitly authorized and the financial effect is understood.

## Implemented scenarios

### 1. Service availability

Requests payment history and verifies HTTP `200`, JSON structure, and the `data` collection.

### 2. Balance validation

Requests funding sources, locates the RUB account (`currency=643`, `type=ACCOUNT`), and validates that balance data is numeric and positive.

### 3. Payment creation

Generates a unique payment identifier and submits a 1 RUB payment request to terminal `99`. The response is validated for ID consistency and an expected transaction state.

### 4. Payment-state verification

Re-reads the created payment and validates successful execution plus amount/currency integrity.

## External-service note

The upstream payment endpoint used by this implementation may be unavailable, restricted, or reject non-production/test credentials. Live HTTP failures therefore need to be separated from test-code failures. CI intentionally validates code integrity and pytest collection without issuing external payment requests.

## Safety boundary

This repository is an API QA implementation, not a payment client for end users. It does not ship credentials and should not be configured with an account that is not explicitly authorized for testing.
