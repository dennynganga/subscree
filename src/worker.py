from celery import Celery

from src.settings import settings

celery_app = Celery(broker=settings.celery_broker)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(settings.due_bills_checker_frequency)


@celery_app.task
def check_due_bills():
    """
    Checks for bills that are due today
    """
    # query subscriptions to see which have a next_charge_date as today
