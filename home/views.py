from django.shortcuts import render


def index(request):
    """
    renders view for the homepage
    """
    return render(request, "home/index.html")


def about(request):
    """
    renders view for the about page
    """
    return render(request, "home/about.html")


def privacy_policy(request):
    """
    renders view for the privacy policy page
    """
    return render(request, "home/privacy_policy.html")


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
