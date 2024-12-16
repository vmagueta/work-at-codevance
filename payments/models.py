from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models

from .utils import calculate_new_amount


class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=14, unique=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.name} - {self.cnpj}"


class Payment(models.Model):
    vendor = models.ForeignKey(
        Vendor, related_name="payments", on_delete=models.CASCADE
    )
    issue_date = models.DateField()
    due_date = models.DateField()
    original_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for {self.vendor.name} - ${self.original_amount} on {self.due_date}"

    def is_antecipation_available(self, request_date):
        """
        Checks if the anticipation can be requested.
        """
        return request_date < self.due_date


class Antecipation(models.Model):
    NOT_REQUESTED = "not_requested"
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    IN_PROGRESS = "in_progress"

    STATUS_CHOICES = [
        (NOT_REQUESTED, "Not Requested"),
        (PENDING, "Pending"),
        (APPROVED, "Approved"),
        (REJECTED, "Rejected"),
        (IN_PROGRESS, "In Progress"),
    ]

    payment = models.ForeignKey(
        Payment, related_name="antecipation", on_delete=models.CASCADE
    )
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=NOT_REQUESTED
    )
    new_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    def save(self, *args, **kwargs):
        """
        Overrides the save method to automatically calculate the anticipation amount
        if the request is 'PENDING'.
        """
        if self.status == self.PENDING and not self.new_amount:
            self.new_amount = calculate_new_amount(
                self.payment.original_amount,
                self.payment.due_date,
                self.request_date,
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Anticipation for Payment {self.payment.id} - Status: {self.status}"
