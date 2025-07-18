
from django.test import TestCase
from .models import Medicine
from django.urls import reverse

 # Medicines Search/Sort Tests

class MedicineSearchTests(TestCase):
    def setUp(self):
        self.aspirin = Medicine.objects.create(
            medicine_name="Aspirin",
            formula="Acetylsalicylic Acid",
            dose="300mg",
            manufacturer="Bayer",
            price=1.0,
            rating=4.0,
        )
        self.aspirin2 = Medicine.objects.create(
            medicine_name="Aspirin (Generic)",
            formula="Acetylsalicylic Acid",
            dose="300mg",
            manufacturer="Teva",
            price=0.8,
            rating=3.5,
        )
        self.para = Medicine.objects.create(
            medicine_name="Paracetamol",
            formula="Paracetamol",
            dose="500mg",
            manufacturer="GSK",
            price=1.2,
            rating=4.5,
        )

    def test_search_by_name(self):
        response = self.client.get('/medicines/?q=aspirin')
        self.assertContains(response, "Aspirin")
        self.assertNotContains(response, "Paracetamol")

    def test_search_by_formula(self):
        response = self.client.get('/medicines/?q=acetyl')
        self.assertContains(response, "Aspirin")
        self.assertNotContains(response, "Paracetamol")

    def test_no_results(self):
        response = self.client.get('/medicines/?q=xyz')
        self.assertContains(response, "No medicines found")


class SimilarMedicinesTests(TestCase):
    def setUp(self):
        self.main = Medicine.objects.create(
            medicine_name="Ibuprofen",
            formula="Ibuprofen",
            dose="200mg",
            manufacturer="Reckitt",
            price=2.0,
            rating=4.0,
        )
        self.similar1 = Medicine.objects.create(
            medicine_name="Ibuprofen Forte",
            formula="Ibuprofen",
            dose="400mg",
            manufacturer="Reckitt",
            price=2.5,
            rating=4.2,
        )
        self.similar2 = Medicine.objects.create(
            medicine_name="Ibuprofen (Generic)",
            formula="Ibuprofen",
            dose="200mg",
            manufacturer="Teva",
            price=1.8,
            rating=3.8,
        )
        self.other = Medicine.objects.create(
            medicine_name="Paracetamol",
            formula="Paracetamol",
            dose="500mg",
            manufacturer="GSK",
            price=1.2,
            rating=4.5,
        )

    def test_similar_medicines_displayed(self):
        response = self.client.get(f'/medicines/{self.main.pk}/')
        # Should show both similar1 and similar2, but not self.main or self.other
        self.assertContains(response, "Ibuprofen Forte")
        self.assertContains(response, "Ibuprofen (Generic)")
        self.assertNotContains(response, "Paracetamol")
        # Should not list itself as similar
        self.assertNotContains(
            response,
            '<a href="/medicines/{}/">Ibuprofen</a>'.format(self.main.pk)
        )

    def test_no_similar_medicines(self):
        response = self.client.get(f'/medicines/{self.other.pk}/')
        self.assertContains(response, "No similar medicines found.")
 
  

class MedicineSortFilterTests(TestCase):
    def setUp(self):
        Medicine.objects.create(
            medicine_name="AlphaMed", formula="F", dose="D", manufacturer="M",
            price=2.0, rating=3.0
        )
        Medicine.objects.create(
            medicine_name="BetaMed", formula="F", dose="D", manufacturer="M",
            price=1.0, rating=5.0
        )
        Medicine.objects.create(
            medicine_name="GammaMed", formula="F", dose="D", manufacturer="M",
            price=3.0, rating=4.0
        )

    def test_sort_by_price_asc(self):
        response = self.client.get('/medicines/?sort=price&order=asc')
        content = response.content.decode()
        self.assertTrue(
            content.index("BetaMed") < content.index("AlphaMed") < content.index("GammaMed")
        )

    def test_sort_by_price_desc(self):
        response = self.client.get('/medicines/?sort=price&order=desc')
        content = response.content.decode()
        self.assertTrue(
            content.index("GammaMed") < content.index("AlphaMed") and
            content.index("AlphaMed") < content.index("BetaMed")
        )

    def test_filter_by_rating(self):
        response = self.client.get('/medicines/?rating=5')
        self.assertContains(response, "BetaMed")
        self.assertNotContains(response, "AlphaMed")
        self.assertNotContains(response, "GammaMed")

    def test_filter_by_rating_and_sort(self):
        response = self.client.get('/medicines/?rating=4&sort=price&order=asc')
        content = response.content.decode()
        # Only BetaMed and GammaMed should be present,
        # BetaMed (1.0) before GammaMed (3.0)
        self.assertTrue(content.index("BetaMed") < content.index("GammaMed"))
        self.assertNotIn("AlphaMed", content)

    def test_no_results(self):
        response = self.client.get('/medicines/?rating=6')
        self.assertContains(
            response,
            "No medicines found matching your search and filters."
        )

  
# --- Cart and Checkout View Tests ---
# --- Cart and Checkout View Tests ---

class CartViewTests(TestCase):
    def setUp(self):
        self.med1 = Medicine.objects.create(
            medicine_name="TestMed1",
            formula="F1",
            dose="D1",
            manufacturer="M1",
            price=5.0,
            rating=4.0,
        )
        self.med2 = Medicine.objects.create(
            medicine_name="TestMed2",
            formula="F2",
            dose="D2",
            manufacturer="M2",
            price=7.0,
            rating=3.0,
        )

    def test_add_to_cart_and_view_cart(self):
        # Add med1 to cart
        response = self.client.get(reverse('add_to_cart', args=[self.med1.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect to cart
        # View cart
        response = self.client.get(reverse('view_cart'))
        self.assertContains(response, "TestMed1")
        self.assertContains(response, "£5.00")

    def test_remove_from_cart(self):
        # Add and then remove
        self.client.get(reverse('add_to_cart', args=[self.med2.pk]))
        response = self.client.get(
            reverse('remove_from_cart', args=[self.med2.pk])
        )
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('view_cart'))
        self.assertNotContains(response, "TestMed2")

    def test_cart_checkout_redirects_if_empty(self):
        response = self.client.get(reverse('cart_checkout'))
        self.assertEqual(response.status_code, 302)  # Should redirect to cart

    def test_cart_checkout_with_items(self):
        # Add to cart
        self.client.get(reverse('add_to_cart', args=[self.med1.pk]))
        # Simulate checkout page (should redirect to Stripe, but we check for redirect)
        response = self.client.get(reverse('cart_checkout'))
        self.assertEqual(response.status_code, 302)
