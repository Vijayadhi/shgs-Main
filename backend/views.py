from lib2to3.fixes.fix_input import context

from django.shortcuts import render
from sqlparse.utils import consume

from backend.models import Services, Blog


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