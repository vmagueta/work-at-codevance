from datetime import datetime
from decimal import Decimal


def calculate_new_amount(
    original_amount: Decimal, due_date: datetime, request_date: datetime
) -> Decimal:
    """
    Calculates the new amount to be paid through the anticipation.
    """
    DISCOUNT_RATE = Decimal(0.03)

    if isinstance(request_date, datetime):
        request_date = request_date.date()

    days_diference = (due_date - request_date).days
    discount = Decimal(
        original_amount * ((DISCOUNT_RATE / 30) * days_diference)
    )
    approved_amount = Decimal(original_amount - discount)

    return approved_amount
