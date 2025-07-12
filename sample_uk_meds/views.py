from django.urls import reverse
from .models import Medicine
from django import forms

# Medicine form for create/update
class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['medicine_name', 'formula', 'dose', 'manufacturer', 'price', 'rating', 'emc_leaflet_url']

# CREATE
def medicine_create(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('medicine_list')
    else:
        form = MedicineForm()
    return render(request, 'sample_uk_meds/medicine_form.html', {'form': form, 'action': 'Add'})

# UPDATE
def medicine_update(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    if request.method == 'POST':
        form = MedicineForm(request.POST, instance=medicine)
        if form.is_valid():
            form.save()
            return redirect('medicine_detail', pk=medicine.pk)
    else:
        form = MedicineForm(instance=medicine)
    return render(request, 'sample_uk_meds/medicine_form.html', {'form': form, 'action': 'Edit'})

# DELETE
def medicine_delete(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    if request.method == 'POST':
        medicine.delete()
        return redirect('medicine_list')
    return render(request, 'sample_uk_meds/medicine_confirm_delete.html', {'medicine': medicine})

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

import stripe
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from .models import Medicine
from django.db import models

stripe.api_key = settings.STRIPE_SECRET_KEY
# Create your views here.

def buy_medicine(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    price_str = str(medicine.price).replace('£', '').strip()
    try:
        price_pence = int(float(price_str) * 100)
    except ValueError:
        price_pence = 100  # fallback to £1.00 if price is invalid

    from django.urls import reverse
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'gbp',
                'product_data': {
                    'name': medicine.medicine_name,
                },
                'unit_amount': price_pence,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('payment_success')),
        cancel_url=request.build_absolute_uri(reverse('medicine_list')),
    )
    return redirect(session.url, code=303)

def payment_success(request):
    return render(request, 'sample_uk_meds/payment_success.html')


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

    # Sorting (Vitamin D Gummies last)
    if sort == 'price':
        sort_field = 'price' if order == 'asc' else '-price'
        medicines = medicines.order_by(sort_field)
    elif sort == 'rating':
        sort_field = 'rating' if order == 'asc' else '-rating'
        medicines = medicines.order_by(sort_field)
    elif sort == 'formula':
        sort_field = 'formula' if order == 'asc' else '-formula'
        medicines = medicines.order_by(sort_field)
    elif sort == 'manufacturer':
        sort_field = 'manufacturer' if order == 'asc' else '-manufacturer'
        medicines = medicines.order_by(sort_field)
    else:
        medicines = medicines.order_by('medicine_name')

    # Move Vitamin D Gummies to the end
    vitamin_d_gummies = medicines.filter(medicine_name__iexact='Vitamin D Gummies')
    medicines = medicines.exclude(medicine_name__iexact='Vitamin D Gummies')
    medicines = list(medicines) + list(vitamin_d_gummies)

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

# --- CART VIEWS ---
from django.http import JsonResponse

def add_to_cart(request, pk):
    cart = request.session.get('cart', {})
    cart[str(pk)] = cart.get(str(pk), 0) + 1
    request.session['cart'] = cart
    return redirect('view_cart')

def view_cart(request):
    cart = request.session.get('cart', {})
    medicines = []
    total = 0
    for pk, qty in cart.items():
        try:
            med = Medicine.objects.get(pk=pk)
            price = float(str(med.price).replace('£', '').strip())
            subtotal = price * qty
            medicines.append({'medicine': med, 'quantity': qty, 'subtotal': subtotal})
            total += subtotal
        except Medicine.DoesNotExist:
            continue
    return render(request, 'sample_uk_meds/cart.html', {'cart_items': medicines, 'total': total})

def remove_from_cart(request, pk):
    cart = request.session.get('cart', {})
    if str(pk) in cart:
        del cart[str(pk)]
        request.session['cart'] = cart
    return redirect('view_cart')


# --- CART CHECKOUT VIEW ---
import stripe
from django.conf import settings

def cart_checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('view_cart')
    line_items = []
    for pk, qty in cart.items():
        try:
            med = Medicine.objects.get(pk=pk)
            price = float(str(med.price).replace('£', '').strip())
            price_pence = int(price * 100)
            line_items.append({
                'price_data': {
                    'currency': 'gbp',
                    'product_data': {
                        'name': med.medicine_name,
                    },
                    'unit_amount': price_pence,
                },
                'quantity': qty,
            })
        except Medicine.DoesNotExist:
            continue
    if not line_items:
        return redirect('view_cart')
    stripe.api_key = settings.STRIPE_SECRET_KEY
    from django.urls import reverse
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri(reverse('payment_success')),
        cancel_url=request.build_absolute_uri(reverse('view_cart')),
    )
    return redirect(session.url, code=303)