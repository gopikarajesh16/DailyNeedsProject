from django.db import models
from django.contrib.auth.models import User,auth
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Category(models.Model):
        name= models.CharField(max_length=200)
        def __str__(self):
            return self.name

class Products(models.Model):
    name = models.CharField(max_length=200)
    price = models.CharField(max_length=20, default="0.00")  # Storing price as a string
    details = models.TextField()
    image = models.ImageField(upload_to="products/")
    ctry = models.ForeignKey(Category, on_delete=models.CASCADE)
    farmer = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to user

    def __str__(self):
        return self.name



class Profile(models.Model):
    us = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=30, null=True, blank=True)  # Optional phone
    image = models.ImageField(upload_to='profilepic', null=True, blank=True)  # Optional profile pic
    address = models.TextField(blank=True, null=True)
    is_farmer = models.BooleanField(default=False)  # Default: User is a customer
    created_at = models.DateTimeField(default=timezone.now)  # Default timestamp

    def __str__(self):
        return str(self.us)




@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(us=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Customer
    product = models.ForeignKey("Products", on_delete=models.CASCADE)  # Ordered product
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    order_date = models.DateTimeField(auto_now_add=True)
    
    rating = models.IntegerField(null=True, blank=True)  # New rating field (1-5)

    def __str__(self):
        return f"Order {self.id} - {self.product.name} ({self.user.username})"

