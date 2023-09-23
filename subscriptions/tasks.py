from celery import shared_task

from subscriptions.models import Subscriptions
from subscriptions.services import retrieve_session


@shared_task
def task_retrieve_session():
    """Задание обработка сеанс оплаты"""
    subscriptions = Subscriptions.objects.filter(pay_status='open')
    for subscription in subscriptions:
        subscription_session = retrieve_session(subscription.session_id)
        if subscription_session['status'] == 'complete':
            subscription.payment_status = subscription_session['payment_status']
            subscription.pay_status = subscription_session['status']
            subscription.post.count_pay = subscription.post.count_pay + 1
            subscription.post.save()
            subscription.save()
