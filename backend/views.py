from lib2to3.fixes.fix_input import context

from django.shortcuts import render
from sqlparse.utils import consume

from backend.models import Services, Blog, Gallery


# Create your views here.

def index(request):
    services = Services.objects.all()
    context = {
        "services": services
    }
    return render(request, "backend/home.html", context)


def contact(request):
    return render(request, "backend/contactUs.html")


def blog(request):
    blogs = Blog.objects.all()
    context = {
        "blogs": blogs
    }

    return render(request, "backend/blogs.html", context)


def gallery(request):
    galleries = Gallery.objects.all()  # Fetch all gallery images
    context = {
        'galleries': galleries
    }
    return render(request, "backend/gallery.html", context)
