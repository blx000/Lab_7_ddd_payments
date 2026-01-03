from dataclasses import dataclass
from enum import Enum
from typing import List

from domain.money import Money


class OrderStatus(str, Enum):
    DRAFT = "DRAFT"
    PAID = "PAID"


@dataclass(frozen=True)
class OrderLine:
    sku: str
    price: Money
    qty: int

    def __post_init__(self):
        if not self.sku:
            raise ValueError("sku is required")
        if self.qty <= 0:
            raise ValueError("qty must be positive")


class Order:
    def __init__(self, order_id: str, currency: str = "USD"):
        if not order_id:
            raise ValueError("order_id is required")
        self.order_id = order_id
        self.currency = currency
        self._status = OrderStatus.DRAFT
        self._lines: List[OrderLine] = []

    @property
    def status(self) -> OrderStatus:
        return self._status

    @property
    def lines(self) -> List[OrderLine]:
        # отдаём копию, чтобы нельзя было менять список снаружи
        return list(self._lines)

    def add_line(self, line: OrderLine) -> None:
        self._ensure_not_paid()
        if line.price.currency != self.currency:
            raise ValueError("line currency must match order currency")
        self._lines.append(line)

    def total(self) -> Money:
        total = Money(0, self.currency)
        for line in self._lines:
            total = total + (line.price * line.qty)
        return total

    def pay(self) -> Money:
        # Инвариант: нельзя оплатить пустой заказ
        if len(self._lines) == 0:
            raise ValueError("cannot pay empty order")
        # Инвариант: нельзя оплатить повторно
        if self._status == OrderStatus.PAID:
            raise ValueError("order already paid")
        self._status = OrderStatus.PAID
        return self.total()

    def _ensure_not_paid(self) -> None:
        # Инвариант: после оплаты нельзя менять строки
        if self._status == OrderStatus.PAID:
            raise ValueError("cannot modify paid order")
