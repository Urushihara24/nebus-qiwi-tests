# API Tests for MCC “Luna” (Nebus)

Test assignment solution: validating a payment gateway API based on QIWI documentation.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/pytest-34A853?style=for-the-badge&logo=pytest&logoColor=white" alt="pytest">
  <img src="https://img.shields.io/badge/Playwright-45BA4B?style=for-the-badge&logo=playwright&logoColor=white" alt="Playwright">
  <img src="https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white" alt="Postman">
</p>

## Stack

- **Python 3.12** + **pytest**
- **Playwright** (`APIRequestContext`)
- **Postman** (collection included)

## Run

1. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate # Linux/macOS
    # venv\Scripts\activate # Windows
    ```
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    playwright install
    ```
3. Create a `.env` file in the project root with test data:
    ```env
    QIWI_BASE_URL=https://edge.qiwi.com
    QIWI_TOKEN=your_test_token
    QIWI_ACCOUNT=your_test_phone_number
    ```
4. Run the tests:
    ```bash
    pytest -v -s test_qiwi_api.py
    ```

## What is tested

1. **Service availability**: GET request to payment history. Verifies HTTP 200 and the response structure, including the `data` key.
2. **Balance check**: GET request to funding sources. Finds a RUB account (`currency: "643"`, `type: "ACCOUNT"`) and strictly verifies `balance > 0`.
3. **Payment creation**: PUT request to create a payment (terminal `99` — mobile phone). Generates a unique `payment_id` and submits a 1 RUB payment.
4. **Payment execution**: GET request to retrieve the status of the previously created payment. Verifies transition to `SUCCESS` and the correct amount for the generated `payment_id`.

> [!NOTE]
> According to the assignment, the service is not operational. The tests are therefore expected to fail with HTTP errors such as 401/404/500 when test tokens are used. The code demonstrates test architecture, `.env` configuration, and passing data between test steps.