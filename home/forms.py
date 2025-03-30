from django import forms

from.models import Products

class ProductsForm(forms.ModelForm):
    class Meta:
        model=Products
        fields='__all__'


from .models import Profile

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'image', 'address'] 























