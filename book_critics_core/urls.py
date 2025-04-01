from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('signup/', views.signup, name='signup'),
    path('inscription/', views.inscirption, name='inscription'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.show_profile, name='profile'),
    # Tickets
    path('ticket/', views.ticket, name='ticket'),
    path('create_ticket/', views.create_ticket, name='create_ticket'),
    path('tickets/', views.all_tickets, name='tickets'),
    # Reviews
    path('create_review/', views.create_review, name='create_review'),
]
