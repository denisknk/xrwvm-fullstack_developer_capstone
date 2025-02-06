from django.contrib import admin
from .models import CarMake, CarModel

# Register CarMake model


@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  # Show fields in admin panel
    search_fields = ('name',)  # Enable search by name

# Register CarModel model


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'car_make', 'dealer_id', 'type',
                    'year')  # Show fields in admin panel
    list_filter = ('car_make', 'type', 'year')  # Enable filtering
    # Enable search by model or make
    search_fields = ('name', 'car_make__name')
