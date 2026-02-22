# models.py (Same as before - no changes needed)
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum

class TransactionType(Enum):
    EXPENSE = "expense"
    INCOME = "income"

class UdharStatus(Enum):
    PENDING = "pending"
    PARTIAL = "partial"
    CLEARED = "cleared"

@dataclass
class Expense:
    id: Optional[int]
    amount: float
    category: str
    description: str
    date: str
    transaction_type: TransactionType
    
    def to_tuple(self):
        return (self.amount, self.category, self.description, 
                self.date, self.transaction_type.value)

@dataclass
class Udhar:
    id: Optional[int]
    person_name: str
    amount: float
    description: str
    date_given: str
    due_date: Optional[str]
    status: UdharStatus
    amount_paid: float = 0.0
    
    @property
    def remaining_amount(self):
        return self.amount - self.amount_paid
    
    def to_tuple(self):
        return (self.person_name, self.amount, self.description,
                self.date_given, self.due_date, self.status.value, self.amount_paid)