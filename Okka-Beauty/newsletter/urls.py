# urls.py
from django.urls import path
from newsletter import views
from .views import *

urlpatterns = [
    path('newsletter/', views.newsletter, name='newsletter'),
]
