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
