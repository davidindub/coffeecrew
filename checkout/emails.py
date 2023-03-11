from django.core.mail import EmailMessage
from django.template.loader import get_template
from .models import Order


def send_confirmation_email(order):
    """
    Sends customer a confirmation email for their order.
    """
    print("send_confirmation_email() called")
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
    print("📧 confirmation email sent 📧")

    return mail.send()


def send_dispatch_email(order):
    """
    Sends customer an email that their order has been dispatched
    """
    print("send_dispatch_email() called")
    message = get_template("checkout/email/order_dispatched_email.html"
                           ).render({
                               "order": order
                           })
    mail = EmailMessage(
        subject=f"Order Dispatched {order.order_number}",
        body=message,
        from_email="coffeecrewshop@gmail.com",
        to=[order.user.email],
        reply_to=["coffeecrewshop@gmail.com"],
    )
    mail.content_subtype = "html"
    print("📧 dispatch email sent 📧")

    return mail.send()
