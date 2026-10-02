from datetime import datetime, timezone

from django.contrib.auth.models import Group, User
from rest_framework import status
from rest_framework.test import APITestCase

from restaurant.models import Category, MenuItem


class RegistrationAndLoginTest(APITestCase):
    def test_register_new_user(self):
        response = self.client.post('/api/registration/', {
            'username': 'newcustomer',
            'password': 'StrongPass123',
            'email': 'newcustomer@example.com',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)

    def test_register_duplicate_username_fails(self):
        User.objects.create_user(username='existing', password='pass12345')
        response = self.client.post('/api/registration/', {
            'username': 'existing',
            'password': 'pass12345',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_valid_credentials(self):
        User.objects.create_user(username='diner', password='pass12345')
        response = self.client.post('/api/login/', {
            'username': 'diner',
            'password': 'pass12345',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_with_invalid_credentials(self):
        response = self.client.post('/api/login/', {
            'username': 'ghost',
            'password': 'wrong',
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class MenuItemAPITest(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(slug='mains', title='Main Dishes')
        self.manager_group, _ = Group.objects.get_or_create(name='Manager')

        self.manager = User.objects.create_user(username='manager', password='pass12345')
        self.manager.groups.add(self.manager_group)

        self.customer = User.objects.create_user(username='customer', password='pass12345')

    def test_anonymous_user_cannot_list_menu_items(self):
        response = self.client.get('/api/menu-items/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_customer_can_read_menu_items(self):
        self.client.force_authenticate(user=self.customer)
        response = self.client.get('/api/menu-items/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_customer_cannot_create_menu_item(self):
        self.client.force_authenticate(user=self.customer)
        response = self.client.post('/api/menu-items/', {
            'title': 'Lemon Dessert', 'price': 8.00, 'category_id': self.category.id,
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_manager_can_create_menu_item(self):
        self.client.force_authenticate(user=self.manager)
        response = self.client.post('/api/menu-items/', {
            'title': 'Lemon Dessert', 'price': 8.00, 'category_id': self.category.id,
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MenuItem.objects.count(), 1)


class BookingAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='diner', password='pass12345')

    def test_authenticated_user_can_create_booking(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/bookings/', {
            'name': 'Table for two',
            'no_of_guests': 2,
            'booking_date': datetime(2026, 11, 1, 18, 30, tzinfo=timezone.utc),
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_anonymous_user_cannot_create_booking(self):
        response = self.client.post('/api/bookings/', {
            'name': 'Table for two',
            'no_of_guests': 2,
            'booking_date': datetime(2026, 11, 1, 18, 30, tzinfo=timezone.utc),
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
