from django.shortcuts import render


def index(request):
    """
    renders view for the homepage
    """
    return render(request, "home/index.html")
