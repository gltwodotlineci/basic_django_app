from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('signup/', views.signup, name='signup'),
    path('inscription/', views.inscription, name='inscription'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.show_profile, name='profile'),
    path('other_prof/<uuid:user_id>/', views.other_profile, name='other'),
    path('users/', views.all_users, name='all_users'),
    path('search_usr/', views.search_user, name='search_usr'),
    # Following process
    path('follow_user/', views.follow_user, name='follow_user'),
    path('unfollow_user/', views.unfollow_user, name='unfollow_user'),
    # Tickets
    path('ticket/', views.ticket, name='ticket'),
    path('create_ticket/', views.create_ticket, name='create_ticket'),
    path('flux/', views.flux, name='flux'),
    path('my_tickets/<uuid:user_id>/', views.my_tickets, name='my_tickets'),
    path('update_tc/', views.update_tck, name='update_tc'),
    path('delete_ticket/', views.delete_ticket, name='delete_ticket'),
    # Reviews
    path('create_review/', views.create_review, name='create_review'),
    path('update_review/', views.update_review, name='update_review'),
    path('delete_review/', views.delete_review, name='delete_review'),
    # Ticket & Review
    path('ticket_and_review/', views.ticket_and_review, name='ticketreview'),
    path('createticketreview/', views.create_tck_rvw, name='create-tck-rvw'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
