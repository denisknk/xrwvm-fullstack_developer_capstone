from django.shortcuts import render, get_object_or_404, redirect
from .models import CarMake, CarModel
from .populate import initiate
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from datetime import datetime
import logging
import json
from django.views.decorators.csrf import csrf_exempt

def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)
    if(count == 0):
        print("Database is empty. Running initiate() to populate data.")
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
    return JsonResponse({"CarModels":cars})

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.

# Create a `login_user` view to handle sign-in request
@csrf_exempt
def login_user(request):
    if request.method == "POST":
        try:
            # Parse JSON request body
            data = json.loads(request.body)
            username = data.get('userName')
            password = data.get('password')

            # Authenticate user
            user = authenticate(username=username, password=password)
            if user is not None:
                # Log the user in
                login(request, user)
                response_data = {"userName": username, "status": "Authenticated"}
            else:
                response_data = {"userName": username, "status": "Failed: Invalid credentials"}

        except json.JSONDecodeError:
            response_data = {"status": "Failed: Invalid JSON format"}
    else:
        response_data = {"status": "Failed: Only POST requests are allowed"}

    return JsonResponse(response_data)

# Create a `logout_user` view to handle sign-out request
@csrf_exempt
def logout_user(request):
    if request.method == "POST":
        username = request.user.username if request.user.is_authenticated else ""
        logout(request)
        return JsonResponse({"userName": username, "status": "Logged out successfully"})
    return JsonResponse({"status": "Failed: Only POST requests are allowed"})

# Create a `registration` view to handle sign-up request
@csrf_exempt
def registration(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get('userName')
            password = data.get('password')
            first_name = data.get('firstName', '')
            last_name = data.get('lastName', '')
            email = data.get('email', '')

            # Check if username already exists
            if User.objects.filter(username=username).exists():
                return JsonResponse({"userName": username, "error": "Already Registered"})

            # Create a new user
            user = User.objects.create_user(
                username=username, 
                first_name=first_name, 
                last_name=last_name, 
                password=password, 
                email=email
            )

            # Log the user in
            login(request, user)

            return JsonResponse({"userName": username, "status": "Authenticated"})

        except json.JSONDecodeError:
            return JsonResponse({"status": "Failed: Invalid JSON format"})

    return JsonResponse({"status": "Failed: Only POST requests are allowed"})

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    return JsonResponse({"status": "Dealerships endpoint not implemented yet"})

# Create a `get_dealer_reviews` view to render the reviews of a dealer
def get_dealer_reviews(request, dealer_id):
    return JsonResponse({"status": f"Reviews for dealer {dealer_id} not implemented yet"})

# Create a `get_dealer_details` view to render the dealer details
def get_dealer_details(request, dealer_id):
    return JsonResponse({"status": f"Dealer details for {dealer_id} not implemented yet"})

# Create an `add_review` view to submit a review
def add_review(request):
    return JsonResponse({"status": "Add review endpoint not implemented yet"})