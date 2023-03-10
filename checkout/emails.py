from django.core.mail import EmailMessage
from django.template.loader import get_template
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
        from_email="coffeecrewshop@gmail.com",
        to=[order.user.email],
        reply_to=["coffeecrewshop@gmail.com"],
    )
    mail.content_subtype = "html"
    return mail.send()
