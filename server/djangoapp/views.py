from django.shortcuts import render, get_object_or_404, redirect
from .models import CarMake, CarModel
from .restapis import get_request, analyze_review_sentiments, post_review
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

#Update the `get_dealerships` render list of dealerships all by default, particular state if state is passed
def get_dealerships(request, state="All"):
    if(state == "All"):
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/"+state

    print(f"Fetching data from: {endpoint}")
    dealerships = get_request(endpoint)
    
    print(f"Dealerships received: {dealerships}")  
    return JsonResponse({"status":200,"dealers":dealerships})

def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = "/fetchReviews/dealer/" + str(dealer_id)
        reviews = get_request(endpoint)
        # reviews = [
        #     {"review": "Great experience, highly recommend!"},
        #     {"review": "Terrible service, would not return."},
        # ]

        print(f"TEST API Response for dealer {dealer_id}: {reviews}")  # Debugging print

        if reviews is None:  # API request failed
            return JsonResponse({"status": 500, "message": "Failed to fetch reviews"})

        if not reviews:  # Empty list (no reviews found)
            return JsonResponse({"status": 200, "reviews": [], "message": "No reviews available for this dealer."})

        valid_reviews = []
        for review_detail in reviews:
            if isinstance(review_detail, dict):  # Ensure it's a dictionary
                print(f"Processing review: {review_detail.get('review', '')}")  # Debugging print
                response = analyze_review_sentiments(review_detail.get('review', ''))
                print(f"Sentiment response: {response}")  # Debugging print

                # Check if response is not None before accessing it
                if response is not None:
                    review_detail['sentiment'] = response.get('sentiment', 'unknown')
                else:
                    review_detail['sentiment'] = 'unknown'  # Set a default value if the response is None
                
                valid_reviews.append(review_detail)

        return JsonResponse({"status": 200, "reviews": valid_reviews})

    return JsonResponse({"status": 400, "message": "Bad Request"})

def get_dealer_details(request, dealer_id):
    if(dealer_id):
        endpoint = "/fetchDealer/" + str(dealer_id)
        dealership = get_request(endpoint)

        print(f"API Response for dealer {dealer_id}: {dealership}")  # Log the response

        if not dealership:  # Handle case when no data is returned
            return JsonResponse({"status": 404, "message": "Dealer not found"})
        
        return JsonResponse({"status": 200, "dealer": dealership})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})

def add_review(request):
    if(request.user.is_anonymous == False):
        data = json.loads(request.body)
        try:
            response = post_review(data)
            return JsonResponse({"status":200})
        except:
            return JsonResponse({"status":401,"message":"Error in posting review"})
    else:
        return JsonResponse({"status":403,"message":"Unauthorized"})