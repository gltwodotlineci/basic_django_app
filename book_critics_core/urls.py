from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('signup/', views.signup, name='signup'),
    path('inscription/', views.inscirption, name='inscription'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/<uuid:user_id>', views.show_profile, name='profile'),
]
