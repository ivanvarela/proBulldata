from django.urls import path, include
from . import views

app_name = 'bets'

urlpatterns = [
    path('', views.home, name='home_bets'),
]
