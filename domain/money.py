from dataclasses import dataclass


@dataclass(frozen=True)
class Money:
    amount: int
    currency: str = "USD"

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("amount must be non-negative")
        if not self.currency:
            raise ValueError("currency is required")

    def __add__(self, other: "Money") -> "Money":
        self._ensure_same_currency(other)
        return Money(self.amount + other.amount, self.currency)

    def __mul__(self, qty: int) -> "Money":
        if qty <= 0:
            raise ValueError("qty must be positive")
        return Money(self.amount * qty, self.currency)

    def _ensure_same_currency(self, other: "Money") -> None:
        if self.currency != other.currency:
            raise ValueError("currency mismatch")
