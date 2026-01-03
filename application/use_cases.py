from dataclasses import dataclass

from application.ports import OrderRepository, PaymentGateway


@dataclass(frozen=True)
class PaymentResult:
    order_id: str
    transaction_id: str
    total_amount: int
    currency: str


class PayOrderUseCase:
    def __init__(self, repo: OrderRepository, gateway: PaymentGateway):
        self.repo = repo
        self.gateway = gateway

    def execute(self, order_id: str) -> PaymentResult:
        order = self.repo.get_by_id(order_id)
        if order is None:
            raise ValueError("order not found")

        total_money = order.pay()              # доменная операция (проверяет инварианты)
        tx_id = self.gateway.charge(order_id, total_money)  # внешний платёж
        self.repo.save(order)                  # сохраняем новое состояние

        return PaymentResult(
            order_id=order.order_id,
            transaction_id=tx_id,
            total_amount=total_money.amount,
            currency=total_money.currency,
        )
