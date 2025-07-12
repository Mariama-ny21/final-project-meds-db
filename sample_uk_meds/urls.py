from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('medicines/', views.medicine_list, name='medicine_list'),
    path('medicines/<int:pk>/', views.medicine_detail, name='medicine_detail'),
    path('medicines/add/', views.medicine_create, name='medicine_create'),
    path('medicines/<int:pk>/edit/', views.medicine_update, name='medicine_update'),
    path('medicines/<int:pk>/delete/', views.medicine_delete, name='medicine_delete'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # Stripe payment URLs
    path('buy/<int:pk>/', views.buy_medicine, name='buy_medicine'),
    path('payment/success/', views.payment_success, name='payment_success'),
    # Cart URLs
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/checkout/', views.cart_checkout, name='cart_checkout'),
]

