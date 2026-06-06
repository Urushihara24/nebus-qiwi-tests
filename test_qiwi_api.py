import os
import uuid
import time
import pytest
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("QIWI_BASE_URL", "https://edge.qiwi.com")
TOKEN = os.getenv("QIWI_TOKEN", "test_token")
ACCOUNT = os.getenv("QIWI_ACCOUNT", "79000000000")

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Глобальная переменная для передачи payment_id между тестами
current_payment_id = None

@pytest.fixture(scope="module")
def api_request():
    """Фикстура для создания API-контекста Playwright"""
    with sync_playwright() as p:
        request_context = p.request.new_context(
            base_url=BASE_URL,
            extra_http_headers=HEADERS
        )
        yield request_context
        request_context.dispose()

def test_01_service_availability(api_request):
    """1. Проверка доступности сервиса"""
    response = api_request.get(f"/payment-history/v2/persons/{ACCOUNT}/payments", params={"rows": 1})
    
    assert response.status == 200, f"Ожидался 200, получен {response.status}"
    data = response.json()
    assert "data" in data, "В ответе отсутствует ключ 'data'"
    assert isinstance(data["data"], list), "Ключ 'data' должен быть массивом"

def test_02_balance_check(api_request):
    """2. Проверка баланса (должен быть > 0)"""
    response = api_request.get(f"/funding-sources/v2/persons/{ACCOUNT}/accounts")
    
    assert response.status == 200, f"Ожидался 200, получен {response.status}"
    data = response.json()
    
    rub_account = next((acc for acc in data["accounts"] if acc["currency"] == "643" and acc["type"] == "ACCOUNT"), None)
    assert rub_account is not None, "Рублевый счет (643, ACCOUNT) не найден"
    
    assert isinstance(rub_account["balance"], (int, float)), "Баланс должен быть числом"
    assert rub_account["balance"] > 0, f"Баланс должен быть строго больше 0, текущий: {rub_account['balance']}"

def test_03_create_payment(api_request):
    """3. Создание платежа на 1 рубль"""
    global current_payment_id
    current_payment_id = f"test-pay-{uuid.uuid4().hex}"
    
    payload = {
        "id": current_payment_id,
        "sum": {"amount": 1.00, "currency": "643"},
        "paymentMethod": {"type": "Account", "accountId": "643"},
        "fields": {"account": "79000000000"}
    }
    
    # ИСПРАВЛЕНО: используем data= вместо json=
    response = api_request.put(f"/sinap/api/v2/terms/99/payments/{current_payment_id}", data=payload)
    assert response.status in [200, 201], f"Ожидался 200 или 201, получен {response.status}"
    
    data = response.json()
    assert data["id"] == current_payment_id
    assert data["transaction"]["state"]["code"] in ["READY", "SUCCESS"]
    
def test_04_execute_payment(api_request):
    """4. Исполнение платежа (проверка статуса)"""
    global current_payment_id
    assert current_payment_id is not None, "Payment ID не был создан в предыдущем шаге"
    
    time.sleep(1.5) # Небольшая задержка для асинхронной обработки на стороне сервера
    
    response = api_request.get(f"/sinap/api/v2/terms/99/payments/{current_payment_id}")
    
    assert response.status == 200, f"Ожидался 200, получен {response.status}"
    data = response.json()
    
    assert data["transaction"]["state"]["code"] == "SUCCESS", f"Ожидался SUCCESS, получен {data['transaction']['state']['code']}"
    assert data["sum"]["amount"] == 1.00, f"Сумма искажена: {data['sum']['amount']}"
    assert data["sum"]["currency"] == "643"
