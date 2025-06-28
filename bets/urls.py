from django.urls import path, include
from . import views

app_name = 'bets'

urlpatterns = [
    path('', views.home, name='home_bets'),
    path('admin/', views.admin_users, name='admin_users'),
    path('proc_acceso/<str:profile_id>/', views.proc_acceso, name='proc_acceso'),
    path('chng_admin/<str:profile_id>', views.chng_admin, name='chng_admin'),
    path('admin/user/delete/<int:profile_id>', views.delete_user, name='delete_user'),
]
