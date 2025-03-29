from django.db import models
from django.utils import timezone
from django.utils.timezone import now
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"
    
class PoultryInventory(models.Model):
    broilers_male = models.PositiveIntegerField(default=0)
    broilers_female = models.PositiveIntegerField(default=0)
    layers_female = models.PositiveIntegerField(default=0)
    kienyeji_male = models.PositiveIntegerField(default=0)
    kienyeji_female = models.PositiveIntegerField(default=0)
    date_updated = models.DateTimeField(default=timezone.now)

    def total_broilers(self):
        return self.broilers_male + self.broilers_female

    def total_kienyeji(self):
        return self.kienyeji_male + self.kienyeji_female

    def __str__(self):
        return f"Inventory as of {self.date_updated.date()}"
    
class Produce(models.Model):
    PRODUCE_TYPES = [
        ('Rice', 'Rice'),
        ('Maize', 'Maize'),
        ('Wheat', 'Wheat'),
        ('Beans', 'Beans'),
        ('Millet', 'Millet'),
        ('Other', 'Other'),
    ]

    produce_type = models.CharField(max_length=50, choices=PRODUCE_TYPES)
    quantity = models.PositiveIntegerField()  # Quantity in Kg
    date_recorded = models.DateTimeField(default=now)

class EggProduction(models.Model):
    total = models.IntegerField(default=0)
    eggs_raised = models.PositiveIntegerField(default=0)
    eggs_incubated = models.PositiveIntegerField(default=1)
    date_recorded = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Eggs Raised on {self.date_recorded}"

    def clean(self):
        from django.core.exceptions import ValidationError
        
        # Ensure eggs_incubated is not zero
        if self.eggs_incubated <= 0:
            raise ValidationError({'eggs_incubated': "You must incubate at least one egg."})

class DiseaseManagement(models.Model):
    DISEASE_CHOICES = [
        ('Newcastle', 'Newcastle Disease'),
        ('Coccidiosis', 'Coccidiosis'),
    ]

    disease_name = models.CharField(max_length=50, choices=DISEASE_CHOICES)
    symptoms = models.TextField()
    control_measures = models.TextField()
    date_reported = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.disease_name} reported on {self.date_reported}"
    
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"