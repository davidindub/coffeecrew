from django.shortcuts import render
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.views.generic import TemplateView, FormView
from coffeecrew.settings import DEFAULT_FROM_EMAIL
from products.models import Product
from .forms import ContactForm


class IndexView(TemplateView):
    """
    renders view for the homepage
    """
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["latest_products"] = Product.objects.order_by(
            "-date_added")[:3]
        return context


class NewsletterView(TemplateView):
    """
    renders view for the newsletter page
    """
    template_name = "home/newsletter.html"


class PrivacyPolicyView(TemplateView):
    """
    renders view for the privacy policy page
    """
    template_name = "home/privacy_policy.html"


class ContactUsView(FormView):
    """
    Renders view for the contact page

    Pre-populate the name and email field if the user is logged in.
    """
    template_name = "home/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("contact_submit")

    def form_valid(self, form):
        name = form.cleaned_data["full_name"]
        email = form.cleaned_data["email"]
        message = form.cleaned_data["message"]

        subject = "Contact Us Form Submission"
        message = f"Name: {name}\nEmail: {email}\n\n{message}"
        sender_email = DEFAULT_FROM_EMAIL
        recipient_email = [DEFAULT_FROM_EMAIL]
        send_mail(subject, message, sender_email, recipient_email)
        return super().form_valid(form)

    def get_initial(self):
        user = self.request.user
        if user.is_anonymous:
            return {
            }
        if user.id:
            return {
                "full_name": user.get_full_name(),
                "email": user.email,
            }


class ContactUsSuccessView(TemplateView):
    """
    View for successful contact us form submission
    """
    template_name = "home/contact_us_success.html"


def handler403(request, exception):
    """
    View for 403 Error Page
    """
    return render(request, "errors/403.html", status=403)


def handler404(request, exception):
    """
    View for 404 Error Page
    """
    return render(request, "errors/404.html", status=404)


def handler500(request):
    """
    View for 500 Error Page
    """
    return render(request, "errors/500.html", status=500)
