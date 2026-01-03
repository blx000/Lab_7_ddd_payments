import pytest

from application.use_cases import PayOrderUseCase
from domain.money import Money
from domain.order import Order, OrderLine, OrderStatus
from infrastructure.fake_gateway import FakePaymentGateway
from infrastructure.in_memory_repo import InMemoryOrderRepository


def make_repo_with_order(order: Order) -> InMemoryOrderRepository:
    repo = InMemoryOrderRepository()
    repo.add(order)
    return repo


def test_successful_payment():
    order = Order("o-1", currency="USD")
    order.add_line(OrderLine("SKU1", Money(50, "USD"), 2))  # 100

    repo = make_repo_with_order(order)
    gw = FakePaymentGateway()
    uc = PayOrderUseCase(repo, gw)

    result = uc.execute("o-1")

    assert result.total_amount == 100
    assert result.currency == "USD"
    assert result.transaction_id.startswith("tx-o-1-100")

    saved = repo.get_by_id("o-1")
    assert saved.status == OrderStatus.PAID
    assert gw.charges == [("o-1", 100, "USD")]


def test_error_on_empty_order_payment():
    order = Order("o-empty", currency="USD")

    repo = make_repo_with_order(order)
    gw = FakePaymentGateway()
    uc = PayOrderUseCase(repo, gw)

    with pytest.raises(ValueError, match="cannot pay empty order"):
        uc.execute("o-empty")


def test_error_on_double_payment():
    order = Order("o-2", currency="USD")
    order.add_line(OrderLine("SKU1", Money(10, "USD"), 1))

    repo = make_repo_with_order(order)
    gw = FakePaymentGateway()
    uc = PayOrderUseCase(repo, gw)

    uc.execute("o-2")
    with pytest.raises(ValueError, match="order already paid"):
        uc.execute("o-2")


def test_cannot_modify_after_payment():
    order = Order("o-3", currency="USD")
    order.add_line(OrderLine("SKU1", Money(10, "USD"), 1))

    repo = make_repo_with_order(order)
    gw = FakePaymentGateway()
    uc = PayOrderUseCase(repo, gw)

    uc.execute("o-3")

    with pytest.raises(ValueError, match="cannot modify paid order"):
        order.add_line(OrderLine("SKU2", Money(5, "USD"), 1))


def test_total_is_sum_of_lines():
    order = Order("o-4", currency="USD")
    order.add_line(OrderLine("A", Money(20, "USD"), 3))  # 60
    order.add_line(OrderLine("B", Money(15, "USD"), 2))  # 30

    assert order.total().amount == 90
