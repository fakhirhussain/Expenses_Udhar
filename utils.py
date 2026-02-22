# utils.py (Enhanced for mobile)
from datetime import datetime, timedelta
from typing import List, Tuple

def format_currency(amount: float) -> str:
    """Format amount in Indian Rupee style"""
    return f"₹{amount:,.2f}"

def format_currency_compact(amount: float) -> str:
    """Compact format for mobile screens"""
    if amount >= 100000:
        return f"₹{amount/100000:.1f}L"
    elif amount >= 1000:
        return f"₹{amount/1000:.1f}K"
    return f"₹{amount:.0f}"

def get_current_date() -> str:
    return datetime.now().strftime("%Y-%m-%d")

def get_current_month() -> str:
    return datetime.now().strftime("%Y-%m")

def get_month_options() -> List[str]:
    """Return list of last 12 months for selection"""
    months = []
    today = datetime.now()
    for i in range(12):
        date = today - timedelta(days=30*i)
        months.append(date.strftime("%Y-%m"))
    return months

def validate_amount(amount_str: str) -> Tuple[bool, float]:
    """Validate and convert amount string to float"""
    try:
        amount = float(amount_str)
        if amount <= 0:
            return False, 0
        return True, amount
    except ValueError:
        return False, 0

def get_category_suggestions() -> List[str]:
    """Common expense categories"""
    return [
        "Food", "Transport", "Shopping", "Entertainment",
        "Bills", "Health", "Education", "Rent",
        "Groceries", "Personal", "Gifts", "Investment",
        "Salary", "Freelance", "Other"
    ]

def get_status_color(status: str) -> tuple:
    """Return RGB color for status"""
    colors = {
        'pending': (0.9, 0.2, 0.2, 1),    # Red
        'partial': (0.9, 0.6, 0.1, 1),    # Orange
        'cleared': (0.2, 0.7, 0.2, 1),    # Green
        'expense': (0.9, 0.2, 0.2, 1),    # Red
        'income': (0.2, 0.7, 0.2, 1),     # Green
    }
    return colors.get(status, (0.5, 0.5, 0.5, 1))