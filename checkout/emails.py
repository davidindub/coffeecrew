from django.core.mail import EmailMessage
from django.template.loader import get_template
from coffeecrew.settings import DEFAULT_FROM_EMAIL
from .models import Order


def send_confirmation_email(order):
    """
    Sends customer a confirmation email for their order.
    """
    message = get_template("checkout/email/order_confirmation_email.html"
                           ).render({
                               "order": order
                           })
    mail = EmailMessage(
        subject=f"Order Confirmation {order.order_number}",
        body=message,
        from_email=DEFAULT_FROM_EMAIL,
        to=[order.user.email],
        reply_to=[DEFAULT_FROM_EMAIL],
    )
    mail.content_subtype = "html"

    return mail.send()


def send_dispatch_email(order):
    """
    Sends customer an email that their order has been dispatched
    """
    message = get_template("checkout/email/order_dispatch_email.html"
                           ).render({
                               "order": order
                           })
    mail = EmailMessage(
        subject=f"Order Dispatched {order.order_number}",
        body=message,
        from_email=DEFAULT_FROM_EMAIL,
        to=[order.user.email],
        reply_to=[DEFAULT_FROM_EMAIL],
    )
    mail.content_subtype = "html"

    return mail.send()
