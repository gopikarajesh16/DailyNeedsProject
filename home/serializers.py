from rest_framework import serializers
from .models import Category,Products  # Ensure Category is defined in models.py

class Categoryserializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class Productsserializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['name', 'price','details', 'image']