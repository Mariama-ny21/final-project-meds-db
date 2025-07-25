
"""
models.py
---------
Defines database models for medicines, orders, and order items.
Each model represents a table in the database and uses Django's ORM for data management.
"""

from django.contrib.auth.models import User
from django.db import models



class Medicine(models.Model):
    """
    Represents a medicine available in the system.
    Fields include name, formula, dose, manufacturer, price, rating, and EMC leaflet URL.
    """
    medicine_name = models.CharField(
        max_length=200,
        help_text="Commercial name of the medicine"
    )
    formula = models.CharField(
        max_length=200,
        help_text="Active ingredient or formula"
    )
    dose = models.CharField(
        max_length=200,
        help_text="Dosage and packaging information"
    )
    manufacturer = models.CharField(
        max_length=100,
        help_text="Manufacturer name"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Price in British pounds"
    )
    rating = models.FloatField(
        help_text="Customer/clinical rating out of 5 (Demo only)"
    )
    emc_leaflet_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="URL to the EMC patient leaflet for this medicine"
    )
    common_usage = models.CharField(
        max_length=255,
        blank=True,
        help_text="Short summary of what the medicine is commonly used for (e.g. headache, cold & flu)"
    )

    class Meta:
        ordering = ['medicine_name']
        verbose_name = "Medicine"
        verbose_name_plural = "Medicines"

    def __str__(self):
        return f"{self.medicine_name} - {self.manufacturer}"

    def get_price_display(self):
        """Return formatted price with currency symbol"""
        return f"£{self.price}"

    def get_rating_display(self):
        """Return rating with star representation"""
        stars = "★" * int(self.rating) + "☆" * (5 - int(self.rating))
        return f"{self.rating}/5 {stars} (Demo only)"



# Order status choices
ORDER_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('processing', 'Processing'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
]


class Order(models.Model):
    """
    Represents a user's order, containing one or more order items.
    Tracks user, status, and order date.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS_CHOICES,
        default='pending'
    )
    ordered_at = models.DateTimeField(auto_now_add=True)
    # Add more fields as needed, e.g., shipping_address, etc.

    def __str__(self):
        return f"Order #{self.id} by {self.user.username} ({self.status})"


class OrderItem(models.Model):
    """
    Represents a single item in an order, linking a medicine to an order with a quantity.
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return (
            f"{self.quantity} x {self.medicine.medicine_name} "
            f"(Order #{self.order.id})"
        )