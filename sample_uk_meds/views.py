
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect, render


# Custom UserCreationForm to remove username help text
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields
        help_texts = {
            'username': '',  # Remove or customize help text here
        }

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'sample_uk_meds/register.html', {'form': form})
from django.shortcuts import render, get_object_or_404
from .models import Medicine
from django.db import models

# Create your views here.

def home(request):
    return render(request, 'sample_uk_meds/home.html')


def medicine_list(request):
    query = request.GET.get('q', '')
    sort = request.GET.get('sort', 'name')
    order = request.GET.get('order', 'asc')
    rating_filter = request.GET.get('rating', '')

    medicines = Medicine.objects.all()
    if query:
        medicines = medicines.filter(
            models.Q(medicine_name__icontains=query) |
            models.Q(formula__icontains=query)
        )
    if rating_filter:
        try:
            rating_val = float(rating_filter)
            medicines = medicines.filter(rating__gte=rating_val)
        except ValueError:
            pass
    # Sorting
    if sort == 'price':
        sort_field = 'price' if order == 'asc' else '-price'
        medicines = medicines.order_by(sort_field)
    elif sort == 'rating':
        sort_field = 'rating' if order == 'asc' else '-rating'
        medicines = medicines.order_by(sort_field)
    elif sort == 'formula':
        sort_field = 'formula' if order == 'asc' else '-formula'
        medicines = medicines.order_by(sort_field)
    else:
        medicines = medicines.order_by('medicine_name')

    context = {
        'medicines': medicines,
        'query': query,
        'sort': sort,
        'order': order,
        'rating_filter': rating_filter,
    }
    return render(request, 'sample_uk_meds/medicine_list.html', context)


def medicine_detail(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    # Find up to 5 similar medicines by formula or medicine name (excluding the current one)
    similar_meds = (
        Medicine.objects
        .filter(
            (
                models.Q(formula=medicine.formula) |
                models.Q(medicine_name__icontains=medicine.medicine_name)
            ),
            ~models.Q(pk=medicine.pk)
        )
        .distinct()
        .order_by('medicine_name')[:5]
    )
    return render(
        request,
        'sample_uk_meds/medicine_detail.html',
        {'medicine': medicine, 'similar_meds': similar_meds}
    )