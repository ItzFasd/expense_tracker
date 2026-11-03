from dataclasses import dataclass

KIND_EXPENSE = "expense"
KIND_INCOME = "income"


@dataclass(frozen=True)
class Category:
    id: int
    name: str
    kind: str


@dataclass(frozen=True)
class Transaction:
    id: int
    amount_cents: int
    category_id: int
    date: str
    comment: str


@dataclass(frozen=True)
class TransactionRow:
    id: int
    amount_cents: int
    category_name: str
    kind: str
    date: str
    comment: str


@dataclass(frozen=True)
class MonthSummary:
    total_income: int
    total_expense: int
    by_category: dict[str, int]

    @property
    def balance(self) -> int:
        return self.total_income - self.total_expense
