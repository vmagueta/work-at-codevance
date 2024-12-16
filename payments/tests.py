from datetime import datetime
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase

from payments.models import Antecipation, Payment, Vendor

from .utils import calculate_new_amount


class PaymentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create()
        self.vendor = Vendor.objects.create(
            user=self.user,
            name="Vendor",
            email="vendor@test.com",
            cnpj="12345678000190",
        )
        self.payment = Payment.objects.create(
            vendor=self.vendor,
            issue_date=datetime(2024, 12, 15).date(),
            due_date=datetime(2024, 12, 31).date(),
            original_amount=Decimal(200.00),
        )
        self.antecipation = Antecipation.objects.create(
            payment_id=self.payment.id
        )

    def test_positive_payment_creation(self):
        """A positive test for a payment creation"""
        self.assertEqual(self.payment.original_amount, Decimal(200.00))

    def test_positive_payment_status(self):
        """A positive test for a payment status in antecipation"""
        self.assertTrue(self.antecipation.status == "not_requested")

    def test_positive_calculate_new_amount(self):
        """A positive test for calculating a new amount for the vendor"""
        new_amount = calculate_new_amount(
            self.payment.original_amount,
            self.payment.due_date,
            request_date=datetime.now(),
        )
        new_amount = round(new_amount, 2)
        self.assertAlmostEqual(new_amount, Decimal(196.80))
