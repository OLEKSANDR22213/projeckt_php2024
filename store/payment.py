from typing import Dict
from .models import Order

class PaymentProcessor:
    def __init__(self):
        self.payments: Dict[int, bool] = {}

    def process_payment(self, order: Order) -> bool:
        success = True
        self.payments[order.id] = success
        return success 