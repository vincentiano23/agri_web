from django import forms
from .models import Product, ContactMessage

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product name'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product price'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product description',
                'rows': 4
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your email address'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Your message',
                'rows': 5
            }),
        }
