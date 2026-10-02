from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return self.title


class MenuItem(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    featured = models.BooleanField(default=False, db_index=True)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name='menu_items'
    )

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Booking(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bookings',
        null=True, blank=True
    )
    name = models.CharField(max_length=255)
    no_of_guests = models.PositiveSmallIntegerField(default=1)
    booking_date = models.DateTimeField()
    notes = models.CharField(max_length=500, blank=True)

    class Meta:
        ordering = ['booking_date']

    def __str__(self):
        return f'{self.name} - {self.booking_date:%Y-%m-%d %H:%M}'
