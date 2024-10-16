from django.urls import path

from backend import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contactUs/', views.contact, name='contact'),
    path('blogs/', views.blog, name='blog'),
]