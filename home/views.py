from django.shortcuts import render
from django.views.generic import TemplateView
from products.models import Product


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


class AboutView(TemplateView):
    """
    renders view for the about page
    """
    template_name = "home/about.html"


class PrivacyPolicyView(TemplateView):
    """
    renders view for the privacy policy page
    """
    template_name = "home/privacy_policy.html"


class ContactUsView(TemplateView):
    """
    renders view for the contact page
    """
    template_name = "home/contact.html"


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
