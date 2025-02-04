from django.urls import path
from . import views  # Import views from djangoapp

app_name = 'djangoapp'  # Namespace for this app

urlpatterns = [
    path('login/', views.login_user, name='login'),  # API for user login
    path('register/', views.registration, name='register'),
    path('logout/', views.logout_user, name='logout'),
]