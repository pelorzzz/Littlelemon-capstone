from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('api/menu-items/', views.MenuItemsView.as_view()),
    path('api/menu-items/<int:pk>/', views.SingleMenuItemView.as_view()),

    path('api/bookings/', views.BookingListView.as_view()),
    path('api/bookings/<int:pk>/', views.SingleBookingView.as_view()),

    path('api/registration/', views.RegistrationView.as_view()),
    path('api/login/', views.LoginView.as_view()),
]
