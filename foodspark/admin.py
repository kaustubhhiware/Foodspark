from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(Customer)
admin.site.register(Restaurant)
admin.site.register(FoodItem)
admin.site.register(Order)
admin.site.register(Cart)
