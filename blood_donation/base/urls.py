from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('add_donor', register_donor, name='register_donor'),
    path('search_donor', search_donors, name = 'search_donors'),
    path('register', user_register, name = 'user_register'),
    path('login', user_login, name='user_login'),
    path('logout', user_logout, name='logout'),
    path('send_email/', send_message_twilio, name='send_email'),
]
