# urls.py
from django.urls import path
from contact import views
from .views import *

urlpatterns = [
    path('contact-us/', views.contact, name='contacts'),
]
