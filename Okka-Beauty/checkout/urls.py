# urls.py
from django.urls import path
from checkout import views
from .views import *

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('order', views.order, name='order'),
]
