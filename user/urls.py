from django.urls import path
from . import views


app_name = 'user'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('home/', views.user_home, name='home'),
    path('priest-dashboard/', views.priest_dashboard, name='priest-dashboard'),
    path('priest-profile/', views.priest_profile, name='priest-profile'),
    path('nav/', views.navbar, name='nav'),

]
