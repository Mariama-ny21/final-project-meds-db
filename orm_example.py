# Example Django ORM Usage

# models.py
from django.db import models

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    manufacturer = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

# views.py (example snippets)
from .models import Medicine

# Create a new medicine
med = Medicine.objects.create(name="Aspirin", price=2.99, manufacturer="Pfizer")

# Query all medicines
all_meds = Medicine.objects.all()

# Filter medicines by manufacturer
pfizer_meds = Medicine.objects.filter(manufacturer="Pfizer")

# Update a medicine
med = Medicine.objects.get(pk=1)
med.price = 3.49
med.save()

# Delete a medicine
med.delete()

# Use in a view (example)
from django.shortcuts import render

def medicine_list(request):
    medicines = Medicine.objects.all()
    return render(request, 'medicine_list.html', {'medicines': medicines})
