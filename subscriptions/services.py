import requests
from requests import Response

from config.settings import STRIPE_API_KEY


def create_session(success_url, currency='usd'):
    """Создать сеанс оплаты"""
    images = 'https://files.stripe.com/links/MDB8YWNjdF8xTlhkR2FCT0xUUTBGcWN4fGZsX3Rlc3RfZ3cyendIMmxraFJHQTc2RHNkS1VGS1cy00KnnMohGD'
    headers = {'Authorization': f'Bearer {STRIPE_API_KEY}'}
    data = {
        'mode': 'payment',
        'success_url': 'http://192.168.88.239:8000/posts',
        'line_items[0][price_data][currency]': 'rub',
        'line_items[0][price_data][product_data][name]': 'test',
        'line_items[0][price_data][product_data][images][0]': images,
        'line_items[0][price_data][unit_amount]': 10000,
        'line_items[0][quantity]': 1
    }
    response = requests.post('https://api.stripe.com/v1/checkout/sessions', headers=headers, data=data)
    return response.json()


def retrieve_session(session_id):
    """Детали сеанса оплаты"""
    headers = {'Authorization': f'Bearer {STRIPE_API_KEY}'}
    response = requests.get(f'https://api.stripe.com/v1/checkout/sessions/{session_id}', headers=headers)
    return response.json()


def expire_session(session_id):
    """Завершить сеанс оплаты"""
    headers = {'Authorization': f'Bearer {STRIPE_API_KEY}'}
    response = requests.post(f'https://api.stripe.com/v1/checkout/sessions/{session_id}/expire', headers=headers)
    return response.json()
