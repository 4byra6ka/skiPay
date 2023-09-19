import requests
from requests import Response

from config.settings import STRIPE_API_KEY


def create_session(amount, currency='usd'):
    headers = {'Authorization': f'Bearer {STRIPE_API_KEY}'}
    params = {'amount': amount, 'currency': currency}
    response = requests.post('https://api.stripe.com/v1/payment_intents', headers=headers, params=params)
    data = response.json()
    return data['id']

def retrieve_session(amount, currency='usd'):
    headers = {'Authorization': f'Bearer {STRIPE_API_KEY}'}
    params = {'amount': amount, 'currency': currency}
    response = requests.post('https://api.stripe.com/v1/payment_intents', headers=headers, params=params)
    data = response.json()
    return data['id']

def retrieve_payment_intent(id):
    headers = {'Authorization': f'Bearer {STRIPE_API_KEY}'}
    response = requests.get(f'https://api.stripe.com/v1/payment_intents/{id}', headers=headers)
    # data = response.json()
    # # Обработка полученных данных
    return response.json()