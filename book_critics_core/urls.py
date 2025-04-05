from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('signup/', views.signup, name='signup'),
    path('inscription/', views.inscription, name='inscription'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.show_profile, name='profile'),
    path('other_profile/<uuid:user_id>/', views.other_profile, name='other_profile'),
    path('all_users/', views.all_users, name='all_users'),
    # Following process
    path('follow_user/', views.follow_user, name='follow_user'),
    path('unfollow_user/', views.unfollow_user, name='unfollow_user'),
    # Tickets
    path('ticket/', views.ticket, name='ticket'),
    path('create_ticket/', views.create_ticket, name='create_ticket'),
    path('tickets/', views.all_tickets, name='tickets'),
    path('my_tickets/', views.my_tickets, name='my_tickets'),
    # Reviews
    path('create_review/', views.create_review, name='create_review'),
]
