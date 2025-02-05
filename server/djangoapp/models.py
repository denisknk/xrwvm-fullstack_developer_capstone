from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Car Make Model
class CarMake(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Car Make Name
    description = models.TextField(blank=True, null=True)  # Optional Description

    def __str__(self):
        return self.name  # Returns car make name as string representation


# Car Model Model
class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name="models")  # Many-to-One Relationship
    dealer_id = models.IntegerField(null=True, blank=True)  # Refers to dealer created in Cloudant database
    name = models.CharField(max_length=100)  # Car Model Name

    # Car Type Choices
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        ('TRUCK', 'Truck'),
        ('COUPE', 'Coupe'),
        ('HATCHBACK', 'Hatchback'),
    ]
    type = models.CharField(max_length=10, choices=CAR_TYPES, default='SUV')

    # Car Year with validation (2015 - 2023)
    year = models.IntegerField(
        validators=[
            MaxValueValidator(2023),
            MinValueValidator(2015)
        ]
    )

    def __str__(self):
        return f"{self.car_make.name} {self.name} ({self.year})"  # Prints Car Make & Model