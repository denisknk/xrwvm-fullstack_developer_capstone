from django.urls import path
from . import views  # Import views from djangoapp

app_name = 'djangoapp'  # Namespace for this app

urlpatterns = [
    path('login/', views.login_user, name='login'),  # API for user login
    path('get_cars/', view=views.get_cars, name ='getcars'),
    path('register/', views.registration, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path(route='get_dealers', view=views.get_dealerships, name='get_dealers'),
    path(route='get_dealers/<str:state>', view=views.get_dealerships, name='get_dealers_by_state'),
    path(route='dealer/<int:dealer_id>', view=views.get_dealer_details, name='dealer_details'),
    path(route='reviews/dealer/<int:dealer_id>', view=views.get_dealer_reviews, name='dealer_details'),
    path(route='add_review', view=views.add_review, name='add_review'),
]