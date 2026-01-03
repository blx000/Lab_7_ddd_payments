from application.ports import PaymentGateway
from domain.money import Money


class FakePaymentGateway(PaymentGateway):
    def __init__(self):
        self.charges = []  # можно смотреть в тестах

    def charge(self, order_id: str, money: Money) -> str:
        self.charges.append((order_id, money.amount, money.currency))
        return f"tx-{order_id}-{money.amount}"
