from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from payments.models import Payment


@shared_task
def send_payment_email(payment_id, action):
    try:
        payment = Payment.objects.get(id=payment_id)

        subject = f"Payment {action}"
        message = f"The payment {payment_id} was {action}."
        recipient = payment.vendor.user.email

        html_message = """\
        <html>
            <body>
                <h2>Payment {{ payment.id }} {{ action }}</h2>
                <p>The payment {{ payment.id }} was {{ action }} sucefully.</p>
            </body>
        </html>
        """
        plain_message = strip_tags(html_message)

        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient],
            html_message=html_message,
        )
        return f"E-mail for {action} sent succefully."
    except Payment.DoesNotExist:
        return f"Payment {payment_id} not found!"
