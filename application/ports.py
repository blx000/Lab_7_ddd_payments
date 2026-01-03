from abc import ABC, abstractmethod
from typing import Optional

from domain.money import Money
from domain.order import Order


class OrderRepository(ABC):
    @abstractmethod
    def get_by_id(self, order_id: str) -> Optional[Order]:
        raise NotImplementedError

    @abstractmethod
    def save(self, order: Order) -> None:
        raise NotImplementedError


class PaymentGateway(ABC):
    @abstractmethod
    def charge(self, order_id: str, money: Money) -> str:
        """Возвращает идентификатор транзакции."""
        raise NotImplementedError
