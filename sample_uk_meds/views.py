
from django.contrib.auth.decorators import login_required
from .models_profile import UserProfile
from .models import Medicine
from django.db.models import Avg, Count

# Decorator to restrict view to healthcare professionals
def healthcare_professional_required(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        try:
            profile = UserProfile.objects.get(user=request.user)
            if profile.is_healthcare_professional:
                return view_func(request, *args, **kwargs)
        except UserProfile.DoesNotExist:
            pass
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("You do not have permission to access this page.")
    return _wrapped_view

# Healthcare Dashboard view with analytics
@healthcare_professional_required
def healthcare_dashboard(request):
    total_meds = Medicine.objects.count()
    agg = Medicine.objects.aggregate(
        avg=Avg('price'),
        min_price=models.Min('price'),
        max_price=models.Max('price'),
        avg_rating=Avg('rating')
    )
    avg_price = agg['avg']
    min_price = agg['min_price']
    max_price = agg['max_price']
    avg_rating = agg['avg_rating']
    top_manufacturers = (
        Medicine.objects.values('manufacturer')
        .annotate(count=Count('id'))
        .order_by('-count')[:3]
    )
    # For Chart.js: labels and counts for top manufacturers
    manufacturer_labels = [m['manufacturer'] for m in top_manufacturers]
    manufacturer_counts = [m['count'] for m in top_manufacturers]

    # Find medicine names for min and max price
    min_price_medicine = Medicine.objects.filter(price=min_price).first()
    max_price_medicine = Medicine.objects.filter(price=max_price).first()
    min_price_medicine_name = min_price_medicine.medicine_name if min_price_medicine else 'N/A'
    max_price_medicine_name = max_price_medicine.medicine_name if max_price_medicine else 'N/A'

    # Ratings distribution (1-5 stars)
    ratings_distribution = [
        Medicine.objects.filter(rating__gte=i, rating__lt=i+1).count() for i in range(1, 5)
    ]
    ratings_distribution.append(Medicine.objects.filter(rating=5).count())

    import json
    return render(request, 'sample_uk_meds/healthcare_dashboard.html', {
        'total_meds': total_meds,
        'avg_price': avg_price,
        'min_price': min_price,
        'max_price': max_price,
        'avg_rating': avg_rating,
        'top_manufacturers': top_manufacturers,
        'manufacturer_labels': json.dumps(manufacturer_labels),
        'manufacturer_counts': json.dumps(manufacturer_counts),
        'min_price_medicine': min_price_medicine_name,
        'max_price_medicine': max_price_medicine_name,
        'ratings_distribution': json.dumps(ratings_distribution),
    })

"""
views.py
--------
Contains all view functions for the sample_uk_meds app, including CRUD for medicines,
user registration, cart management, and Stripe payment integration.
"""

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
    """Create a new medicine entry via a form."""
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
    """Update an existing medicine entry by primary key."""
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
    """Delete a medicine entry by primary key after confirmation."""
    medicine = get_object_or_404(Medicine, pk=pk)
    if request.method == 'POST':
        medicine.delete()
        return redirect('medicine_list')
    return render(request, 'sample_uk_meds/medicine_confirm_delete.html', {'medicine': medicine})

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models_profile import UserProfile
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect, render


# Custom UserCreationForm to remove username help text

from django import forms as djforms
class CustomUserCreationForm(UserCreationForm):
    is_healthcare_professional = djforms.BooleanField(
        required=False,
        label="I am a healthcare professional"
    )
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields
        help_texts = {
            'username': '',  # Remove or customize help text here
        }

def register(request):
    """Register a new user using a custom user creation form, with role."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            is_hp = form.cleaned_data.get('is_healthcare_professional', False)
            UserProfile.objects.create(user=user, is_healthcare_professional=is_hp)
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
    """Start a Stripe checkout session for a single medicine purchase."""
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
    """Render the payment success page after Stripe checkout."""
    return render(request, 'sample_uk_meds/payment_success.html')


# Create your views here.

def home(request):
    """Render the home page."""
    return render(request, 'sample_uk_meds/home.html')


def medicine_list(request):
    """Display a list of medicines with search, filter, and sort options."""
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
    """Show details for a single medicine and up to 5 similar medicines."""
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
    """Add a medicine to the session-based cart."""
    cart = request.session.get('cart', {})
    cart[str(pk)] = cart.get(str(pk), 0) + 1
    request.session['cart'] = cart
    return redirect('view_cart')

def view_cart(request):
    """Display the contents of the cart and the total price."""
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
    """Remove a medicine from the session-based cart."""
    cart = request.session.get('cart', {})
    if str(pk) in cart:
        del cart[str(pk)]
        request.session['cart'] = cart
    return redirect('view_cart')


# --- CART CHECKOUT VIEW ---
import stripe
from django.conf import settings

def cart_checkout(request):
    """Start a Stripe checkout session for all items in the cart."""
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