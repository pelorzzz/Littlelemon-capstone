Little Lemon Capstone - API paths for peer review
==================================================

Base URL (local): http://127.0.0.1:8000/

Static page:
  /

API endpoints:
  /api/menu-items/             GET, POST     (list / create menu items - Manager group required to write)
  /api/menu-items/<id>/        GET, PUT, DELETE
  /api/bookings/               GET, POST     (requires authentication)
  /api/bookings/<id>/          GET, PUT, DELETE
  /api/registration/           POST          (create a new user + auth token)
  /api/login/                  POST          (get an auth token for an existing user)

How to test with Insomnia / curl:
1. POST /api/registration/ with {"username": "...", "password": "..."} to get a token.
2. Add header "Authorization: Token <token>" to subsequent requests.
3. GET/POST /api/menu-items/ and /api/bookings/ as above.

To make a user a Manager (so they can create/edit/delete menu items):
  python manage.py shell
  >>> from django.contrib.auth.models import User, Group
  >>> g, _ = Group.objects.get_or_create(name='Manager')
  >>> User.objects.get(username='<username>').groups.add(g)
