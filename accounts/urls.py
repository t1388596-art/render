from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.custom_login_view, name='login'),
    path('signup/', views.custom_signup_view, name='signup'),
    path('profile/', views.profile_view, name='profile'),
]