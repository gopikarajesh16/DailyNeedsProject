from django.contrib import admin
from .models import Products,Category,Profile

admin.site.register (Products)
admin.site.register (Profile)
admin.site.register (Category)

from .models import Order  # Import the Order model

# Register the Order model in admin
admin.site.register(Order)