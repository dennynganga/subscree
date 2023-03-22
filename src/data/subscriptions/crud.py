import math
from datetime import datetime

from sqlalchemy.orm import Session

from src.data.subscriptions.db import SubscriptionDAO


def get_current_batch(session: Session):
    today = datetime.utcnow().today()
    current_hour = today.hour
    hours_left = 24 - current_hour
    total_bills = session.query(SubscriptionDAO).filter(SubscriptionDAO.next_charge_date == today.date())
    current_batch_count = math.ceil(total_bills.count() / hours_left)
    return total_bills.limit(current_batch_count).all()


def get_product_subscriptions(session: Session):
    pass
