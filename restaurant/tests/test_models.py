from datetime import datetime, timezone

from django.test import TestCase

from restaurant.models import Booking, Category, MenuItem


class CategoryModelTest(TestCase):
    def test_string_representation(self):
        category = Category.objects.create(slug='main', title='Main Dishes')
        self.assertEqual(str(category), 'Main Dishes')
        self.assertIsInstance(category.title, str)


class MenuItemModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(slug='starters', title='Starters')

    def test_create_menu_item(self):
        item = MenuItem.objects.create(
            title='Greek Salad', price=12.50, featured=True, category=self.category
        )
        self.assertEqual(str(item), 'Greek Salad')
        self.assertTrue(item.featured)
        self.assertEqual(item.category, self.category)


class BookingModelTest(TestCase):
    def test_create_booking(self):
        booking = Booking.objects.create(
            name='Maria Kovač',
            no_of_guests=4,
            booking_date=datetime(2026, 12, 24, 19, 0, tzinfo=timezone.utc),
        )
        self.assertEqual(booking.no_of_guests, 4)
        self.assertIn('Maria Kovač', str(booking))
