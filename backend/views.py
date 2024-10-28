from tempfile import template

from django.shortcuts import render
from django.template.defaultfilters import title
from sqlparse.utils import consume

from backend.models import Services, Blog, Gallery

# Create your views here.

services = Services.objects.first()
context = {
    "services": services
}


def index(request):
    # params =  request.build_absolute_uri()
    return render(request, "backend/home.html", context)


def contact(request):
    return render(request, "backend/contactUs.html", context)


def blog(request):
    blogs = Blog.objects.all()
    context.update({
        "blogs": blogs
    })

    return render(request, "backend/blogs.html", context)


def gallery(request):
    galleries = Gallery.objects.all()  # Fetch all gallery images
    context.update({
        'galleries': galleries
    })

    return render(request, "backend/gallery.html", context)
