from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('fetch/', views.fetch_balance, name='fetch_balance'),
]
